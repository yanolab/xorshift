all: xorshift.o
	gcc -o xorshift xorshift.o

xorshift.o: xorshift.c
	gcc -c xorshift.c --std=gnu99 -O3

clean:
	rm *.o xorshift
