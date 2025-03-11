#include <algorithm>
#include <iostream>
#include <unordered_set>
#include <unordered_map>
#include <vector>
#include <tuple>
#include <set>
#include <cstdint>

using namespace std;

vector<set<vector<uint8_t>>> IPS;

void integer_partitions_helper(uint8_t n, vector<uint8_t> current, set<vector<uint8_t>> &result, uint8_t max_val) {
    
    if (n == 0) {
        result.emplace(current);
        return;
    }

    for (uint8_t i = min(n, max_val); i >= 1; --i) {
        current.insert(current.begin(), i);
        integer_partitions_helper(n - i, current, result, i);
        current.erase(current.begin()); // Backtrack
    }
}

set<vector<uint8_t>> integer_partitions(uint8_t n) {
    set<vector<uint8_t>> result;
    vector<uint8_t> current;

    integer_partitions_helper(n, current, result, n);

    printf("%d\n", result.size());
    return result;
}

int main(void) {
  uint8_t n =  26;

  // Create a list of all integer partitions from 1 to n 
  for (uint8_t i = 1; i <= n; i++) {
    IPS.push_back(integer_partitions(i));
  }

  // for (uint8_t i = 25; i < n; i++) {
  //   printf("[");
  //   for (const auto &p : IPS[i]) {
  //     printf("{");
  //     for (uint8_t num : p) {
  //       printf("%d ", num);
  //     }
  //     printf("}, ");
  //   }
  //   printf("]\n");
    
  // }

  return 0;
}
