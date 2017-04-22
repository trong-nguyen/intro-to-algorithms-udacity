#ifndef linked_list_h
#define linked_list_h

class Node {
public:
	typedef int DataType;
	Node(const DataType & value);
	DataType data;
	Node * next;
};

class LinkedList{
public:
	LinkedList();
	~LinkedList();

	void add(const Node::DataType & value);
	Node::DataType pop();
	Node * begin();

	int size() const;
private:
	Node * head;
	int counts;
};

#endif