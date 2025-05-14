#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <climits>

using namespace std;

// Function to map the tile name to an index
int getTileIndex(const string& tile) {
    if (tile == "up") return 0;
    if (tile == "down") return 1;
    if (tile == "left") return 2;
    if (tile == "right") return 3;
    return -1; // Invalid input (should not happen with valid constraints)
}

int calculateMinimumMoves(int N, const vector<string>& instructions) {
    // DP table: dp[i][j][k]
    // i: instruction index, j: position of left leg, k: position of right leg
    vector<vector<vector<int>>> dp(N + 1, vector<vector<int>>(4, vector<int>(4, INT_MAX)));

    // Initialize DP for the first instruction (start at any position)
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            dp[0][i][j] = 0; // No moves required initially
        }
    }

    // Process each instruction
    for (int i = 1; i <= N; ++i) {
        int targetTile = getTileIndex(instructions[i - 1]);
        for (int left = 0; left < 4; ++left) {
            for (int right = 0; right < 4; ++right) {
                if (left == targetTile || right == targetTile) {
                    // One leg is already on the target tile
                    dp[i][left][right] = min(dp[i][left][right], dp[i - 1][left][right]);
                } else {
                    // Move left leg to the target tile
                    dp[i][targetTile][right] = min(dp[i][targetTile][right], dp[i - 1][left][right] + 1);
                    // Move right leg to the target tile
                    dp[i][left][targetTile] = min(dp[i][left][targetTile], dp[i - 1][left][right] + 1);
                }
            }
        }
    }

    // Find the minimum moves in the last state
    int result = INT_MAX;
    for (int left = 0; left < 4; ++left) {
        for (int right = 0; right < 4; ++right) {
            result = min(result, dp[N][left][right]);
        }
    }

    return result;
}

int main() {
    int N;
    cin >> N;

    vector<string> instructions(N);
    for (int i = 0; i < N; ++i) {
        cin >> instructions[i];
    }

    cout << calculateMinimumMoves(N, instructions) << endl;

    return 0;
}

