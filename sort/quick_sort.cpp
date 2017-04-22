#define CATCH_CONFIG_MAIN
#include <algorithm>
#include <iterator>
#include "../include/catch.hpp"
#include <vector>
#include <iostream>

typedef std::vector<int> Array;

int select_pivot(int start, int end) {
	return (start + end) / 2;
}

void swap(Array & a, int i, int j) {
	const int tmp = a[i];
	a[i] = a[j];
	a[j] = tmp;
}

int partition(Array & a, int pivot, int start, int end) {
	const int v = a[pivot];
	int i=start, j=end;
	while(i <= j){
		while(a[i] < v){
			i++;
		}
		while(a[j] > v){
			j--;
		}
		if( i <= j ){
			swap(a, i, j);
			i++;
			j--;
		}
	}
	return i;
}

void quick_sort(Array & a, int start, int end) {
	if( start >= end ) {
		return;
	}
	const int i = select_pivot(start, end);
	const int pivot = partition(a, i, start, end);
	if(start < pivot){
		quick_sort(a, start, pivot-1);
	}
	if(pivot < end){
		quick_sort(a, pivot, end);
	}
}


SCENARIO("Sort array by quick_sort", "[quick_sort]"){
	GIVEN("One array with unique values"){
		Array a {3, 2, 1};
		Array va {1, 2, 3};

		quick_sort(a, 0, a.size()-1);
		REQUIRE(std::equal(a.begin(), a.end(), va.begin()));
	}

	GIVEN("One array with duplicates"){
		Array a {3, 3, 1, 1, 2, 9, 10, 11, 1, 11};
		Array va {1, 1, 1, 2, 3, 3, 9, 10, 11, 11};

		quick_sort(a, 0, a.size()-1);
		REQUIRE(std::equal(a.begin(), a.end(), va.begin()));
	}
}