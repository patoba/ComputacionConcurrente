#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
   int i;
   int a,b;
   pid_t pidh1,pidh2,pidx;
   int prod,mayor;
   int res;

   printf("\nDame dos enteros: \n");
   scanf("%d%d", &a, &b);
   pidh1 = fork();

// código del padre
   if(pidh1)
   {
      pidh2 = fork();
      if(pidh2)
      {
        for(i = 0; i < 2; i++)
        {
           pidx = wait(&res);
 	   if (pidx == pidh1)
             prod = res;
           else
             mayor = res;
        }
        printf("\n El producto de %d y %d es %d", a,b,prod);
        printf("\n El mayor de %d y %d es %d \n", a,b,mayor);
      }

      else
      {
         if(a > b)
           exit(a);
         else
           exit(b);
      }
   }
// hijo 1
   else
      {
	 prod = a * b;
	 exit(prod);
      }

  return(0);

 }
