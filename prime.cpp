#include<iostream>
using namespace std;

int main(){
    int n,c=0;
    cin>>n;
    for(int i=2; i<n; i++){
        for(int j=1; j<n; j++){
            if(i%j==0){
                c++;
            }
        }
        if(c==2){
            cout<<i<<" ";
        }
        c=0;
    }
}
