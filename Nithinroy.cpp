#include <iostream>
using namespace std;

struct Node{
    int data;
    Node* left;
    Node* right;
    Node(int val){
        data=val;
        left=NULL;
        right=NULL;
    }
};

Node* insertElements(Node* root, int val){
    if(root==NULL){
        return new Node(val);
    }
    
    if(val<root->data){
        root->left=insertElements(root->left, val);
    }
    else{
        root->right=insertElements(root->right, val);
    }
    return root;
}
 void inorder(Node* root,int key){
     if(root==NULL){
         return;
     }
     
     inorder(root->left);
     cout<<root->data<<" ";
     inorder(root->right);
 }
  void preorder(Node* root){
     if(root==NULL){
         return;
     }
     cout<<root->data<<" ";
     preorder(root->left);
     preorder(root->right);
 }
  void postorder(Node* root){
     if(root==NULL){
         return;
     }
     
     postorder(root->left);
     postorder(root->right);
     cout<<root->data<<" ";

 }
 void mint(Node* root){
 	Node* temp = root;
 	while(temp->left!=NULL){
 		temp = temp->left;
	 }
	 cout<<"\nMin:"<<temp->data;
 }
  void maxt(Node* root){
 	Node* temp = root;
 	while(temp->right!=NULL){
 		temp = temp->right;
	 }
	 cout<<"\nMax:"<<temp->data;
 }

int main()
{
    Node* root=NULL;
    int n;
    cin>>n;
    int arr[n];
    for(int i=0;i<n; i++){
    	cin>>arr[i];
	}
    root=insertElements(root, arr[0]);
    for(int i=1; i<n; i++){
       	insertElements(root, arr[i]);
	}

    cout << "\nPreorder Traversal: ";
    preorder(root);
    cout << "\nInorder Traversal: ";
    inorder(root,23);
    cout << "\nPostorder Traversal: ";
    postorder(root);
    mint(root);
    maxt(root);
    return 0;
}
