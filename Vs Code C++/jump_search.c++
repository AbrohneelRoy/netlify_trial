#include <bits/stdc++.h>
using namespace std;

int main(){
    int key,i,n,k=-1;
    cin>>n;
    int a[n];
    for(i=0; i<n; i++){
        cin>>a[i];
    }
cin>>key;
  
int s=0;
int end=sqrt(n);
while(a[end]<=key && end<n){
    s=end;
    end=end+sqrt(n);
    if(end>n-1)
        end=n;
}
for(int i=s; i<end;i++){
    if(a[i]==key){
        cout<<"found";
        k++;
        break;
    }
}
    if(k==-1)
        cout<<"Not Found";

}
