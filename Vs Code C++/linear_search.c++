// Online C++ compiler to run C++ program online
#include <iostream>
using namespace std;

int main(){
    int key,i,n,k=-1;
    cin>>n;
    int a[n];
    for(i=0; i<n; i++){
        cin>>a[i];
    }
    cin>>key;

    for(i=0; i<n; i++){
        if(a[i]==key){
            int t=i;
            cout<<"The key is found "<<t+1<<" position";
            k++;
            break;
        }

    }
    if(k==-1)
        cout<<"The key is not found";


}
