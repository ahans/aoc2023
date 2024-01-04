#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string_view>
#include <string>
#include <vector>

class Input
{
public:
    Input(std::string const& input_file)
    {
        std::ifstream file{input_file};
        buf_ = std::string{std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>()};
        buf_view_ = static_cast<std::string_view>(buf_);
    }

    std::vector<std::string_view> splitlines() const
    {
        std::vector<std::string_view> lines;
        lines.reserve(1000);
        size_t begin{};
        while (begin < buf_view_.length()) {
            auto const next_newline = buf_view_.find('\n', begin);
            if (next_newline == std::string::npos) {
                break;
            }
            lines.push_back(buf_view_.substr(begin, next_newline - begin));
            begin = next_newline + 1;
        }
        return lines;
    }

private:
    std::string buf_;
    std::string_view buf_view_;
};

constexpr std::array digits = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

uint32_t parse_first_digit(std::string_view const sv)
{
    if (std::isdigit(sv[0])) return sv[0] - '0';
#pragma GCC unroll 10
    for (auto i = 0U; i < digits.size(); ++i) {
        if (sv.starts_with(digits[i])) return i + 1;
    }
    return 0;
}

uint32_t parse_last_digit(std::string_view const sv)
{
    if (std::isdigit(sv[sv.size() - 1])) return sv[sv.size() - 1] - '0';
#pragma GCC unroll 10
    for (auto i = 0U; i < digits.size(); ++i) {
        if (sv.ends_with(digits[i])) return i + 1;
    }
    return 0;
}

int main()
{
    Input input{"../inputs/01.txt"};

    auto const begin = std::chrono::high_resolution_clock::now();

    auto process_part1 = [](auto const line) {
        uint32_t first{0};
        for (auto it = line.begin(); it < line.end(); ++it) {
            if (std::isdigit(*it)) {
                first = *it - '0';
                break;
            }
        }

        uint32_t last{0};
        for (auto it = line.rbegin(); it < line.rend(); ++it) {
            if (std::isdigit(*it)) {
                last = *it - '0';
                break;
            }
        }
        return first * 10 + last;
    };

    auto process_part2 = [](auto const line) {
        uint32_t first{0};
        auto l = line;
        while (first == 0) {
            first = parse_first_digit(l);
            l = l.substr(1);
        }

        uint32_t last{0};
        l = line;
        while (last == 0) {
            last = parse_last_digit(l);
            l = l.substr(0, l.length() - 1);
        }
        return first * 10 + last;
    };

    uint32_t p1{};
    uint32_t p2{};
    for (auto const line : input.splitlines()) {
        p1 += process_part1(line);
        p2 += process_part2(line);
    }

    auto const end = std::chrono::high_resolution_clock::now();

    std::cout << p1 << std::endl;
    std::cout << p2 << std::endl;

    std::cout << "runtime: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() << " µs\n";
}
