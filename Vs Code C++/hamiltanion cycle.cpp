#include <iostream>
using namespace std;

#define V 5

void printSolution(int path[]);

bool isSafe(int v, bool graph[V][V], int path[], int pos) {
    if (graph[path[pos - 1]][v] == 0)
        return false;
    for (int i = 0; i < pos; i++)
        if (path[i] == v)
            return false;
    return true;
}

bool hamCycleUtil(bool graph[V][V], int path[], int pos) {
    if (pos == V) {
        if (graph[path[pos - 1]][path[0]] == 1)
            return true;
        else
            return false;
    }

    for (int v = 1; v < V; v++) {
        if (isSafe(v, graph, path, pos)) {
            path[pos] = v;
            if (hamCycleUtil(graph, path, pos + 1) == true)
                return true;
            path[pos] = -1;
        }
    }

    return false;
}

bool hamCycle(bool graph[V][V]) {
    int *path = new int[V];
    for (int i = 0; i < V; i++) 
        path[i] = -1;

    path[0] = 0;
    if (hamCycleUtil(graph, path, 1) == false) {
        cout << "Solution does not exist" << endl;
        return false;
    }

    printSolution(path);
    return true;
}

void printSolution(int path[]) {
    cout << "Solution Exists: Hamiltonian Cycle\n";
    for (int i = 0; i < V; i++)
        cout << path[i] << " ";
    cout << path[0] << " " << endl;
}

int main() {
    bool graph[V][V];
    cout << "Enter the adjacency matrix for the graph (0 or 1):\n";
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            cin >> graph[i][j];
        }
    }

    if (hamCycle(graph)) {
        cout << "Hamiltonian Cycle found!" << endl;
    } else {
        cout << "No Hamiltonian Cycle found." << endl;
    }

    return 0;
}

