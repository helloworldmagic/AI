#include <bits/stdc++.h>
using namespace std;


//DFS Function
void DFS(int start , int v, int **adj, vector<bool>& visited){
   
   cout << start << " ";
    visited[start] = true;
    for (int i = 0; i < v; i++) {
        if (adj[start][i] == 1 && (!visited[i])) {
            DFS(i, v, adj, visited);
        }
    }

}
  

int main()
{
    int v,e;
    //v -> no of vertices
    //e -> no of edges
    cin>>v>>e;
    

    //creating a 2d matrix to form a adjagency matrix
    int *adj = new int[v];

    for (int i=0;i<v;i++) {
        adj[i] = new int[v];

        for (int j=0;j<v;j++) {
            adj[i][j] = 0;
        }
    }


    //adding an edge
    for(int i=0;i<e;i++)
    {  
       int x,y;
       cin>>x>>y;
       
       //undirected graph
       adj[x][y] = 1;
       adj[y][x] = 1;

       //directedgraph
       //adj[x][y] = 1;

    }

    // array to get if the node is visited oer not
    vector<bool> visited(v, false);


    //DFS function
    DFS(0, v, adj, visited);
}
