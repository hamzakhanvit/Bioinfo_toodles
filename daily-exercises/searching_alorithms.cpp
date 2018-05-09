/******************************************************************************
Linear Search
Binary Search
Jump Search
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

int jump_search(std::vector<int> arr, int x){
    int n = arr.size();
    int step = std::sqrt(n);
    int prev=0;
    while(arr.at(min(step,n)-1)<x){
        int prev = step;
        step+=std::sqrt(n);
        if(prev>=n){
            return -1;
        }
    }    
        
    while((arr.at(prev))<x){
        prev++;
        if(prev>=n){
            return -1;
        }
    }   
    if((arr.at(prev))==x){
        return prev;
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
    
    index = jump_search(myvector,5);
    cout << "Jump Search index (-1 means absent) = " << index << "\n";
    return 0;
    
}
