#include<bits/stdc++.h>
using namespace std;

int n,board[100][100];
const int moves[8][2]={{2,1},{1,2},{-1,2},{-2,1},{-2,-1},{-1,-2},{1,-2},{2,-1}};

bool safe(int x, int y){
	return(x>=0 && y>=0 && x<n && y<n && board[x][y]==-1);
}

void printsol(){
	cout<<"Solution: "<<endl;
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cout<<board[i][j]<<" ";
		}
		cout<<endl;
	}
}

bool kalg(int x, int y, int c){
	if(c==n*n){
		return true;
	}
	for(int i=0; i<8; i++){
		int nextx=x+moves[i][0];
		int nexty=y+moves[i][1];
		if(safe(nextx,nexty)){
			board[nextx][nexty]=c;
			if(kalg(nextx,nexty,c+1)){
				return true;
			}
			else{
				board[nextx][nexty]=-1;
			}
		}
	}
	return false;
}

int main(){
	cin>>n;
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			board[i][j]=-1;
		}
	}
	int sx=0,sy=0;
	board[sx][sy]=0;
	if(kalg(sx,sy,1)){
		printsol();
	}
	else{
		cout<<"Not there";
	}
}
