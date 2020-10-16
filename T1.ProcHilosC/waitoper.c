#include <stdio.h>  // Biblioteca estandar para entrada y salida de datos
#include <stdlib.h>  // Biblioteca que incluye funcion importantes e ne llos progrmas (como exit)
#include <sys/types.h>  // Para usar pid_t
#include <sys/wait.h>  // Para poder usar la funcion wait
#include <unistd.h>   // Biblioteca que permite usar la funcion fork

int main(void)  // empieza el programa
{
   int i;   // define la variable i como entero
   int a,b;  // define las variables a y b como enteros
   pid_t pidh1,pidh2,pidx;  // define las variables pidh1, pidh1 y pidx como tipo pid_t
   // pid_t es un tipo de variable entera que se usa para almacenar ids de proceso
   int prod, mayor;   // define las variables prod y mayor como enteros
   int res; // define la variable res como entero

   printf("\nDame dos enteros: \n"); // pide dos enteros al usuario
   scanf("%d %d", &a, &b); // colecta el input dado por el usuario
   printf("%d %d\n", a, b);
   pidh1 = fork(); // crea un nuevo proceso y le asigna su id en pidh1

// código del padre
   if(pidh1)  // si pidh1 es distinto de cero (si es un proceso padre)
   {
      pidh2 = fork();   // crea un nuevo proceso y le asigna su id a pidh2
      if(pidh2)  // si pidh1 es distinto de cero (si es un proceso padre)
      {
        for(i = 0; i < 2; i++) // para i desde 0 hasta i menor a 2 en pasos de 1
        {
            pidx = wait(&res); // wait regresa el pid del proceso que espera el padre, y res poseera el valor del estado de salida del proces hijo
 	        if (pidx == pidh1)  // si el id del proceso es igual al id del prceso pidh1 (si es el proceso hijo 1)
               prod = WEXITSTATUS(res); // asigna el valor de salida del proceso hijo 1 a prod (WEXITSTATUS sirve para obtener la salida)
            else   // si los id de los procesos pidx y pidh son diferents (si es el proceso hijo 2)
               mayor = WEXITSTATUS(res);  // asigna el valor de salida del proceso hijo 1 a mayor (WEXITSTATUS sirve para obtener la salida)
        }
        printf("\n El producto de %d y %d es %d", a, b, prod); // imprime el producto de a y b
        printf("\n El mayor de %d y %d es %d \n", a, b, mayor); // imprime el mayor de a y b
      }

      else // si pidh2 es cero (si es un proceso hijo) compara a y b
      {
         if(a > b) 
            exit(a); // si a es mayor que b, termina el proceso y regresa a
         else
            exit(b); // si b es mayor que a, termina el proceso y regresa b
      }
   }

   else // si pidh1 es cero (si es un proceso hijo) multiplica a y b
   {
	   prod = a * b;
	   exit(prod); // termina el proceso y regresa el producto de a y b
   }

  return(0); // termina la funcion

 }