/******************************************************************************
Linear Search
Binary Search

*******************************************************************************/

#include <iostream>

using namespace std;
#include <vector>

int binary_search(vector<int> myvector, int low, int high, int elem){
    
    while(low<=high){
        int mid = low + (high-low)/2;
        //cout<<"mid = "<< mid<<endl;
        if(myvector.at(mid)==elem){
            return mid;
        }
        if(myvector.at(mid)>elem){
            return binary_search(myvector, low, mid-1, elem);
        }
        if(myvector.at(mid)<elem){
            return binary_search(myvector, mid+1, high, elem);
        }
    }
    return -1;
}

int linear_search(vector<int> myvector,int elem){
    for(int i=0;i<myvector.size();i++){
        
        if(myvector.at(i)==elem)
            return i;
            
    }
    return -1;
}

int main()
{
    vector<int>myvector = vector<int>{1,2,3,4,5}; 
    int index = linear_search(myvector, 3);
    cout << "Linear Search index (-1 means absent) = " << index << "\n";
    
    
    index = binary_search(myvector,0, (myvector.size())-1,5);
    cout << "Binary Search index (-1 means absent) = " << index << "\n";
    return 0;
}
