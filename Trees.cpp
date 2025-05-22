#include <bits/stdc++.h>
using namespace std;

class Node {
public:
    int data;
    Node* left;
    Node* right;

    Node(int val) {
        data = val;
        left = NULL;
        right = NULL;
    }
};

Node* buildTree(int nodes[], int n) {
    if (n == 0 || nodes[0] == -1) {
        return NULL;
    }

    Node* root = new Node(nodes[0]);
    queue<Node*> q;
    q.push(root);

    int index = 1;
    while (!q.empty() && index < n) {
        Node* current = q.front();
        q.pop();

        if (index < n && nodes[index] != -1) {
            current->left = new Node(nodes[index]);
            q.push(current->left);
        }
        index++;

        if (index < n && nodes[index] != -1) {
            current->right = new Node(nodes[index]);
            q.push(current->right);
        }
        index++;
    }

    return root;
}

void inorder(Node* root) {
    if (root == NULL) {
        return;
    }
    inorder(root->left);
    cout << root->data << " ";
    inorder(root->right);
}

void preorder(Node* root) {
    if (root == NULL) {
        return;
    }
    cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}

void postorder(Node* root) {
    if (root == NULL) {
        return;
    }
    postorder(root->left);
    postorder(root->right);
    cout << root->data << " ";
}

int main() {
    cout << "Enter number of nodes: ";
    int n;
    cin >> n;

    if (n <= 0) {
        cout << "Invalid number of nodes. Exiting.";
        return 0;
    }

    int nodes[n];
    cout << "Enter node values (use -1 for NULL nodes):" << endl;
    for (int i = 0; i < n; i++) {
        cin >> nodes[i];
    }

    Node* root = buildTree(nodes, n);

    cout << "\nPreorder Traversal: ";
    preorder(root);
    cout << "\nInorder Traversal: ";
    inorder(root);
    cout << "\nPostorder Traversal: ";
    postorder(root);

    return 0;
}

