#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include <ctime>
#include <numeric>  
#include <unordered_map>
#include <any>
#include <chrono>
#include <stdexcept>
#include <sstream>
#include "json.hpp"

class Cube {
public:
    static double stdfactor;
    int dimension;
    std::vector<std::vector<std::vector<int>>> cube;

    Cube(int dimension) : dimension(dimension), cube(dimension, std::vector<std::vector<int>>(dimension, std::vector<int>(dimension, 0))) {}

    void initialize() {
        std::vector<int> numbers(dimension * dimension * dimension);
        for (int i = 0; i < dimension * dimension * dimension; ++i)
            numbers[i] = i + 1;

        std::shuffle(numbers.begin(), numbers.end(), std::default_random_engine(static_cast<unsigned>(time(0))));
        int index = 0;
        for (int i = 0; i < dimension; ++i) {
            for (int j = 0; j < dimension; ++j) {
                for (int k = 0; k < dimension; ++k) {
                    cube[i][j][k] = numbers[index++];
                }
            }
        }
    }

    std::vector<int> rowSums() const {
        std::vector<int> results;
        for (int z = 0; z < dimension; ++z) {
            for (int y = 0; y < dimension; ++y) {
                int sum = 0;
                for (int x = 0; x < dimension; ++x)
                    sum += cube[z][y][x];
                results.push_back(sum);
            }
        }
        return results;
    }

    std::vector<int> columnSums() const {
        std::vector<int> results;
        for (int z = 0; z < dimension; ++z) {
            for (int x = 0; x < dimension; ++x) {
                int sum = 0;
                for (int y = 0; y < dimension; ++y) {
                    sum += cube[z][y][x];
                }
                results.push_back(sum);
            }
        }
        return results;
    }

    std::vector<int> pillarSums() const {
        std::vector<int> results;
        for (int y = 0; y < dimension; ++y) {
            for (int x = 0; x < dimension; ++x) {
                int sum = 0;
                for (int z = 0; z < dimension; ++z) {
                    sum += cube[z][y][x];
                }
                results.push_back(sum);
            }
        }
        return results;
    }

    std::vector<int> spatialDiagonalSums() const {
        std::vector<int> diagonalSums(4, 0);
        for (int i = 0; i < dimension; ++i) {
            diagonalSums[0] += cube[i][i][i];
            diagonalSums[1] += cube[i][dimension - 1 - i][i];
            diagonalSums[2] += cube[i][i][dimension - 1 - i];
            diagonalSums[3] += cube[i][dimension - 1 - i][dimension - 1 - i];
        }
        return diagonalSums;
    }

    std::vector<int> xyIntersectionDiagonalSums() const {
        std::vector<int> diagonal_sums;
        for (int z = 0; z < dimension; ++z) {
            int diagonal1 = 0, diagonal2 = 0;
            for (int i = 0; i < dimension; ++i) {
                diagonal1 += cube[z][i][i];
                diagonal2 += cube[z][i][dimension - 1 - i];
            }
            diagonal_sums.push_back(diagonal1);
            diagonal_sums.push_back(diagonal2);
        }
        return diagonal_sums;
    }

    std::vector<int> xzIntersectionDiagonalSums() const {
        std::vector<int> diagonal_sums;
        for (int y = 0; y < dimension; ++y) {
            int diagonal1 = 0, diagonal2 = 0;
            for (int i = 0; i < dimension; ++i) {
                diagonal1 += cube[i][y][i];
                diagonal2 += cube[i][y][dimension - 1 - i];
            }
            diagonal_sums.push_back(diagonal1);
            diagonal_sums.push_back(diagonal2);
        }
        return diagonal_sums;
    }

    std::vector<int> yzIntersectionDiagonalSums() const {
        std::vector<int> diagonal_sums;
        for (int x = 0; x < dimension; ++x) {
            int diagonal1 = 0, diagonal2 = 0;
            for (int i = 0; i < dimension; ++i) {
                diagonal1 += cube[i][i][x];
                diagonal2 += cube[i][dimension - 1 - i][x];
            }
            diagonal_sums.push_back(diagonal1);
            diagonal_sums.push_back(diagonal2);
        }
        return diagonal_sums;
    }

    static std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>> allCoordinatePairs(int dimension) {
        std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>> coordinate_pairs;
        std::vector<std::tuple<int, int, int>> coordinates;

        for (int i = 0; i < dimension; ++i) {
            for (int j = 0; j < dimension; ++j) {
                for (int k = 0; k < dimension; ++k) {
                    coordinates.emplace_back(i, j, k);
                }
            }
        }

        for (size_t i = 0; i < coordinates.size(); ++i) {
            for (size_t j = i + 1; j < coordinates.size(); ++j) {
                coordinate_pairs.emplace_back(coordinates[i], coordinates[j]);
            }
        }

        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(coordinate_pairs.begin(), coordinate_pairs.end(), g);

        return coordinate_pairs;
    }

    std::vector<int> allSums() const {
        std::vector<int> all_sums;

        auto row_sums = rowSums();
        all_sums.insert(all_sums.end(), row_sums.begin(), row_sums.end());

        auto column_sums = columnSums();
        all_sums.insert(all_sums.end(), column_sums.begin(), column_sums.end());

        auto pillar_sums = pillarSums();
        all_sums.insert(all_sums.end(), pillar_sums.begin(), pillar_sums.end());

        auto xy_diagonal_sums = xyIntersectionDiagonalSums();
        all_sums.insert(all_sums.end(), xy_diagonal_sums.begin(), xy_diagonal_sums.end());

        auto xz_diagonal_sums = xzIntersectionDiagonalSums();
        all_sums.insert(all_sums.end(), xz_diagonal_sums.begin(), xz_diagonal_sums.end());

        auto yz_diagonal_sums = yzIntersectionDiagonalSums();
        all_sums.insert(all_sums.end(), yz_diagonal_sums.begin(), yz_diagonal_sums.end());

        return all_sums;
    }

    double calculateStandardDeviation(const std::vector<int>& sums) const {
        double mean = std::accumulate(sums.begin(), sums.end(), 0.0) / sums.size();
        double variance = 0;
        for (int sum : sums)
            variance += (sum - mean) * (sum - mean);
        variance /= sums.size();
        return std::sqrt(variance);
    }

    double getH() const {
        std::vector<int> sums = allSums();

        double target = dimension * (std::pow(dimension, 3) + 1) / 2;
        double stddev = calculateStandardDeviation(sums);

        int n = std::count(sums.begin(), sums.end(), static_cast<int>(target));

        return n - stddev * stdfactor;
    }

    double controlH() const {
        std::vector<int> sums = allSums();

        double target = dimension * (std::pow(dimension, 3) + 1) / 2;

        int n = 0;
        double e = 0.0;
        for (int sum : sums) {
            if (sum == static_cast<int>(target)) {
                ++n;
            }
            e += std::abs(target - sum);
        }

        e /= 32700.0;

        return n + e;
    }

    static Cube copyCube(const Cube& source) {
        Cube copy(source.dimension);
        copy.cube = source.cube;
        return copy;
    }

    std::pair<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>, double> findSteepestAscent() {
        Cube dummy_cube = copyCube(*this);
        auto coordinatePairs = allCoordinatePairs(dimension);

        std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>> maxCoordPairs;
        double maxH = -2000;

        for (const auto& [coord1, coord2] : coordinatePairs) {
            auto [x1, y1, z1] = coord1;
            auto [x2, y2, z2] = coord2;

            std::swap(dummy_cube.cube[z1][y1][x1], dummy_cube.cube[z2][y2][x2]);

            double currentH = dummy_cube.getH();

            if (currentH > maxH) {
                maxH = currentH;
                maxCoordPairs = {coord1, coord2};
            }

            std::swap(dummy_cube.cube[z1][y1][x1], dummy_cube.cube[z2][y2][x2]);
        }

        return {maxCoordPairs, maxH};
    }

    std::unordered_map<std::string, std::any> steepestAscentHillClimb() {
        initialize();
        std::unordered_map<std::string, std::any> result;
        result["initial_state"] = copyCube(*this).cube;
        result["switches"] = std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>();
        result["h_values"] = std::vector<double>();

        auto& h_values = std::any_cast<std::vector<double>&>(result["h_values"]);
        auto& switches = std::any_cast<std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>&>(result["switches"]);

        bool done = false;
        while (!done) {
            double currentH = getH();
            h_values.push_back(currentH);
            auto [pair, newH] = findSteepestAscent();

            if (newH > currentH) {
                auto [coord1, coord2] = pair;
                auto [x1, y1, z1] = coord1;
                auto [x2, y2, z2] = coord2;
                std::swap(cube[z1][y1][x1], cube[z2][y2][x2]);

                switches.push_back(pair);
            } else {
                done = true;
            }
        }

        std::any_cast<std::vector<double>>(result["h_values"]).push_back(getH());
        return result;
    }

    std::unordered_map<std::string, std::any> sidewayAscentHillClimb(int limit = 100) {
        initialize();
        std::unordered_map<std::string, std::any> result;
        result["initial_state"] = copyCube(*this).cube;
        result["switches"] = std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>();
        result["h_values"] = std::vector<double>();

        auto& h_values = std::any_cast<std::vector<double>&>(result["h_values"]);
        auto& switches = std::any_cast<std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>&>(result["switches"]);

        bool done = false;
        int currentStreak = 0;
        while (!done) {
            double currentH = getH();
            h_values.push_back(currentH);
            auto [pair, newH] = findSteepestAscent();

            if (newH > currentH || (currentH == newH && currentStreak < limit)) {
                auto [coord1, coord2] = pair;
                auto [x1, y1, z1] = coord1;
                auto [x2, y2, z2] = coord2;
                std::swap(cube[z1][y1][x1], cube[z2][y2][x2]);

                switches.push_back(pair);

                if (newH > currentH){
                    currentStreak = 0;
                }
                else{
                    currentStreak++;
                }
            } else {
                done = true;
            }
        }

        std::any_cast<std::vector<double>>(result["h_values"]).push_back(getH());
        return result;
    }

    std::unordered_map<std::string, std::any> randomRestartHillClimb(int max_restart = 10) {
        std::unordered_map<std::string, std::any> result;
        result["iteration_per_restarts"] = std::vector<int>();
        int iteration = 0;
        double maxH = 0;

        auto& iteration_per_restarts = std::any_cast<std::vector<int>&>(result["iteration_per_restarts"]);

        while (getH() != 109 && iteration < max_restart) {
            auto currResult = steepestAscentHillClimb();
            iteration_per_restarts.push_back(
                std::any_cast<std::vector<double>>(currResult["h_values"]).size()
            );

            double currentH = getH();
            if (currentH > maxH) {
                result["initial_state"] = currResult["initial_state"];
                result["switches"] = currResult["switches"];
                result["h_values"] = currResult["h_values"];
                maxH = currentH;
            }
            iteration++;
        }

        result["restart_counts"] = iteration;
        return result;
    }

    std::unordered_map<std::string, std::any> stochasticHillClimb() {
        initialize();
        std::unordered_map<std::string, std::any> result;
        result["initial_state"] = copyCube(*this).cube;
        result["switches"] = std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>();
        result["h_values"] = std::vector<double>();

        auto& h_values = std::any_cast<std::vector<double>&>(result["h_values"]);
        auto& switches = std::any_cast<std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>&>(result["switches"]);

        const int nmax = 100000;

        std::srand(static_cast<unsigned int>(std::time(nullptr)));

        for (int i = 0; i < nmax; ++i) {
            int x1, y1, z1, x2, y2, z2;

            do {
                x1 = std::rand() % dimension;
                y1 = std::rand() % dimension;
                z1 = std::rand() % dimension;
                x2 = std::rand() % dimension;
                y2 = std::rand() % dimension;
                z2 = std::rand() % dimension;
            } while (x1 == x2 && y1 == y2 && z1 == z2);

            double currentH = getH();
            std::swap(cube[z1][y1][x1], cube[z2][y2][x2]);

            double newH = getH();

            if (currentH >= newH) {
                std::swap(cube[z1][y1][x1], cube[z2][y2][x2]);
            } else {
                switches.emplace_back(std::make_tuple(x1, y1, z1), std::make_tuple(x2, y2, z2));
            }

            h_values.push_back(getH());
        }

        return result;
    }

    double getTemperature(int iteration) const {
        return 200 * std::pow(iteration, -0.5) - 8;
    }

    double getProbability(double deltaE, double temp) const {
        return std::exp(deltaE / temp);
    }

    std::unordered_map<std::string, std::any> simulatedAnnealing() {
        initialize();
        std::unordered_map<std::string, std::any> result;
        result["initial_state"] = copyCube(*this).cube;
        result["switches"] = std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>();
        result["h_values"] = std::vector<double>();
        result["boltzmanns"] = std::vector<double>();
        result["stucks"] = 0;

        auto& h_values = std::any_cast<std::vector<double>&>(result["h_values"]);
        auto& switches = std::any_cast<std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>&>(result["switches"]);
        auto& boltzmanns = std::any_cast<std::vector<double>&>(result["boltzmanns"]);
        auto& stucks = std::any_cast<int&>(result["stucks"]);

        int iteration = 1;
        double temperature = getTemperature(iteration);

        std::srand(static_cast<unsigned int>(std::time(nullptr)));

        h_values.push_back(getH());

        while (temperature > 0) {
            int x1, y1, z1, x2, y2, z2;

            do {
                x1 = std::rand() % dimension;
                y1 = std::rand() % dimension;
                z1 = std::rand() % dimension;
                x2 = std::rand() % dimension;
                y2 = std::rand() % dimension;
                z2 = std::rand() % dimension;
            } while (x1 == x2 && y1 == y2 && z1 == z2);

            double currentH = getH();
            std::swap(cube[z1][y1][x1], cube[z2][y2][x2]);

            double newH = getH();
            double probability;

            if (newH >= currentH) {
                boltzmanns.emplace_back(1.0);
                switches.emplace_back(std::make_tuple(x1, y1, z1), std::make_tuple(x2, y2, z2));
            } else {
                double roll = static_cast<double>(std::rand()) / RAND_MAX;
                probability = getProbability(newH - currentH, temperature);
                boltzmanns.emplace_back(probability);
                stucks++;

                if (roll > probability) {
                    std::swap(cube[z1][y1][x1], cube[z2][y2][x2]);
                } else {
                    switches.emplace_back(std::make_tuple(x1, y1, z1), std::make_tuple(x2, y2, z2));
                }
            }

            iteration++;
            temperature = getTemperature(iteration);

            h_values.push_back(getH());
        }

        return result;
    }

    void printCube() const {
        for (int i = 0; i < dimension; ++i) {
            for (int j = 0; j < dimension; ++j) {
                for (int k = 0; k < dimension; ++k) {
                    std::cout << "cube[" << i << "][" << j << "][" << k << "] = " << cube[i][j][k] << std::endl;
                }
            }
        }
    }
};

std::unordered_map<std::string, std::any> runAlgorithm(const std::string& algorithm, const std::unordered_map<std::string, std::any>& argv = {}) {
    Cube cube(5);
    std::unordered_map<std::string, std::any> result;
    
    auto start_time = std::chrono::high_resolution_clock::now();

    if (algorithm == "steepest ascent") {
        result = cube.steepestAscentHillClimb();
    } else if (algorithm == "sideways ascent") {
        if (argv.find("limit") != argv.end()) {
            int limit = std::any_cast<int>(argv.at("limit"));
            result = cube.sidewayAscentHillClimb(limit);
        } else {
            result = cube.sidewayAscentHillClimb();
        }
    } else if (algorithm == "random restart") {
        if (argv.find("max_restart") != argv.end()) {
            int max_restart = std::any_cast<int>(argv.at("max_restart"));
            result = cube.randomRestartHillClimb(max_restart);
        } else {
            result = cube.randomRestartHillClimb();
        }
    } else if (algorithm == "stochastic") {
        result = cube.stochasticHillClimb();
    } else if (algorithm == "simulated annealing") {
        result = cube.simulatedAnnealing();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end_time - start_time;

    result["duration"] = duration.count();
    result["final H"] = cube.getH();
    result["control H"] = cube.controlH();
    result["final_state"] = cube.cube;

    return result;
}

using json = nlohmann::json;

void printResult(const std::unordered_map<std::string, std::any>& result) {
    json jsonResult;

    jsonResult["initial_state"] = std::any_cast<std::vector<std::vector<std::vector<int>>>>(result.at("initial_state"));
    jsonResult["final_state"] = std::any_cast<std::vector<std::vector<std::vector<int>>>>(result.at("final_state"));

    auto switches = std::any_cast<std::vector<std::pair<std::tuple<int, int, int>, std::tuple<int, int, int>>>>(result.at("switches"));
    json jsonSwitches = json::array();
    for (const auto& switchPair : switches) {
        json jsonPair;
        jsonPair.push_back(std::make_tuple(std::get<0>(switchPair.first), std::get<1>(switchPair.first), std::get<2>(switchPair.first)));
        jsonPair.push_back(std::make_tuple(std::get<0>(switchPair.second), std::get<1>(switchPair.second), std::get<2>(switchPair.second)));
        jsonSwitches.push_back(jsonPair);
    }
    jsonResult["switches"] = jsonSwitches;

    jsonResult["h_values"] = std::any_cast<std::vector<double>>(result.at("h_values"));

    jsonResult["final H"] = std::any_cast<double>(result.at("final H"));
    jsonResult["control H"] = std::any_cast<double>(result.at("control H"));
    jsonResult["duration"] = std::any_cast<double>(result.at("duration"));

    if (result.find("iteration_per_restarts") != result.end()) {
        jsonResult["iteration_per_restarts"] = std::any_cast<std::vector<int>>(result.at("iteration_per_restarts"));
    }
    if (result.find("restart_counts") != result.end()) {
        jsonResult["restart_counts"] = std::any_cast<int>(result.at("restart_counts"));
    }

    if (result.find("boltzmanns") != result.end()) {
        jsonResult["boltzmanns"] = std::any_cast<std::vector<double>>(result.at("boltzmanns"));
    }
    if (result.find("stucks") != result.end()) {
        jsonResult["stucks"] = std::any_cast<int>(result.at("stucks"));
    }

    std::cout << jsonResult.dump(4) << std::endl;
}


double Cube::stdfactor = 0.5;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << "cube" << " \"ALGORITHM_NAME\"" << std::endl;
        return 1;
    }

    std::unordered_map<std::string, std::any> options;

    for (int i = 2; i < argc; i += 2) {
        std::string key = argv[i];

        if (key.rfind("--", 0) == 0 && i + 1 < argc) {
            key = key.substr(2); 
            std::string value = argv[i + 1];

            try {
                int intValue = std::stoi(value);
                options[key] = intValue;
            } catch (std::invalid_argument&) {
                options[key] = value;
            }
        } else {
            std::cerr << "Invalid argument format: " << argv[i] << std::endl;
            return 1;
        }
    }

    std::string algorithm = argv[1];
    std::unordered_map<std::string, std::any> result = runAlgorithm(algorithm, options);

    printResult(result);

    return 0;
}