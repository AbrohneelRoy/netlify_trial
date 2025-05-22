#include<bits/stdc++.h>
#include<vector>
using namespace std;

const int MAX = 100;
int cost[MAX][MAX];
int dp[MAX][MAX];  // A 2D array to store the minimum cost values
int r, c;

int mincost() {
    // Initialize the dp array
    dp[0][0] = cost[0][0];

    // Initialize the first row and first column of dp
    for (int i = 1; i < r; i++) {
        dp[i][0] = dp[i - 1][0] + cost[i][0];
    }
    for (int j = 1; j < c; j++) {
        dp[0][j] = dp[0][j - 1] + cost[0][j];
    }

    // Fill the dp array
    for (int i = 1; i < r; i++) {
        for (int j = 1; j < c; j++) {
            dp[i][j] = cost[i][j] + min(dp[i - 1][j], dp[i][j - 1]);
        }
    }

    int i = r - 1, j = c - 1;
    vector<pair<int, int>> path;
    path.push_back({i, j});

    // Backtrack to find the path
    while (i > 0 || j > 0) {
        if (i > 0 && dp[i - 1][j] < dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
        path.push_back({i, j});
    }

    reverse(path.begin(), path.end());

    // Print the path
    cout << "Minimum cost: " << dp[r - 1][c - 1] << endl;
    cout << "Path:" << endl;
    for (auto p : path) {
        cout << "(" << p.first << "," << p.second << ") ";
    }

    return dp[r - 1][c - 1];
}

int main() {
    cin >> r >> c;
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            cin >> cost[i][j];
        }
    }
    mincost();
    return 0;
}

