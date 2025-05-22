#include<bits/stdc++.h>
using namespace std;

void hey(string a, string b) {
    int l = a.length();
    int arr[l + 1][l + 1];
    for (int i = 0; i <= l; i++) {
        for (int j = 0; j <= l; j++) {
            arr[i][j] = 0;
        }
    }

    for (int i = 1; i <= l; i++) {
        for (int j = 1; j <= l; j++) {
            if (a[i - 1] == b[j - 1]) {
                arr[i][j] = arr[i - 1][j - 1] + 1;
            } else {
                arr[i][j] = max(arr[i - 1][j], arr[i][j - 1]);
            }
        }
    }

    int i = l, j = l;
    int index = arr[l][l];
    string str(a.length() + 1, '\0');
    while (i > 0 && j > 0) {
        if (a[i - 1] == b[j - 1]) {
            str[index - 1] = a[i - 1];
            index--;
            i--;
            j--;
        } else if (arr[i][j - 1] > arr[i - 1][j]) {
            i--;
        } else {
            j--;
        }
    }

    cout << str;
}

int main() {
    string a;
    cin >> a;
    string b = a;
    reverse(b.begin(), b.end());
    hey(a, b);
    return 0;
}

