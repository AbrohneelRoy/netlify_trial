#include<iostream>
using namespace std;

bool m(string t,string p){
    int i=0,j=0;
    while(i<t.size()&&j<p.size()){
        if(j+1<p.size()&&p[j+1]=='*'){
            char c=p[j];
            j+=2;
            while(i<t.size()&&t[i]==c)i++;
        }
        else if(j+1<p.size()&&p[j+1]=='+'){
            char c=p[j];
            j+=2;
            if(i>=t.size()||t[i]!=c)
				return 0;
            i++;
            while(i<t.size()&&t[i]==c)i++;
        }
        else{
            if(t[i]!=p[j])
				return 0;
            i++;j++;
        }
    }
    while(j+1<p.size()&&(p[j+1]=='*'||p[j+1]=='+'))j+=2;
    return i>=t.size()&&j>=p.size();
}

string res(string t,string p){
    for(int i=0;i<t.size();i++){
        for(int j=t.size()-i;j>=1;j--){
            string s=t.substr(i,j);
            if(m(s,p))
				return s;
			else{
				return "No Solution Exist";
			}
        }
    }
    return "";
}

int main(){
    string t,p;
    cin>>t>>p;
    cout<<res(t,p);
    return 0;
}
