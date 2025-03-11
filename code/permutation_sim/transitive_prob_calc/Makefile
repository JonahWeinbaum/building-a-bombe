.PHONY: all clean
all: transitive

clean:
	rm -f transitive

transitive: transitive.cpp
	g++ -Wno-stringop-overread -O3 -std=c++20 $^ -o $@
