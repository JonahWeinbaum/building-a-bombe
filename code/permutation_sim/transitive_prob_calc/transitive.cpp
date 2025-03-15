#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <set>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;
using std::chrono::duration;
using std::chrono::duration_cast;
using std::chrono::high_resolution_clock;
using std::chrono::seconds;

struct ProbHash {
  size_t
  operator()(const tuple<vector<uint8_t>, vector<uint8_t>, int> &key) const {
    auto &[v1, v2, n] = key;
    size_t h1 = hash<int>()(n);
    size_t h2 = 0, h3 = 0;

    for (uint8_t x : v1)
      h2 ^= hash<uint8_t>()(x) + 0x9e3779b9 + (h2 << 6) + (h2 >> 2);
    for (uint8_t x : v2)
      h3 ^= hash<uint8_t>()(x) + 0x9e3779b9 + (h3 << 6) + (h3 >> 2);

    return h1 ^ h2 ^ h3;
  }
};

struct PopHash {
  size_t operator()(const tuple<vector<uint8_t>, vector<uint8_t>> &key) const {
    auto &[v1, v2] = key;
    size_t h1 = 0, h2 = 0;

    for (uint8_t x : v1)
      h1 ^= hash<uint8_t>()(x) + 0x9e3779b9 + (h1 << 6) + (h1 >> 2);
    for (uint8_t x : v2)
      h2 ^= hash<uint8_t>()(x) + 0x9e3779b9 + (h2 << 6) + (h2 >> 2);

    return h1 ^ h2;
  }
};

struct VVIComparator {
  bool operator()(const vector<vector<uint8_t>> &v1,
                  const vector<vector<uint8_t>> &v2) const {
    vector<vector<uint8_t>> sorted_v1 = v1;
    vector<vector<uint8_t>> sorted_v2 = v2;

    sort(sorted_v1.begin(), sorted_v1.end());
    sort(sorted_v2.begin(), sorted_v2.end());
    return sorted_v1 < sorted_v2;
  }
};

unordered_map<tuple<vector<uint8_t>, vector<uint8_t>, int>, double, ProbHash>
    prob_memo;
unordered_map<tuple<vector<uint8_t>, vector<uint8_t>>,
              set<vector<vector<uint8_t>>, VVIComparator>, PopHash>
    pop_memo;

std::ostream &operator<<(std::ostream &os, const vector<pair<int, int>> &mult) {
  os << "{";
  for (const auto &pair : mult) {
    os << "<" << pair.first << ", " << pair.second << ">";
  }
  os << "}";
  return os;
}

std::ostream &operator<<(std::ostream &os, const vector<uint8_t> &vi) {
  os << "{";
  for (const auto &num : vi) {
    os << to_string(num) << " ";
  }
  os << "}";
  return os;
}

std::ostream &operator<<(std::ostream &os, const vector<vector<uint8_t>> &vvi) {
  os << "{";
  for (const auto &vi : vvi) {
    os << vi;
  }
  os << "}";
  return os;
}

std::ostream &
operator<<(std::ostream &os,
           const set<vector<vector<uint8_t>>, VVIComparator> &svvi) {
  os << "[";
  for (const auto &vvi : svvi) {
    os << vvi;
  }
  os << "]";
  return os;
}

vector<vector<vector<uint8_t>>> IPS;

void integer_partitions_helper(uint8_t n, vector<uint8_t> current,
                               set<vector<uint8_t>> &result, uint8_t max_val) {

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

vector<vector<uint8_t>> integer_partitions(uint8_t n) {
  set<vector<uint8_t>> result;
  vector<uint8_t> current;

  integer_partitions_helper(n, current, result, n);

  vector<vector<uint8_t>> to_vec(result.begin(), result.end());

  return to_vec;
}

set<vector<vector<uint8_t>>, VVIComparator>
partition_of_partition(vector<uint8_t> p, const vector<uint8_t> target_p,
                       int depth = 0) {

  tuple key = {p, target_p};
  if (pop_memo.find(key) != pop_memo.end()) {
    return pop_memo[key];
  }

  
  set<vector<vector<uint8_t>>, VVIComparator> result;

  // Base case with valid partition
  if (p.empty() && target_p.empty()) {
    result.insert(vector<vector<uint8_t>>{});
  }

  // Base case with invalid partition
  if (p.empty() || target_p.empty()) {
    return result;
  }

  uint8_t head = target_p[0];
  vector<uint8_t> tail(target_p.begin() + 1, target_p.end());

  for (const vector<uint8_t> &part : IPS[head - 1]) {

    // part is a subset of p
    if (includes(p.begin(), p.end(), part.begin(), part.end())) {
      // Remove part from p
      vector<uint8_t> diff;
      set_difference(p.begin(), p.end(), part.begin(), part.end(),
                     inserter(diff, diff.begin()));

      // Recursive call to compute possible suffices
      set<vector<vector<uint8_t>>, VVIComparator> suffixes =
          partition_of_partition(move(diff), tail, depth + 2);
      for (vector<vector<uint8_t>> suffix : suffixes) {
        suffix.insert(suffix.begin(), part);
        result.emplace(move(suffix));
      }
    }
  }

  pop_memo[key] = result;
  return result;
}

vector<pair<int, int>> multiplicity(const vector<uint8_t> &p) {
  unordered_map<int, int> freq_map;

  for (int num : p) {
    freq_map[num]++;
  }

  vector<pair<int, int>> result(freq_map.begin(), freq_map.end());
  return result;
}

int num_of_partition(const vector<uint8_t> &p, int n) {
  float result = tgamma(n + 1);
  vector<pair<int, int>> p_m = multiplicity(p);
  for (const auto &pair : p_m) {
    result /=
        pow(tgamma(pair.first + 1), pair.second) * tgamma(pair.second + 1);
  }
  return (int)result;
}

int num_of_cycle_type(const vector<uint8_t> &p, int n) {
  float result = tgamma(n + 1);
  vector<pair<int, int>> p_m = multiplicity(p);
  for (const auto &pair : p_m) {
    result /= pow(pair.first, pair.second) * tgamma(pair.second + 1);
  }
  return (int)result;
}

int partitions_to_search_space(vector<uint8_t> &p1, vector<uint8_t> &p2,
                               int n) {
  return num_of_cycle_type(p1, n) * num_of_cycle_type(p2, n);
}

vector<vector<vector<vector<uint8_t>>>>
group_pops(set<vector<vector<uint8_t>>, VVIComparator> &pop1,
           set<vector<vector<uint8_t>>, VVIComparator> &pop2) {
  vector<vector<vector<vector<uint8_t>>>> result;
  for (const auto &subpop1 : pop1) {
    for (const auto &subpop2 : pop2) {
      result.push_back(vector<vector<vector<uint8_t>>>{});
      for (int i = 0; i < subpop1.size(); i++) {
        vector<vector<uint8_t>> pair = {subpop1[i], subpop2[i]};
        sort(pair.begin(), pair.end());
        result.back().push_back(pair);
      }
    }
  }
  return result;
}

float get_transitive_prob(vector<uint8_t> &p1, vector<uint8_t> &p2, int n) {
  if (p1.size() == 1 || p2.size() == 1) {
    return 1.0;
  }

  tuple key = {p1, p2, n};
  if (prob_memo.find(key) != prob_memo.end()) {
    return prob_memo[key];
  }

  int search_size = partitions_to_search_space(p1, p2, n);
  float result = search_size;

  for (auto &part : IPS[n - 1]) {
    if (part.size() == 1) {
      continue;
    }
    tuple key1 = {p1, part};
    tuple key2 = {p2, part};
    set<vector<vector<uint8_t>>, VVIComparator> c1_pop = pop_memo[key1];
    set<vector<vector<uint8_t>>, VVIComparator> c2_pop = pop_memo[key2];

    if (c1_pop.empty() || c2_pop.empty()) {
      continue;
    }

    vector<vector<vector<vector<uint8_t>>>> groups = group_pops(c1_pop, c2_pop);

    float subtotal = 0.0;
    for (auto &group : groups) {
      float subsubtotal = 1.0;
      for (int i = 0; i < group.size(); i++) {
        subsubtotal *=
            partitions_to_search_space(group[i][0], group[i][1], part[i]) *
            get_transitive_prob(group[i][0], group[i][1], part[i]);
      }
      subtotal += subsubtotal;
    }
    subtotal *= num_of_partition(part, n);

    result -= subtotal;
  }

  result /= search_size;

  // Store in memo table
  prob_memo[key] = result;

  return result;
}

int main(void) {
  uint8_t n = 26;

  cout << "GENERATING IPS..." << endl;
  
  // Create a list of all integer partitions from 1 to n
  for (uint8_t i = 1; i <= n; i++) {
    IPS.push_back(integer_partitions(i));
  }

  cout << "GENERATED IPS!" << endl;

  cout << "GENERATING POPS..." << endl;
  
  for (int k = 1; k <= n; k++) {
    for (int i = 0; i < IPS[k - 1].size(); i++) {
      for (int j = 0; j <= i; j++) {
        partition_of_partition(IPS[k - 1][i], IPS[k - 1][j], n);
      }
    }
  }

  cout << "GENEARTED POPS!" << endl;

  cout << "COMPUTING PROBS..." << endl;

  for (int k = 1; k <= n; k++) {
    cout << "Computing loop (k=" << k << ")" << endl;
    auto t1 = high_resolution_clock::now();
    for (int i = 0; i < IPS[k - 1].size(); i++) {
      for (int j = 0; j <= i; j++) {
	get_transitive_prob(IPS[k - 1][i], IPS[k - 1][j], n);
      }
    }
    auto t2 = high_resolution_clock::now();
    auto ms_int = duration_cast<seconds>(t2 - t1);
    cout << "\tLoop took " << ms_int << endl;
  }

  return 0;
}
