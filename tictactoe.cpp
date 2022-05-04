#include<bits/stdc++.h>
using namespace std;
 
char board [3][3];
int counter = 0;
char turn = 'x';
int choice = 0;


pair<int, int> getrownumber(int x){
  switch(x){
    case 1:
      return {0,0};
    case 2:
      return {0,1};
    case 3: 
      return {0,2};
    case 4: 
      return {1,0};
    case 5:
      return {1,1};
    case 6:
      return {1,2};
    case 7:
      return {2,0};
    case 8:
      return {2,1};
    case 9: 
      return {2,2};
    default:
      return {-1,-1};
  }
}


bool checkwin(int i, int j){
  if(board[i][0] == turn && board[i][1] == turn  && board[i][2] == turn)
    return true;

  if(board[0][j] == turn && board[1][j] == turn && board[2][j] == turn)
    return true;

  if(board[0][0] == turn && board[1][1] == turn && board[2][2] == turn)
    return true;

  if(board[0][2] == turn && board[1][1] == turn && board[2][0] == turn)
    return true;

  return false;
}


bool game(){

  if(turn == 'x')
    cout<<"Player 1 Enter Value: \n";
  

  if(turn == 'o')
    cout<<"player 2 Enter Value: \n";

  cout<<"Enter Your Choice:  ";
  cin>>choice;

  pair <int, int> p = getrownumber(choice);

  int i=p.first, j=p.second;

  if(board[i][j] != '-'){
    cout<<"Already taken number /n";
    game();
  }
    
  else{
    board[i][j] = turn;
    
    if(checkwin(i,j) == true)
      return true;
    
    if(turn == 'x')
     turn = 'o';
    
    else if(turn == 'o')
        turn = 'x';
  }

  
  return false;
  
}

void printBoard(){
  for(int i=0;i<3;i++){
    for(int j=0;j<3;j++)
      cout<<board[i][j]<<" ";
    cout<<endl;
  }

}

int main() {
    
    bool isdraw = false;
  for(int i=0;i<3;i++)
    for(int j=0;j<3;j++)
      board[i][j] = '-';

  cout<<"New game"<<endl;

  printBoard();

  while(true){
    if(counter >= 9){
      cout<<"Match is Draw";
      isdraw = true;
      break;
    }

    bool istrue = game();

    printBoard();
    
    if(istrue)
      break;
  }
    
    if(!isdraw)
  cout<<"Player "<<turn<<" wins"<<endl;
  return 0;
}
