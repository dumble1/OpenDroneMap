#include <stdio.h>
#include<stdlib.h>

int main(){
  int check=0;
  check = system("/code/my_code/copy_vertex");
  if(check == -1){
    printf("error in copy_vertex!\n");
  }else{
    check = system("python /code/my_code/draw.py");
  }
  if(check==-1)
    printf("error in  draw.py");

  return 0;
}
