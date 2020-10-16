#include <pthread.h>  //incluye la libreria para manejar hilos POSIX
#include <stdio.h> // esta es la libreia standar de llamadas al sistema

void *codigo_del_hilo(void *id)// define la funcion que va ejecutar el hilo y le permite pasar a la funcion del hilo el id
{
 int i;  // define i como entero
 for(i = 0; i < 50; i++) // itera i desde 0 hasta 49
  printf("\n Soy el hilo: %d, iter = %d", *(int*)id, i); // Imprime el ID del hilo junto a la iteracion en la que se encuentra
 pthread_exit(id); // Termina el hilo con identificador id
}

// codigo del proceso principal
int main(void) // define la funcion principal como que no regresa nada
{
  pthread_t hilo1, hilo2; // crea dos identificadores de hilo: hilo1 e hilo2
  int id1 = 11; // asigna el id1 como 11 entero
  int id2 = 55; // asigna el id2 como 55 entero
  
  pthread_create(&hilo1, NULL, codigo_del_hilo, &id2); // crea un hilo con identificador hilo1 que ejecute el codigo_del_hilo
  pthread_create(&hilo2, NULL, codigo_del_hilo, &id1); // crea un hilo con identificador hilo2 que ejecute el codigo_del_hilo

  pthread_join(hilo1, NULL); // Espera a que termine el hilo 1 sin esperar que regrese nada
  pthread_join(hilo2, NULL); // Espera a que termine el hilo 2 sin esperar que regrese nada

  printf("\n Hilos terminados \n"); // Termina el hilo
  return(0); // termina el programa
}