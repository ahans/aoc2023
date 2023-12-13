#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>
#include <vector>

struct Mapping
{
    int64_t src, dst, len;
};

[[nodiscard]] std::optional<std::pair<int64_t, int64_t>> overlap(int64_t b0, int64_t len0, int64_t b1, int64_t len1)
{
    if (b0 > b1) {
        std::swap(b0, b1);
        std::swap(len0, len1);
    }
    auto const b = std::max(b0, b1);
    auto const e = std::min(b0 + len0, b1 + len1);
    if (e > b) {
        auto pair = std::make_pair(b, e - b);
        return {pair};
    }
    return {};
}

using Stages = std::vector<std::vector<Mapping>>;

[[nodiscard]] int64_t expand_range(Stages const& stages, int64_t begin, int64_t const len, size_t const stage_id)
{
    if (stage_id == stages.size()) {
        return begin;
    }
    int64_t min = std::numeric_limits<int64_t>::max();
    std::vector<std::pair<int64_t, int64_t>> match_ranges;
    for (auto const& mapping : stages[stage_id]) {
        auto maybe_overlap = overlap(begin, len, mapping.src, mapping.len);
        if (maybe_overlap.has_value()) {
            auto [overlap_begin, overlap_len] = maybe_overlap.value();
            match_ranges.push_back(maybe_overlap.value());
            overlap_begin += mapping.dst - mapping.src;
            auto loc = expand_range(stages, overlap_begin, overlap_len, stage_id + 1);
            if (loc < min) {
                min = loc;
            }
        }
    }
    if (match_ranges.empty()) {
        return expand_range(stages, begin, len, stage_id + 1);
    }

    for (auto const [match_x, match_len] : match_ranges) {
        if (begin < match_x) {
            auto const loc = expand_range(stages, begin, match_x - begin, stage_id + 1);
            if (loc < min) {
                min = loc;
            }
        }
        begin = match_x + match_len;
    }
    return min;
}

int main()
{
    auto begin = std::chrono::high_resolution_clock::now();
    std::vector<int64_t> seeds;
    std::ifstream f{"../inputs/05.txt"};
    Stages stages{7};

    std::string line;
    std::getline(f, line);
    line = line.substr(7);
    std::istringstream iss(line);
    int64_t i;
    while (iss >> i) {
        seeds.push_back(i);
    }
    std::getline(f, line);

    for (auto map_id = 0; map_id < 7; ++map_id) {
        auto& stage = stages.at(map_id);
        std::getline(f, line);
        while (!f.eof()) {
            std::getline(f, line);
            if (line.length() < 5) break;
            std::istringstream iss(line);
            int64_t dst, src, len;
            iss >> dst >> src >> len;
            stage.push_back(Mapping{src, dst, len});
        }
        std::sort(stage.begin(), stage.end(), [](auto const& a, auto const& b) { return a.src < b.src; });
    }

    {
        int64_t min = std::numeric_limits<int64_t>::max();
        for (auto s : seeds) {
            auto loc = expand_range(stages, s, 1, 0);
            if (loc < min) min = loc;
        }
        std::cout << min << '\n';
    }

    {
        int64_t min = std::numeric_limits<int64_t>::max();
        for (auto i = 0; i < seeds.size(); i += 2) {
            auto loc = expand_range(stages, seeds[i], seeds[i + 1], 0);
            if (loc < min) min = loc;
        }
        std::cout << min << '\n';
    }
    std::cout << (std::chrono::high_resolution_clock::now() - begin).count() << " ns\n";
}