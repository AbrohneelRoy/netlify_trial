#include <bits/stdc++.h>
#include <vector>
#include <climits>
using namespace std;

int findMin(vector<int>& arr, int l, int r) {
    int m = INT_MAX;
    for (int i = l; i <= r; i++) {
        m = min(m, arr[i]);
    }
    return m;
}

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    int nqueries;
    cin >> nqueries;
    vector<pair<int, int>> q;
    for (int i = 0; i < nqueries; i++) {
        int start, end;
        cin >> start >> end;
        q.push_back({start, end});
    }
    for (const auto& a : q) {
        int l = a.first;
        int r = a.second;
        int minimum = findMin(arr, l, r);
        cout << "Minimum of [" << l << ", " << r << "] is " << minimum << endl;
    }
    return 0;
}

