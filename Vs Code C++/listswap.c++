#include <iostream>
using namespace std;

struct Node {
    int data;
    struct Node* next;
};

struct Node* head = NULL;

void addNode(int value) {
    struct Node* newNode = new Node;
    newNode->data = value;
    newNode->next = head;
    head = newNode;
}

void swapNodes(int a, int b) {
    if (a == b) {
        return;
    }
    struct Node *prevA = NULL, *currA = head;
    while (currA && currA->data != a) {
        prevA = currA;
        currA = currA->next;
    }

    struct Node *prevB = NULL, *currB = head;
    while (currB && currB->data != b) {
        prevB = currB;
        currB = currB->next;
    }

    if (currA == NULL || currB == NULL) {
        return;
    }

    if (prevA != NULL) {
        prevA->next = currB;
    } else {
        head = currB;
    }

    if (prevB != NULL) {
        prevB->next = currA;
    } else {
        head = currA;
    }

    struct Node* temp = currB->next;
    currB->next = currA->next;
    currA->next = temp;
}

void reverseList() {
    struct Node* current = head;
    struct Node* prev = NULL, *next = NULL;
    while (current != NULL) {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }
    head = prev;
}

void display() {
    struct Node* ptr;
    ptr = head;
    while (ptr != NULL) {
        cout<< ptr->data <<" ";
        ptr = ptr->next;
    }
    cout<< endl;
}

int main() {
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        int value;
        cin >> value;
        addNode(value);
    }
    int a, b;
    cin >> a >> b;
    swapNodes(a, b);
    reverseList();
    display();
    return 0;
}


