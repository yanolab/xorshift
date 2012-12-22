#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define MAXPATHSIZE 256

static unsigned long w = 123456789;

void initseed(unsigned long value) {
  w = value;
}

unsigned long xor128() {
  static unsigned long x = 123456789;
  static unsigned long y = 362436069;
  static unsigned long z = 521288629;
  //static unsigned long w = 88675123;

  unsigned long t;

  t = x ^ (x << 11);
  x = y; y = z; z = w;
  return w = (w ^ (w >> 19)) ^ (t ^ (t >> 8));
}

void fillrandom(char *buffer, size_t bufferSize) {
  for (size_t index = 0; index < bufferSize; index++)
    *(buffer + index) = (char)xor128();
}

int main(int argc, char *argv[]) {
  if (argc != 4) {
    printf("xorshift OUTFILE BLOCKSIZE COUNT");
    exit(1);
  }

  initseed((unsigned long)time(NULL));

  size_t blockSize = atol(argv[2]);
  uint64_t blockCount = atol(argv[3]);

  char *buffer = (char *)malloc(sizeof(char) * blockSize);
  FILE *fout;

  if ((fout = fopen(argv[1], "w")) == NULL) {
    printf("cannot open file: %s, so skipped.", argv[1]);
    exit(1);
  }

  for (uint64_t noOfBlock = 0; noOfBlock < blockCount; noOfBlock++) {
    fillrandom(buffer, blockSize);
    fwrite(buffer, blockSize, 1, fout);
    fflush(fout);
  }

  free(buffer);

  fclose(fout);

  return 0;
}
