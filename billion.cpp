#include <iostream>
#include <chrono>

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    for (long long i = 1; i <= 1000000000; ++i) {
        // The loop does nothing but iterate
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;

    std::cout << "Counting from 1 to 1,000,000,000 took " << duration.count() << " seconds." << std::endl;

    return 0;
}
