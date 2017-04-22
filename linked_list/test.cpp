#define CATCH_CONFIG_MAIN
#include <stdexcept>
#include "../include/catch.hpp"
#include "linked_list.h"

SCENARIO("Creating and modifying lists", "[linked_list]"){
	GIVEN("A linked_list"){
		LinkedList list;

		REQUIRE(list.size() == 0);
		REQUIRE(list.begin() == 0);

		WHEN("adding items"){
			list.add(5);
			list.add(1);
			list.add(4);
			list.add(3);
			list.add(1);
			list.add(9);

			THEN("size and iterator should be changed"){
				REQUIRE(list.size() == 6);
				REQUIRE(list.begin() != 0);
				REQUIRE(list.begin()->data == 9);
			}


			WHEN("poping"){
				REQUIRE(list.pop() == 9);
				REQUIRE(list.pop() == 1);

				THEN("size should be reduced"){
					REQUIRE(list.size() == 4);
					REQUIRE(list.begin() != 0);
					REQUIRE(list.begin()->data == 3);
				}

				REQUIRE(list.pop() == 3);
				REQUIRE(list.pop() == 4);
				REQUIRE(list.pop() == 1);
				REQUIRE(list.pop() == 5);

				THEN("size should be nulled now"){
					REQUIRE(list.size() == 0);
					REQUIRE(list.begin() == 0);
				}

				THEN("should throw when poping empty"){
					REQUIRE_THROWS_WITH(list.pop(), Catch::Contains("pop empty list"));
				}
			}
		}
	}
}