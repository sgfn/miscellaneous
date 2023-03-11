CXXC=g++
CXXFLAGS=--std=c++11 -Wall -Wextra -pedantic
OFLAG=-O2
LDFLAGS=-larmadillo

all:
	make heateq

heateq: heateq.cc
	$(CXXC) $(CXXFLAGS) $(OFLAG) -o heateq heateq.cc $(LDFLAGS)

clean:
	rm -f ./heateq
