#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>

int is_one(char const* s) {
    return 1 * (s[0] == 'o' && s[1] == 'n' && s[2] == 'e');
}

int is_two(char const* s) {
    return 2 * (s[0] == 't' && s[1] == 'w' && s[2] == 'o');
}
int is_three(char const* s) {
    return 3 * (s[0] == 't' && s[1] == 'h' && s[2] == 'r' && s[3] == 'e' && s[4] == 'e');
}
int is_four(char const* s) {
    return 4 * (s[0] == 'f' && s[1] == 'o' && s[2] == 'u' && s[3] == 'r');
}
int is_five(char const* s) {
    return 5 * (s[0] == 'f' && s[1] == 'i' && s[2] == 'v' && s[3] == 'e');
}
int is_six(char const* s) {
    return 6 * (s[0] == 's' && s[1] == 'i' && s[2] == 'x');
}
int is_seven(char const* s) {
    return 7 * (s[0] == 's' && s[1] == 'e' && s[2] == 'v' && s[3] == 'e' && s[4] == 'n');
}
int is_eight(char const* s) {
    return 8 * (s[0] == 'e' && s[1] == 'i' && s[2] == 'g' && s[3] == 'h' && s[4] == 't');
}
int is_nine(char const* s) {
    return 9 * (s[0] == 'n' && s[1] == 'i' && s[2] == 'n' && s[3] == 'e');
}


int parse_digit(char const* s) {
    return is_one(s) + is_two(s) + is_three(s) + is_four(s) + is_five(s) + is_six(s) + is_seven(s) + is_eight(s) + is_nine(s);
}

int main() {
    struct timespec  ts;

    char buffer[32*1024];
    char* c;
    size_t num_chars;
    char line[50];
    int i;
    int fst, lst;
    int fst_p2, lst_p2;
    int tmp;
    int p1, p2;
    int64_t begin;

    num_chars = read(STDIN_FILENO, buffer, 32 * 1024);

    clock_gettime(CLOCK_REALTIME, &ts);
    begin = ts.tv_sec * 1000000000 + ts.tv_nsec;

    // one
    // two
    // three
    // four five six seven eight nine
    
    p1 = 0;
    p2 = 0;
    fst = 0;
    fst_p2 = 0;
    lst = 0;
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
            p2 += fst_p2 * 10 + lst_p2;
            fst_p2 = 0;
        } else {
            tmp = parse_digit(c);
            if (tmp < 0 || tmp > 9) printf("error! %d\n", tmp);
            if (tmp > 0) {
                lst_p2 = tmp;
                if (fst_p2 == 0) fst_p2 = lst_p2;
            }
        }
    }

    printf("%d\n", p1);
    printf("%d\n", p2);

    clock_gettime(CLOCK_REALTIME, &ts);
    printf("runtime: %lld\n", ((ts.tv_sec * 1000000000 + ts.tv_nsec) - begin) / 1000);
}