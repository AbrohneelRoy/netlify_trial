#include<bits/stdc++.h>
using namespace std;

int c=0;

void subsum(int arr[],int n,int s, int in, int ts){
	if(s==ts){
		c++;
		if(in<n){
			subsum(arr,n,s-arr[in-1],in,ts);
		}
	}
	else{
		for(int i=in; i<n; i++){
			subsum(arr,n,s+arr[i],i+1, ts);
		}
	}
	
}

int main(){
	int n,s;
	cin>>n;
	int arr[n];
	for(int i=0; i<n; i++){
		cin>>arr[i];
	}
	cin>>s;
	subsum(arr,n,0,0,s);
	cout<<c;
}
