#include <boost/container/static_vector.hpp>

#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <ranges>
#include <tuple>
#include <vector>

struct Grid
{
    Grid(std::string const& input)
    {
        auto line_ranges = std::views::split(input, '\n');
        width = line_ranges.front().size();
        height = width;
        grid_.reserve(width * height);
        for (auto const& line_range : line_ranges) {
            std::ranges::transform(line_range, std::back_inserter(grid_), [](char const c) { return c - '0'; });
        }
        if (grid_.size() != width * height) {
            throw std::runtime_error("unexpected size of input grid");
        }
    }

    [[nodiscard]] uint8_t operator[](size_t index) const
    {
        return grid_[index];
    }

    uint32_t width, height;
    std::vector<uint8_t> grid_;
};

template <auto L, auto U>
[[nodiscard]] uint32_t dijkstra(Grid const& grid)
{
    using Tuple = std::tuple<uint16_t, uint16_t, uint8_t>;
    std::array<boost::container::static_vector<Tuple, 1000>, 128> todo;
    std::vector<std::array<uint16_t, 2>> cost(grid.width * grid.height, {64000, 64000});
    cost[0] = {0, 0};

    auto const width = grid.width;
    auto const height = grid.height;

    auto index = 0;

    todo[0].push_back({0, 0, 0});
    todo[0].push_back({0, 0, 1});

    while (true) {
        while (todo[index % 128].size() > 0) {
            auto const [x, y, direction] = todo[index % 128].back();
            todo[index % 128].pop_back();

            // Retrieve cost for our current location and direction.
            auto index = width * y + x;
            auto steps = cost[index][direction];

            // Check if we've reached the end.
            if (x == width - 1 && y == height - 1) {
                return steps;
            }

            if (direction == 0) {
                // We just moved vertically so now check both left and right directions.

                // Left
                {
                    auto index2 = index;
                    auto steps2 = steps;

                    // Each direction loop is the same:
                    // * Check to see if we gone out of bounds
                    // * Increase the cost by the "heat" of the square we've just moved into.
                    // * Check if we've already been to this location with a lower cost.
                    // * Add new state to priority queue.
                    for (auto i = 1; i <= U; ++i) {
                        if (i > x) {
                            break;
                        }

                        index2 -= 1;
                        steps2 += grid[index2];

                        if (i >= L && (steps2 < cost[index2][1])) {
                            todo[steps2 % 128].push_back({x - i, y, 1});
                            cost[index2][1] = steps2;
                        }
                    }
                }

                // Right
                {
                    auto index2 = index;
                    auto steps2 = steps;

                    for (auto i = 1; i <= U; ++i) {
                        if (x + i >= width) {
                            break;
                        }

                        index2 += 1;

                        steps2 += grid[index2];

                        if (i >= L && (steps2 < cost[index2][1])) {
                            todo[steps2 % 128].push_back({x + i, y, 1});
                            cost[index2][1] = steps2;
                        }
                    }
                }
            } else {
                // We just moved horizontally so now check both up and down directions.

                // Up
                {
                    auto index2 = index;
                    auto steps2 = steps;

                    for (auto i = 1; i <= U; ++i) {
                        if (i > y) {
                            break;
                        }

                        index2 -= width;

                        steps2 += grid[index2];

                        if (i >= L && (steps2 < cost[index2][0])) {
                            todo[steps2 % 128].push_back({x, y - i, 0});
                            cost[index2][0] = steps2;
                        }
                    }
                }

                // Down
                {
                    auto index2 = index;
                    auto steps2 = steps;

                    for (auto i = 1; i <= U; ++i) {
                        if (y + i >= height) {
                            break;
                        }

                        index2 += width;
                        steps2 += grid[index2];

                        if (i >= L && (steps2 < cost[index2][0])) {
                            todo[steps2 % 128].push_back({x, y + i, 0});
                            cost[index2][0] = steps2;
                        }
                    }
                }
            }
        }

        index += 1;
    }
    __builtin_unreachable();
}

int main()
{
    std::ifstream file{"../inputs/17.txt"};
    std::string input{std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>()};

    auto const begin = std::chrono::high_resolution_clock::now();
    Grid const grid{input};

    auto p1 = dijkstra<1, 3>(grid);
    auto p2 = dijkstra<4, 10>(grid);

    auto const end = std::chrono::high_resolution_clock::now();

    std::cout << p1 << std::endl;
    std::cout << p2 << std::endl;
    std::cout << "runtime: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() << " µs\n";
}
