CXX = g++
CCFLAGS = -std=c++11 -O3
SOURCES = quick_sort.cpp
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = tester

%.o: %.cpp
	$(CXX) $(CCFLAGS) -c $< -o $@

$(EXECUTABLE): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $@

clean:
	rm $(OBJECTS) $(EXECUTABLE)

test: $(EXECUTABLE)
	./$(EXECUTABLE)