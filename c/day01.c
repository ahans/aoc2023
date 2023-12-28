#include <stdio.h>
#include <stdlib.h>

int digitcmp(char const* a, char const* b, int n)
{
    int i;
    for (i = 0; i < n; ++i) {
        if (a[i] != b[i]) return 0;
    }
    return 1;
}

int parse_digit(char const* str) {
    if (digitcmp(str, "one", 3)) return 1;
    if (digitcmp(str, "two", 3)) return 2;
    if (digitcmp(str, "three", 5)) return 3;
    if (digitcmp(str, "four", 4)) return 4;
    if (digitcmp(str, "five", 4)) return 5;
    if (digitcmp(str, "six", 3)) return 6;
    if (digitcmp(str, "seven", 5)) return 7;
    if (digitcmp(str, "eight", 5)) return 8;
    if (digitcmp(str, "nine", 4)) return 9;
    return 0;
}

int main() {
    char* c;
    size_t num_chars;
    int i;
    int fst, lst;
    int fst_p2, lst_p2;
    int tmp;
    int p1, p2;

    char buffer[32768];

    num_chars = read(0, buffer, sizeof(buffer));

    p1 = 0;
    p2 = 0;
    fst = 0;
    lst = 0;
    fst_p2 = 0;
    lst_p2 = 0;

    for (c = buffer; c < buffer + num_chars; ++c) {
	if ('1' <= *c && *c <= '9') {
	    lst = *c - '0';
	    lst_p2 = lst;
	    if (fst == 0) fst = lst;
	    if (fst_p2 == 0) fst_p2 = lst;
	} else if (*c == '\n') {
	    p1 += fst * 10 + lst;
	    fst = 0;
	    lst = 0;
	    p2 += fst_p2 * 10 + lst_p2;
	    fst_p2 = 0;
	    lst_p2 = 0;
	} else {
	    tmp = parse_digit(c);
	    if (tmp > 0) {
		lst_p2 = tmp;
		if (fst_p2 == 0) fst_p2 = lst_p2;
	    }
	}
    }
    printf("%d\n", p1);
    printf("%d\n", p2);

    return 0;
}
