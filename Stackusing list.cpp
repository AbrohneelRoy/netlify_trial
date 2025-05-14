#include<iostream>
#include<limits.h>
using namespace std;
struct lnode{
	int data;
	struct lnode *next;
};

typedef struct lnode node;

node *top =NULL;

void push(node **top,int value){
  node *newnode = new node();
  newnode -> data = value;
  newnode -> next = *top;
  *top = newnode; 	
}

int pop(node **top){
	node *del = *top; 
	*top= (*top) -> next;
	int temp = del ->data;	
	//free(del);
	return temp;
}

int peek(node **top){
	if(*top== NULL){
		cout<<"Stack is Empty"<<endl;
		return INT_MIN;
	}
	return (*top) -> data;
}

int main()
{
	node *top1 = NULL;
	node *top2 = NULL; 
	push(&top1,3);
	push(&top1,5);
	push(&top1,7);
	push(&top2,15);
	push(&top2,17);
	cout<<"Popped is:"<<pop(&top2)<<endl;
	cout<<"Top element is: "<<peek(&top2);
	return 0;
}
