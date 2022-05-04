#include <bits/stdc++.h>
using namespace std;


//DFS Function
void BFS(int start , int v, vector<int> adj[], vector<bool>& visited){
    
    queue<int> q;
    q.push(start);

    visited[start] = true;

    while(!q.empty())
    {
        int curr = q.front();
        q.pop();
        cout<<curr<<" ";

        for(int i=0;i<adj[curr].size();i++)
            if(visited[adj[curr][i]] == false)
            {
                q.push(adj[curr][i]);
                visited[adj[curr][i]] = true;
            }
    }

}
  

int main()
{
    int v,e;
    cin>>v>>e;
    

    //creating a 2d matrix to form a adjagency matrix
    vector<int> adj[v];

  

    //adding an edge
    for(int i=0;i<e;i++)
    {  
       int x,y;
       cin>>x>>y;
       
       //undirected graph
       adj[x].push_back(y);
       adj[y].push_back(x);
   
       //directedgraph
       // adj[x].push_back(y);

    }

    // array to get if the node is visited oer not
    vector<bool> visited(v, false);


    //DFS function
    BFS(0, v, adj, visited);
}
