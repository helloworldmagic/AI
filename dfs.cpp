#include <bits/stdc++.h>
using namespace std;

void DFS(int start , int v, int **adj, vector<bool>& visited){
   cout << start << " ";
    visited[start] = true;
    for (int i = 0; i < v; i++) {
        if (adj[start][i] == 1 && (!visited[i])) {
            DFS(i, v, adj, visited);
        }
    }

}
  

int main(){
   int v,e;
   cout<<"Enter no of vertex : ";
   cin>>v;
   cout<<"Enter no of edeges : ";
   cin>>e;
    
    int *adj = new int[v];

    for (int i=0;i<v;i++) {
        adj[i] = new int[v];

        for (int j=0;j<v;j++) {
            adj[i][j] = 0;
        }
    }
 
    for(int i=0;i<e;i++)
    {  
       int x,y;
       cout<<"Enter x and y : "<<endl;
       cin>>x>>y;
       
       //undirected graph
       adj[x][y] = 1;
       adj[y][x] = 1;

       //directedgraph
       //adj[x][y] = 1;

    }
    vector<bool> visited(v, false);
    DFS(0, v, adj, visited);
}
