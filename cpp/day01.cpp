#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <ranges>
#include <string_view>
#include <string>
#include <vector>
#include <numeric>

int main()
{
    std::ifstream file{"../inputs/01.txt"};
    std::string input{std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>()};

    auto const begin = std::chrono::high_resolution_clock::now();

    auto const process_part1 = [](auto const line) {
        constexpr auto not_digit = [](char c) {
            return !std::isdigit(c);
        };
        auto const first = *(line | std::views::drop_while(not_digit)).begin() - '0';
        auto const last = *(line | std::views::reverse | std::views::drop_while(not_digit)).begin() - '0';
        return first * 10 + last;
    };

    constexpr std::array digits = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

    auto const find_first_digit = [&](auto sv) -> uint32_t {
        while (true) {
            if (std::isdigit(sv[0])) return sv[0] - '0';
#pragma GCC unroll 10
            for (auto i{0U}; i < digits.size(); ++i) {
                if (sv.starts_with(digits[i])) return i + 1;
            }
            sv = sv.substr(1);
        }
        __builtin_unreachable();
    };

    auto const find_last_digit = [&](auto sv) -> uint32_t {
        while (true) {
            if (std::isdigit(sv.back())) return sv.back() - '0';
#pragma GCC unroll 10
            for (auto i{0U}; i < digits.size(); ++i) {
                if (sv.ends_with(digits[i])) return i + 1;
            }
            sv = sv.substr(0, sv.length() - 1);
        }
        __builtin_unreachable();
    };

    auto process_part2 = [&](auto const line) {
        auto const first = find_first_digit(line);
        auto const last = find_last_digit(line);
        return first * 10 + last;
    };

    auto line_ranges = std::views::split(input, '\n');

    auto const [p1, p2] = std::accumulate(
        line_ranges.begin(), line_ranges.end(), std::make_pair(0U, 0U), [&](auto acc, auto const& line_range) {
            if (line_range.size() > 0) {
                acc.first += process_part1(line_range);
                acc.second += process_part2(std::string_view{line_range});
            }
            return acc;
        });

    auto const end = std::chrono::high_resolution_clock::now();

    std::cout << p1 << std::endl;
    std::cout << p2 << std::endl;

    std::cout << "runtime: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() << " µs\n";
}
