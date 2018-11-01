
'''
compare_two_vcfs.py

Created by Hamza Khan on 2018-09-27

A script to compare two vcfs
'''

import argparse
import csv
import os
import re
import math
import vcf
import glob
from collections import defaultdict


clustervcfdicts = defaultdict(list)

class compare_vcfs(object):

    def __init__(self):
        pass

    def read_vcf(self, vcffile):
        """
        Reads a VCF file and makes a dictionary 
        Returns:dict
        read_vcf()->dict
        """
        read_vcf_dict = {}

        vcf_reader = vcf.Reader(open(vcffile, 'r'))

        for record in vcf_reader:
            key = record.CHROM +"_"+str(record.POS)
            read_vcf_dict[key] = record

        return read_vcf_dict


    def read_cluster_vcf(self, vcffile):
        """
        Reads a VCF file and makes a dictionary 
        Returns:dict
        read_vcf()->dict
        """
        cluster_vcf_dict = {}

        vcf_reader = vcf.Reader(open(vcffile, 'r'))

        for record in vcf_reader:
            key = record.CHROM +"_"+str(record.POS)
            clustervcfdicts[key].append([vcffile.split("/")[-2],record])


    def compare_vcf(self, readsvcfdict):
        """
        Compare records between vcf
        """     
	both_homozygous = 0
	het_to_pure_homozygous = 0
	het_to_heterozygous = 0
	missing_records = 0
	common_records = 0
	indels_in_ref = 0
        indels_in_cluster = 0
        combined = defaultdict(list)
        clustercoverage = defaultdict(list)
        refcoverage = {}
        two_or_more_alts = 0
        

	for key in readsvcfdict:

            if(len(readsvcfdict[key].REF)>1 or len(readsvcfdict[key].ALT[0])>1):
                        print "Skipping ref record!"
                        indels_in_ref+=1
                        continue

	    if(key in clustervcfdicts):
                common_records+=1
	        for record in clustervcfdicts[key]:
                			  
		    
		    #print "??????", readsvcfdict[key].REF, len(readsvcfdict[key].REF) , readsvcfdict[key].ALT[0], \
		    #      len(readsvcfdict[key].ALT[0]), record[1].REF, len(record[1].REF),\
		    #      record[1].ALT[0], len(record[1].ALT[0])

                    if (len(record[1].REF) > 1 or len(record[1].ALT[0])>1):
                        print "Skipping cluster record!"
                        indels_in_cluster+=1
                        combined[key].append('SK')
                        continue
                   
                    
                    if(len(readsvcfdict[key].ALT) > 1):
                        print "Skipping cluster record due to two or more ALT"
                        two_or_more_alts+=1
                        combined[key].append('SK')
                        continue 
   
		    print "Common, ", key, readsvcfdict[key] , readsvcfdict[key].get_hets(),  len(readsvcfdict[key].ALT), record[1], record[1].get_hets()
		    
		 
		    #Check for homozygous sites
		    if readsvcfdict[key].get_hets() == [] and record[1].get_hets() == []:
		        both_homozygous+=1
                        combined[key].append('BH')
		        print "Both homozygous"
     
		    #Count sites that were heterozygous in the original vcf and are pure homozygous in the separated cluster
		    elif readsvcfdict[key].get_hets() != [] and record[1].get_hets() == []:
		        het_to_pure_homozygous+=1
                        combined[key].append('TH') 
		        print "Het to pure homozygous"

		    #Count sites that were heterozygous in the original vcf and are also heterozygous in the separated cluster
		    elif readsvcfdict[key].get_hets() != [] and record[1].get_hets() != []:
		        het_to_heterozygous+=1
                        combined[key].append('TT')
                        clustercoverage[key].append(record[1].get_hets())
                        refcoverage[key]=(readsvcfdict[key].get_hets())
		        print "Het to heterozygous"

		    else:
		        print "CHECK"

	    else:

                missing_records+=1
		#Skip indel records
		print readsvcfdict[key].REF, readsvcfdict[key].ALT[0], len(readsvcfdict[key].REF), "#####", len(readsvcfdict[key].ALT[0]),\
                      "####", len(readsvcfdict[key].ALT)
		if(len(readsvcfdict[key].REF)>1 or len(readsvcfdict[key].ALT[0])>1):
                    print "Indel in reference vcf"
		    continue

                if(len(readsvcfdict[key].ALT)>1):
                     print "Two or more ALTs in reference vcf"
                     continue
                     
		print "No, ", key, readsvcfdict[key], readsvcfdict[key].get_hets()

		if readsvcfdict[key].get_hets() == []:
		    print "NONE"


        print "\n\n# variants in reference vcf = ", len(readsvcfdict)
        print "# variants with indels in reference vcf = ", indels_in_ref, "(Excluded from this analysis)"
        print "# single nucleotide variants in reference vcf = ", len(readsvcfdict), "-" ,indels_in_ref,"=", len(readsvcfdict) - indels_in_ref
	print "# SNV common between reference vcf and cluster vcf= ", common_records
	print "# SNVs for which records are absent in cluster vcf= ", missing_records
        print "# records with indels in cluster (Excluded from this analysis) = ", indels_in_cluster
        print "# records with two ALT in cluster = ", two_or_more_alts
	print "# records with homozygous variants = ", both_homozygous
	print "# records with heterozygous reference variant but homozygous cluster variant = ", het_to_pure_homozygous
	print "# records with heterozygous reference variant and heterozygous cluster variant = ", het_to_heterozygous

        final_counts={}
        ambiguous_genomic_pos = 0
	for key in combined:
            #print key, ":", combined[key]
            if(len(set(combined[key]))==1):
                if(combined[key][0] not in final_counts):
                    final_counts[combined[key][0]]=1
                else:
                    final_counts[combined[key][0]]+=1 
            else:
                ambiguous_genomic_pos+=1

        print final_counts

        try:
            print "# genomic position where different clusters show different evidences, i.e. ambiguous = ", ambiguous_genomic_pos
            print "# genomic position where all clusters show evidence of a homozygous variant = ", final_counts['BH']
            print "# genomic position where all clusters show evidence of a resolved haplotype, ie, het to homo = ", final_counts['TH'] 
            print "# genomic position where all clusters show evidence of a unresolved haplotype, ie, het to het = ", final_counts['TT']       

        except KeyError:
            print "\n"


        only_cluster = 0
	for key in clustervcfdicts:
	    if key not in readsvcfdict:
               for record in clustervcfdicts[key]: 
                   only_cluster+=1
		   print "only_cluster",key, record[0], record[1], record[1].get_hets()
        print "# records that were ONLY present in clusters and not in the reference (Might be due to missalignments or incorrect barcode assignments) = ", only_cluster

        #Finding allele depth ratio for each site
        for key in refcoverage:
            print "Ref = ", refcoverage[key]
            m = re.search('AD=\[(.+?)\]', str(refcoverage[key]))
            if m:
                m = m.group(1)
            m = m.split(',')  
            m = map(float, m) 
            print m
            m =  sum(m)
            print m    
            largest = 0           
            for item in clustercoverage[key]:
                c = re.search('AD=\[(.+?)\]', str(item))
                if c:
                     c = c.group(1)
                c = c.split(',')
                c = map(float, c)
                #print "c =", c
                c = sum(c)
                print "c = ", c
                if(c>largest):
                    largest = c             
            print "Allele_Depth_ref_clus =",  largest/m


def _parse_args():
    """Parse command line arguments"""



    parser = argparse.ArgumentParser(
        description = 'Compare vcf files and find differences in heterozygous SNPs for each haplotype')

    #Positional arguments
    parser.add_argument('-r', '--readsvcf',
                       default = 'None', required = True,
                       help = 'Original VCF file')

    parser.add_argument('-c', '--clusterpath',
                       default = 'None', required=True,
                       help = 'Path to cluster directory')

    args = parser.parse_args()
    return args


def main():

   args = _parse_args()
   obj = compare_vcfs()
   readsvcfdict = obj.read_vcf(args.readsvcf)
   print "Finished reading read vcf. Total records = ", len(readsvcfdict)

   for filename in glob.iglob(os.path.join(args.clusterpath, '*', '*.vcf')):
       obj.read_cluster_vcf(filename)
       print "Finished reading ", filename ," Total records = ", len(clustervcfdicts)

   obj.compare_vcf(readsvcfdict)

if __name__=='__main__':
    main()
