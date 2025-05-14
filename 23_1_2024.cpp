#include<bits/stdc++.h>
using namespace std;

class node{
	public:
		int data;
		node* left;
		node* right;
		node(int val){
			data = val;
			left = NULL;
			right = NULL;
		}
};

void inorder(node* root){
	if(!root){
		return;
	}
	inorder(root->left);
	cout<<root->data<<"->";
	inorder(root->right);
}

void preorder(node* root){
	if(!root){
		return;
	}
	cout<<root->data<<"->";
	preorder(root->left);
	preorder(root->right);
}

void postorder(node* root){
	if(!root){
		return;
	}
	postorder(root->left);
	postorder(root->right);
	cout<<root->data<<"->";
}

node* insert(int arr[],int n){
	node* root = new node(arr[0]);
	queue<node*>q;
	q.push(root);
	int i=1;
	while(i<n){
		node* cur = q.front();
		q.pop();
		if(i<n){
			cur->left = new node(arr[i]);
			q.push(cur->left);
		}
		i++;
		if(i<n){
			cur->right = new node(arr[i]);
			q.push(cur->right);
		}
		i++;
	}
	return root;
}

int main(){
	int n;
	cin>>n;
	int arr[n];
	for(int i=0; i<n; i++){
		cin>>arr[i];
	}
	node* root = insert(arr,n);
	cout<<"Preorder : ";
	preorder(root);
	cout<<"\nInorder : ";
	inorder(root);
	cout<<"\nPostorder : ";
	postorder(root);

	
}
