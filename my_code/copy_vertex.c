#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(){

  FILE* fp = fopen("../odm_texturing/odm_textured_model_geo.obj","r");
  FILE* fout = fopen("copy.obj","w");
  FILE* plyout = fopen("copy.ply","w");

  if(fp!=NULL){
    char tmp[200];
    char* token;
    int i=0;
    float max=-1000000, min=1000000;
    float tmpval;
    int r,g,b,cnt=0;

     while(fgets(tmp,200,fp)!= '\0'){
      if(tmp[0]=='v'&&tmp[1]==' '){    // only vertex.
        cnt++;
        //printf("%s",tmp);
        fputs(tmp,fout);
        token = strtok(tmp," ");
        for(i=0;i<3;i++)  
          token = strtok(NULL," ");    //get z value
        
        tmpval = atof(token);

        if(max< tmpval)
          max = tmpval;
        if(min>tmpval)
          min = tmpval;
      }
      else continue;
    }
    fclose(fout);
    fclose(fp);


    fp = fopen("copy.obj","r");
    float range = max-min;
    //printf("%f\n",range);
    float tmpcolor;
    char color[12]={0};
    char plyformat[200];
    //char* tmp2;
    //tmp2 = (char *)malloc(200);
    char* tokenArr[2];
    tmpval =0;
    
   // printf("make ply\n");
    
    sprintf(plyformat, "ply\nformat ascii 1.0\nelement vertex %d\nproperty float x\nproperty float y\nproperty float z\nproperty uchar diffuse_red\nproperty uchar diffuse_green\nproperty uchar diffuse_blue\nend_header\n",cnt);
     
      fputs(plyformat,plyout);
      for(i=0;i<2;i++){
        tokenArr[i] = (char*)malloc(15);
      }

      while(fgets(tmp,200,fp)!= '\0'){
        //printf("%s",tmp);
        //strcpy(tmp2,tmp);
        //tmp2 = strtok(tmp2,"\n");
        //tmp2 = tmp2 +2;
        token = strtok(tmp," ");
       // printf("%s\n",token);

        for(i=0;i<2;i++){  
          //printf("%d",i);
          tokenArr[i] = strtok(NULL," ");   
        }
        token = strtok(NULL," ");   //get z.

        //printf(" %s\n",token);
        tmpval = atof(token);
        tmpval = tmpval -min;
        tmpcolor = (tmpval)*1020/range;
        if(tmpcolor<=255){            //blue range
            r=0; g=tmpcolor; b=255;
        }
        else if(tmpcolor>255&&tmpcolor<=510){
            r=0; g= 255 ; b = 255-(tmpcolor-255);
        }
        else if(tmpcolor>510 && tmpcolor<=765){
            r= tmpcolor-510; g=255; b=0;
        }
        else if(tmpcolor>765 && tmpcolor<=1020){
            r= 255; g=255-(tmpcolor-765); b=0;
        }
        else printf("color error!\n");
        i=0;
        sprintf(tmp,"%s %s 0 %d %d %d\n",tokenArr[0],tokenArr[1],r,g,b);
       // printf("%s",tmp);

        fputs(tmp, plyout);
       //printf("print\n"); 
    }
    fclose(fp);
    fclose(plyout);
  }

  return 0;
}
