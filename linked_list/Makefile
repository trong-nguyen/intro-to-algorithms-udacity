CC = g++
CFLAGS = -I. -std=c++11 -O3
HEADERS = linked_list.h
SOURCES = linked_list.cpp test.cpp
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = test.exe

default: $(EXECUTABLE)

%.o: %.cpp $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@

.PHONY: clean

clean:
	rm $(OBJECTS) $(EXECUTABLE)

test: $(EXECUTABLE)
	./$(EXECUTABLE)