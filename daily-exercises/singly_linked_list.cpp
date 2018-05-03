#include <iostream>

using namespace std;
struct node
{
    int data;
    node* next;
};

class list{
    private:
    node* head;
    node* tail;
    
    public:
    list(){
        head=NULL;
        tail=NULL;
    }
    
    void createnode(int value){
        node *temp = new node;
        temp->data = value;
        temp->next = NULL;
        if(head==NULL){
            head=temp;
            tail=temp;
            temp=NULL;
        }
        else{
            tail->next=temp;
            tail=temp;
            
        }
    }
    
    void display(){
        node *temp = new node;
        temp=head;
        while(temp!=NULL){
            cout << temp->data <<endl;
            temp=temp->next;
        }
    }
    
    void insert_start(int value){
        node *temp = new node;
        temp->data = value;
        temp->next = head;
        head = temp;
        
    }
    
    void insert_end(int value){
        node *temp = new node;
        temp->data = value;
        temp->next = NULL;
        tail->next = temp;
        tail=temp;
    }
    
    void insert_position(int pos, int value){
        node *temp = new node;
        temp->data=value;
        node *iterator = new node;
        iterator = head;
        for (int i=1;i<pos; i++){
           iterator = iterator->next;
        }
        temp->next = iterator->next;
        iterator->next = temp;
        
    }     
    
    void delete_start(){
        node *temp = new node;
        temp = head->next;
        head = temp;
    }
    
    void delete_end(){
        node *last = new node;
        node *second_last = new node;
        last = head;
        while(last->next!=NULL){
            second_last = last;
            last = last->next;
        }
        second_last->next = NULL;
        tail = second_last;
        
    }
    
};



int main()
{
    cout<<"Create a list with one node value = 2\n";
    list a;
    a.createnode(2);
    a.display();
    cout<<"\nInsert elements 10, 20 at start and 30 at the end\n";
    a.insert_start(10);
    a.insert_start(20);
    a.insert_end(30);
    a.display();
    cout<<"\nInsert element 45 at position 2\n";
    a.insert_position(2,45);
    a.display();
    cout << "\nDelete the start element\n";
    a.delete_start();
    a.display();
    cout << "\nDelete the end element\n";
    a.delete_end();
    a.display();
    
    return 0;
}

