#define CATCH_CONFIG_MAIN
#include <list>
#include <algorithm>
#include <iterator>
#include "../include/catch.hpp"

#include <iostream>

typedef std::list<int> Array;
typedef Array::iterator Iterator;

void merge_sorted(Iterator p1_start, Iterator p1_end, Iterator p2_start, Iterator p2_end, Array & array) {
	Iterator p1=p1_start, p2=p2_start;
	while(p1 != p1_end and p2 != p2_end){
		Iterator p;
		if(p1 == p1_end){
			p = p2++;
		}else if(p2 == p2_end){
			p = p1++;
		}else{
			p = (*p2 > *p1) ? p1++ : p2++;
		}
		array.push_back(*p);
	}
}

SCENARIO("Merging two arrays", "[merge_sorted]"){
	GIVEN("Two arrays"){
		Array a1 {1, 3, 9, 11};
		Array a2 {2, 4, 5};
		Array ma;
		Array va {1, 2, 3, 4, 5, 9, 11};

		merge_sorted(a1.begin(), a1.end(), a2.begin(), a2.end(), ma);

		REQUIRE(std::equal(ma.begin(), ma.end(), va.begin()));
	}
}