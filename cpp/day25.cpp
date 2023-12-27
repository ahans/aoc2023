#include <cstdint>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <chrono>

int main() {
    auto const begin = std::chrono::high_resolution_clock::now();

    auto const str2num = [] (auto const& s) -> uint16_t {
        return (s[0] - 'a') * 26*26 + (s[1] - 'a') * 26 + (s[2] - 'a');
    };
    std::vector<std::vector<uint16_t>> graph(26*26*26);
    std::unordered_set<uint16_t> s;

    while (!std::cin.eof()) {
        std::string line;
        std::getline(std::cin, line);
        auto const num_dst = line.length() / 4 - 1;
        auto const src = str2num(line.substr(0, 3));
        auto& dsts = graph[src];
        s.insert(src);
        for (auto i = 0; i < num_dst; ++i) {
            auto const dst = str2num(line.substr(5 + i * 4, 3));
            dsts.push_back(dst);
            graph[dst].push_back(src);
            s.insert(dst);
        }
    }

    auto const num_nodes = s.size();
    std::cout << "num_nodes " << num_nodes << std::endl;

    while (true) {
        int32_t max_connections{-1};
        uint16_t max_connections_node{};
        uint32_t connection_sum{};
        for (auto const u : s) {
            int32_t num_connections{0};
            for (auto v : graph[u]) {
                if (s.count(v) == 0) {
                    num_connections += 1;
                }
            }
            connection_sum += num_connections;
            if (num_connections > max_connections) {
                max_connections = num_connections;
                max_connections_node = u;
            }
        }
        if (connection_sum == 3) {
            std::cout << (num_nodes - s.size()) * s.size() << std::endl;
            break;
        }
        s.erase(max_connections_node);
    }

    std::cout << (std::chrono::high_resolution_clock::now() - begin).count() / 1e6 << " ms\n";
}