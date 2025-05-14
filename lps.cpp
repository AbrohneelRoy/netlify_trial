#include<bits/stdc++.h>
#include <algorithm>
using namespace std;

void lps(string s,string r){
    int l=s.length();
    int arr[l+1][l+1];
    for(int i=0;i<=l; i++){
        for(int j=0; j<=l; j++){
            arr[i][j]=0;
        }
    }
    for(int i=1; i<=l; i++){
        for(int j=1; j<=l; j++){
            if(s[i-1]==r[j-1]){
                arr[i][j]=1+arr[i-1][j-1];
            }
            else{
                arr[i][j]=max(arr[i][j-1],arr[i-1][j]);
            }
        }
    }
    cout<<arr[l][l]<<endl;
    int i=l+1,j=l+1;
    string t="";
    while (i>0 && j>0){
    	if(s[i-1]==r[j-1]){
    		t=t+s[i-1];
    		i--;
    		j--;
		}
		else if(arr[i-1][j]>arr[i][j-1]){
			i--;
		}
		else{
			j--;
		}
	}
	cout<<t<<endl;
	for(int i=0; i<=l; i++){
		for(int j=0; j<=l; j++){
			cout<<arr[i][j]<<" ";
		}
		cout<<endl;
	}
}

int main(){
    string s;
    cin>>s;
    string r=s;
    reverse(r.begin(), r.end());
    lps(s,r);
}
