from collections import defaultdict
from queue import PriorityQueue
v=10
graph=defaultdict(list)
h={
  'A':12,
  'B':4,
  'C':7,
  'D':3,
  'E':8,
  'F':2,
  'G':0,
  'H':4,
  'I':9,
  'S':13,
}
answer=[]
def best_first_search(start,end):
  visited=[]
  visited.append(start)
  q=PriorityQueue()
  q.put((h[start],start))
  while q.empty()==False:
    a=q.get()
    answer.append(a[1])
    if a[1]==end:
      break
    else:
      for e in graph[a[1]]:
      # print(e[0])
        if e[0] not in visited:
          visited.append(e[0])
          q.put((h[e[0]],e[0]))

def add_vertex(x,y,c):
  graph[x].append((y,c))
add_vertex('S','A',3)
add_vertex('S','B',2)
add_vertex('A','C',4)
add_vertex('A','D',1)
add_vertex('B','E',3)
add_vertex('B','F',1)
add_vertex('E','H',5)
add_vertex('F','I',2)
add_vertex('F','G',3)
best_first_search('S','G')
print(answer)
