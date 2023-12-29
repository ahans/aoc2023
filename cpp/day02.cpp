#include <fstream>
#include <chrono>

template <int max_size>
class InputBuffer {
public:
    InputBuffer(char const* f) {
        FILE* file = fopen(f, "rt");
        fseek(file, 0L, SEEK_END);
        num_chars_ = ftell(file);
        fseek(file, 0L, SEEK_SET);
        fread(buffer_, 1, num_chars_, file);
        fclose(file);
        cur_ = buffer_;
    }

    int size() const {
        return num_chars_;
    }

    char const* cur() const {
        return cur_;
    }

    void advance(int s) {
        cur_ += s;
    }

    bool exhausted() const {
        bool ex = cur_ >= buffer_ + num_chars_;
        return ex;
    }

    int find_next(char c) {
        int offset = 0;
        while (*(cur_ + offset) != c) {
            ++offset;
            if (cur_ + offset >= buffer_ + num_chars_) {
                return -1;
            }
        }

        return offset;
    }

private:
    char buffer_[max_size];
    char* cur_;
    int num_chars_;
};

struct Rgb {
    Rgb() {}
    Rgb (int init) {
        r = init;
        g = init;
        b = init;
    }

    int r;
    int g;
    int b;
};

int main() {
    auto begin = std::chrono::high_resolution_clock::now();
    InputBuffer<16384> buffer("../inputs/02.txt");
    int i = 0;
    int id = 1;
    int p1 = 0;
    int p2 = 0;
    Rgb max(0);
    while (!buffer.exhausted()) {
        int i = buffer.find_next(':');
        buffer.advance(i + 2);
        for (;;) {
            int n = 0;

            while (*buffer.cur() != ' ') {
                n = 10 * n + (*buffer.cur() - '0');
                buffer.advance(1);
            }
            buffer.advance(1);
            switch (*buffer.cur()) {
                case 'r':
                    if (n > max.r) max.r = n;
                    break;
                case 'g':
                    if (n > max.g) max.g = n;
                    break;
                case 'b':
                    if (n > max.b) max.b = n;
            }
            int next_space = buffer.find_next(' ');
            int next_newline = buffer.find_next('\n');
            if (next_space != -1 && next_newline != -1) {
                if (next_newline < next_space) {
                    buffer.advance(next_newline + 1);
                    break;
                } else {
                    buffer.advance(next_space + 1);
                }
            } else if (next_newline != -1) {
                buffer.advance(next_newline + 1);
                break;
            }
        }

        if (max.r <= 12 && max.g <= 13 && max.b <= 14) {
            p1 += id;
        }
        p2 += max.r * max.g * max.b;
        max = Rgb(0);

        id += 1;
    }

    printf("p1: %d\n", p1);
    printf("p2: %d\n", p2);

    auto const end = std::chrono::high_resolution_clock::now();
    printf("%lld\n", (end - begin).count());
}
