#include<iostream>
using namespace std;
int arr[100][100];
int maxs(int r, int c){
	int temp[r][c];
	for(int i=0; i<r; i++){
		temp[i][0]=arr[i][0];
	}
	for(int i=0; i<r; i++){
		temp[0][i]=arr[0][i];
	}
	for(int i=1; i<r; i++){
		for(int j=1; j<c; j++){
			if(arr[i][j]==1){
				temp[i][j]=min(temp[i-1][j-1],min(temp[i][j-1],temp[i-1][j]))+1;
			}
			else{
				temp[i][j]=0;
			}
		}
	}
	int max=0;
	for(int i=0; i<r; i++){
		for(int j=0; j<c; j++){
			if(temp[i][j]>max){
				max=temp[i][j];
			}
		}
	}	
	return max;
}
int main(){
	int r,c;
	cin>>r>>c;
	for(int i=0; i<r; i++){
		for(int j=0; j<c; j++){
			cin>>arr[i][j];
		}
	}
	cout<<maxs(r,c);
}
