/*#include<bits/stdc++.h>
using namespace std;
int n,board[100][100];
const int moves[8][2]={{2,1},{1,2},{-1,2},{-2,1},{-2,-1},{-1,-2},{1,-2},{2,-1}};

bool safe(int x,int y){
	return(x>=0 && y>=0 && x<n && y<n && board[x][y]==-1);
}

void printsol(){
	cout<<"Solution : "<<endl;
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cout<<board[i][j]<<" ";
		}
		cout<<endl;
	}
}

bool knightalg(int x, int y, int c){
	if(c==n*n){
		return true;
	}
	for(int i=0; i<8; i++){
		int nextx=x+moves[i][0];
		int nexty=y+moves[i][1];
		if(safe(nextx,nexty)){
			board[nextx][nexty]=c;
			if(knightalg(nextx,nexty,c+1)){
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
	if(knightalg(sx,sy,1)){
		printsol();
	}
	else{
		cout<<"No solution!";
	}
}

#include<iostream>
using namespace std;

int sundaram(int n){
	int N=(n-1)/2;
	bool mark[N+1];
	for(int i=1; i<=N;i++){
		for(int j=1; (i+j+2*i*j)<=N; j++){
			mark[i+j+2*i*j]=true;
		}
	}
	if(n>=2){
		cout<<"2 ";
	}
	for(int i=1; i<=N;i++){
		if(!mark[i]){
			cout<<2*i+1<<" ";
		}
		
	}
}

int main(){
	int n;
	cin >>n;
	sundaram(n);
}

#include<iostream>
using namespace std;
int cost[100][100],r,c;

int mincost(){
	for(int i=1;i<r; i++){
		cost[i][0]+=cost[i-1][0];
	}
	for(int i=1;i<r; i++){
		cost[0][i]+=cost[0][i-1];
	}
	for(int i=1; i<r; i++){
		for(int j=1; j<c; j++){
			cost[i][j]+=min(cost[i-1][j],cost[i][j-1]);
		}
	}
}

int main(){
	cin>>r>>c;
	for(int i=0; i<r; i++){
		for(int j=0; j<c; j++){
			cin>>cost[i][j];
		}
	}
	mincost();
	cout<<cost[r-1][c-1];
}


#include<iostream>
using namespace std;
int sub[100],n,list[100];


int print(int size){
	for(int i=0; i<size; i++){
		cout<<sub[i]<<" ";
	}
	cout<<endl;
}
void subs(int n,int sum,int si, int tsum,int size){
	if(tsum==sum){
		print(size);
		return;
	}
	else{
		for(int i=si; i<n ;i++){
			sub[size]=list[i];
			subs(n,sum+list[i],i+1,tsum,size+1);
		}
	}
}

int main(){
	cin>>n;
	for(int i=0; i<n; i++){
		cin>>list[i];
	}
	int sum;
	cin>>sum;
	subs(n,0,0,sum,0);
	
}

#include <bits/stdc++.h>
using namespace std;
int coins[20];
int count(int n, int sum)
{

	if (sum == 0)
		return 1;
	if (sum < 0)
		return 0;
	if (n <= 0)
		return 0;
	return count(n, sum - coins[n - 1]) + count(n - 1, sum);
}

int main()
{
	int n;
	cin>>n;
	for(int i=0; i<n; i++){
		cin>>coins[i];
	}
	int sum;
	cin>>sum;
	cout << count(n, sum);
	return 0;
}

#include<iostream>
using namespace std;
const int n=9;
int grid[n][n];

bool safe(int r,int c,int s){
	for(int i=0; i<n; i++){
		if(grid[r][i]==s){
			return false;
		}
	}
	for(int i=0; i<n; i++){
		if(grid[i][c]==s){
			return false;
		}
	}
	int sr=r-r%3;
	int sc=c-c%3;
	for(int i=0; i<3; i++){
		for(int j=0; j<3; j++){
			if(grid[sr+i][sc+j]==s){
				return false;
			}
		}
	}
	return true;
}

int printsol(){
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cout<<grid[i][j]<<" ";
		}
		cout<<endl;
	}
}

bool salg(){
	int r,c;
	bool f=false;
	for(r=0; r<n; r++){
		for(c=0; c<n; c++){
			if(grid[r][c]==0){
				f=true;
				break;
			}
		}
		if(f){
			break;
		}
	}
	if(!f){
		return true;
	}
	for(int i=1; i<=9; i++){
		if(safe(r,c,i)){
			grid[r][c]=i;
			if(salg()){
				return true;
			}
			grid[r][c]=0;
		}
	}
	return false;
}

int main(){
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cin>>grid[i][j];
		}
	}
	if(salg()){
		printsol();
	}
	else{
		cout<<"No";
	}
	
}


#include<iostream>
using namespace std;
int graph[100][100],color[100],n;

bool safe(int x,int p){
	for(int i=0; i<n; i++){
		if(graph[p][i]==1 && x==color[i]){
			return false;
		}
	}
	return true;
}

void printsol(){
	for(int i=0; i<n; i++){
		cout<<color[i]<<" ";
		
	}
}

bool malg(int m,int p){
	if(n==p){
		return true;
	}
	for(int i=1; i<=m;i++){
		if(safe(i,p)){
			color[p]=i;
			if(malg(m,p+1)){
				return true;
			}
			color[p]=0;
		}
	}
	return false;
}

int main(){
	cin>>n;
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cin>>graph[i][j];
		}
	}
	int m;
	cin>>m;
	for(int i=0; i<n; i++){
		color[i]=0;
	}
	if(malg(m,0)){
		printsol();
	}
	else{
		cout<<"No";
	}
}*/

/*#include<bits/stdc++.h>
using namespace std;
int n,board[100][100];
const int moves[8][2]={{2,1},{1,2},{-1,2},{-2,1},{-2,-1},{-1,-2},{1,-2},{2,-1}};

bool safe(int x,int y){
	return(x>=0 && y>=0 && x<n && y<n && board[x][y]==-1);
}

void printsol(){
	cout<<"Solution : "<<endl;
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cout<<board[i][j]<<" ";
		}
		cout<<endl;
	}
}

bool knightalg(int x, int y, int c){
	if(c==n*n){
		return true;
	}
	for(int i=0; i<8; i++){
		int nextx=x+moves[i][0];
		int nexty=y+moves[i][1];
		if(safe(nextx,nexty)){
			board[nextx][nexty]=c;
			if(knightalg(nextx,nexty,c+1)){
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
	if(knightalg(sx,sy,1)){
		printsol();
	}
	else{
		cout<<"No solution!";
	}
}

#include<iostream>
using namespace std;

int sundaram(int n){
	int N=(n-1)/2;
	bool mark[N+1];
	for(int i=1; i<=N;i++){
		for(int j=1; (i+j+2*i*j)<=N; j++){
			mark[i+j+2*i*j]=true;
		}
	}
	if(n>=2){
		cout<<"2 ";
	}
	for(int i=1; i<=N;i++){
		if(!mark[i]){
			cout<<2*i+1<<" ";
		}
		
	}
}

int main(){
	int n;
	cin >>n;
	sundaram(n);
}

#include<iostream>
using namespace std;
int cost[100][100],r,c;

int mincost(){
	for(int i=1;i<r; i++){
		cost[i][0]+=cost[i-1][0];
	}
	for(int i=1;i<r; i++){
		cost[0][i]+=cost[0][i-1];
	}
	for(int i=1; i<r; i++){
		for(int j=1; j<c; j++){
			cost[i][j]+=min(cost[i-1][j],cost[i][j-1]);
		}
	}
}

int main(){
	cin>>r>>c;
	for(int i=0; i<r; i++){
		for(int j=0; j<c; j++){
			cin>>cost[i][j];
		}
	}
	mincost();
	cout<<cost[r-1][c-1];
}


#include<iostream>
using namespace std;
int sub[100],n,list[100];


int print(int size){
	for(int i=0; i<size; i++){
		cout<<sub[i]<<" ";
	}
	cout<<endl;
}
void subs(int n,int sum,int si, int tsum,int size){
	if(tsum==sum){
		print(size);
		return;
	}
	else{
		for(int i=si; i<n ;i++){
			sub[size]=list[i];
			subs(n,sum+list[i],i+1,tsum,size+1);
		}
	}
}

int main(){
	cin>>n;
	for(int i=0; i<n; i++){
		cin>>list[i];
	}
	int sum;
	cin>>sum;
	subs(n,0,0,sum,0);
	
}

#include <bits/stdc++.h>
using namespace std;
int coins[20];
int count(int n, int sum)
{

	if (sum == 0)
		return 1;
	if (sum < 0)
		return 0;
	if (n <= 0)
		return 0;
	return count(n, sum - coins[n - 1]) + count(n - 1, sum);
}

int main()
{
	int n;
	cin>>n;
	for(int i=0; i<n; i++){
		cin>>coins[i];
	}
	int sum;
	cin>>sum;
	cout << count(n, sum);
	return 0;
}

#include<iostream>
using namespace std;
const int n=9;
int grid[n][n];

bool safe(int r,int c,int s){
	for(int i=0; i<n; i++){
		if(grid[r][i]==s){
			return false;
		}
	}
	for(int i=0; i<n; i++){
		if(grid[i][c]==s){
			return false;
		}
	}
	int sr=r-r%3;
	int sc=c-c%3;
	for(int i=0; i<3; i++){
		for(int j=0; j<3; j++){
			if(grid[sr+i][sc+j]==s){
				return false;
			}
		}
	}
	return true;
}

int printsol(){
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cout<<grid[i][j]<<" ";
		}
		cout<<endl;
	}
}

bool salg(){
	int r,c;
	bool f=false;
	for(r=0; r<n; r++){
		for(c=0; c<n; c++){
			if(grid[r][c]==0){
				f=true;
				break;
			}
		}
		if(f){
			break;
		}
	}
	if(!f){
		return true;
	}
	for(int i=1; i<=9; i++){
		if(safe(r,c,i)){
			grid[r][c]=i;
			if(salg()){
				return true;
			}
			grid[r][c]=0;
		}
	}
	return false;
}

int main(){
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cin>>grid[i][j];
		}
	}
	if(salg()){
		printsol();
	}
	else{
		cout<<"No";
	}
	
}


#include<iostream>
using namespace std;
int graph[100][100],color[100],n;

bool safe(int x,int p){
	for(int i=0; i<n; i++){
		if(graph[p][i]==1 && x==color[i]){
			return false;
		}
	}
	return true;
}

void printsol(){
	for(int i=0; i<n; i++){
		cout<<color[i]<<" ";
		
	}
}

bool malg(int m,int p){
	if(n==p){
		return true;
	}
	for(int i=1; i<=m;i++){
		if(safe(i,p)){
			color[p]=i;
			if(malg(m,p+1)){
				return true;
			}
			color[p]=0;
		}
	}
	return false;
}

int main(){
	cin>>n;
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cin>>graph[i][j];
		}
	}
	int m;
	cin>>m;
	for(int i=0; i<n; i++){
		color[i]=0;
	}
	if(malg(m,0)){
		printsol();
	}
	else{
		cout<<"No";
	}
}

#include<iostream>
using namespace std;
int graph[100][100],n,path[100];

bool safe(int m,int p){
	if(graph[path[p-1]][m]==0){
		return false;
	}
	for(int i=0; i<p ;i++){
		if(path[i]==m){
			return false;
		}
	}
	return true;
}

void printsol(){
	for(int i=0; i<n; i++){
		cout<<path[i]<<" ";
	}
	cout<<path[0];
}

bool halg(int p){
	if(p==n){
		return true;
	}
	for(int i=1; i<n; i++){
		if(safe(i,p)){
			path[p]=i;
			if(halg(p+1)){
				return true;
			}
			path[p]=-1;
		}
	}
	return false;
}

int main(){
	cin>>n;
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cin>>graph[i][j];
		}
	}
	for(int i=0; i<n; i++){
		path[i]=-1;
	}
	path[0]=0;
	if(halg(1))
		printsol();
	}
	else{
		cout<<"No";
	}
}
#include<bits/stdc++.h>
using namespace std;

int subset_count=0;
void subset_sum(int list[], int n, int sum, int s_index, int t_sum){
    if(t_sum==sum){
        subset_count++;
        if(s_index<n){
            subset_sum(list,n,sum-list[s_index-1],s_index,t_sum);
        }
    }
        else{
            for(int i=s_index; i<n; i++){
                subset_sum(list,n,sum+list[i],i+1,t_sum);
            }
        }
}

int main(){
    int n, sum;
    cin>>n;
    int list[n];
    for(int i=0; i<n; i++){
        cin>>list[i];
    }
    cin>>sum;
    subset_sum(list,n,0,0,sum);
    cout<<subset_count;
    return 0;
}*/

#include<bits/stdc++.h>
using namespace std;
int r,c,arr[100][100];

void maxf(){
    int dp[r][c]={0};
    int m=0;
    for(int i=0; i<r; i++){
        for(int j=0; j<c; j++){
            if(i==0 || j==0){
                dp[i][j]=arr[i][j];
            }
            else if(arr[i][j]==1){
                dp[i][j]=1+min(dp[i-1][j-1],min(dp[i][j-1],dp[i-1][j]));
            }
            else{
                dp[i][j]=0;
            }
            if(m<dp[i][j]){
                m=dp[i][j];
            }
        }
    }
    cout<<m<<endl;
    for(int i=0; i<r; i++){
        for(int j=0; j<c; j++){
            cout<<dp[i][j]<<" ";
        }
        cout<<endl;
    }
}

int main(){
    cin>>r>>c;
    for(int i=0; i<r; i++){
        for(int j=0; j<c; j++){
            cin>>arr[i][j];
        }
    }
    maxf();
}
