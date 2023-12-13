#include <chrono>
#include <iostream>
#include <string>
#include <vector>

int main()
{
    auto const begin{std::chrono::high_resolution_clock::now()};

    std::string line;
    std::vector<uint32_t> rows;
    std::vector<uint32_t> cols;
    uint32_t p1{};
    uint32_t p2{};
    while (!std::cin.eof()) {
        std::getline(std::cin, line);
        if (line == "") {
            auto const process = [&](auto const& cols_or_rows, auto const factor) {
                for (auto m{0}; m < cols_or_rows.size() - 1; ++m) {
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
            auto const j{rows.size()};
            for (auto i{0U}; i < line.length(); ++i) {
                uint32_t const cond = line[i] == '#';
                row |= cond << i;
                cols[i] |= cond << j;
            }
            rows.push_back(row);
        }
    }
    std::cout << p1 << std::endl;
    std::cout << p2 << std::endl;

    auto const end{std::chrono::high_resolution_clock::now()};
    std::cout << (end - begin).count() << " ns\n";
}
