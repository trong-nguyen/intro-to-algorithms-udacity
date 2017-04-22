#include <stdexcept>
#include "linked_list.h"

Node::Node(const DataType & value) {
	data = value;
	next = 0;
}

LinkedList::LinkedList() {
	head = 0;
	counts = 0;
}

LinkedList::~LinkedList() {
	while(head) {
		Node * it = head;
		head = head->next;
		delete it;
	}
}

void LinkedList::add(const Node::DataType & value) {
	Node * it = new Node(value);
	it->next = head;
	head = it;
	counts++;
}

Node::DataType LinkedList::pop() {
	Node * it = head;
	if(it){
		head = head->next;
		Node::DataType value = it->data;
		delete it;
		counts--;
		return value;
	}else{
		throw std::out_of_range("Trying to pop empty list\n");
	}
}

Node * LinkedList::begin() {
	return head;
}

int LinkedList::size() const {
	return counts;
}