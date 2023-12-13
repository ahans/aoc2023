#include <chrono>
#include <iostream>
#include <string>
#include <vector>

int main()
{
    auto const begin = std::chrono::high_resolution_clock::now();
    std::string line;
    std::vector<uint32_t> rows;
    rows.reserve(32);
    std::vector<uint32_t> cols;
    cols.reserve(32);
    uint32_t p1{};
    uint32_t p2{};
    while (!std::cin.eof()) {
        std::getline(std::cin, line);
        if (line == "") {
            auto const process = [&](auto const& cols_or_rows, auto const factor) {
                for (auto m = 0; m < cols_or_rows.size() - 1; ++m) {
                    uint32_t diffs{};
                    for (auto c0 = m, c1 = m + 1; c0 >= 0 && c1 < cols_or_rows.size(); --c0, ++c1) {
                        diffs += __builtin_popcount(cols_or_rows[c0] ^ cols_or_rows[c1]);
                    }
                    p1 += (diffs == 0) * (m + 1) * factor;
                    p2 += (diffs == 1) * (m + 1) * factor;
                }
            };
            process(rows, 100);
            process(cols, 1);
            rows.clear();
            cols.clear();
        } else {
            if (cols.size() == 0) {
                cols.resize(line.length());
            }
            uint32_t row{};
            auto const j = rows.size();
            for (auto i = 0; i < line.length(); ++i) {
                auto const cond = line[i] == '#';
                row |= cond * (1 << i);
                cols[i] |= cond * (1 << j);
            }
            rows.push_back(row);
        }
    }
    std::cout << p1 << std::endl;
    std::cout << p2 << std::endl;
    auto const end = std::chrono::high_resolution_clock::now();
    std::cout << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() << " µs" << std::endl;
}