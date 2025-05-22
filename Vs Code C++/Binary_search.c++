#include <iostream>
using namespace std;

int main(){
    int key,i,n,k=-1,l,r,mid;
    cin>>n;
    int a[n];
    for(i=0; i<n; i++){
        cin>>a[i];
    }
    cin>>key;
    l=0; r=n-1;
    while(l<=r){
        mid=(l+r)/2;
        if(a[mid]==key){
            int y=mid;
            cout<<"The key is found "<<y+1<<" position";
            k++;
            break;
        }

        else if(a[mid]<key){
            l=mid+1;
        }
        else{
            r=mid-1;
        }
    }
    if(k==-1)
    cout<<"Not found";
} 