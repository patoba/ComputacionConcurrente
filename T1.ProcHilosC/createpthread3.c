#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define NUM_HILOS 5  // define el numero de hilos NUM_HILOS como 5

int I = 0;  // define la variable I como entero y lo inicializa en 0

void *codigo_del_hilo(void *id) // define la funcion que va ejecutar el hilo y le permite pasar a la funcion del hilo el id
{
    int i; // define i como entero
    for(i = 0; i < 50; i++) // para i desde 0 hasta 49
      printf("Hilo %d; i = %d, I = %d\n", *(int*)id, i, I++);  // Imprime el ID del hilo junto a la iteracion en la que se encuentra y aumenta I en 1 y lo imprime
 pthread_exit(id); // termina el hilo
}


// codigo del proceso principal
int main(void) // define la funcion principal como que no regresa nada
{
    int h; // define h como entero
    pthread_t hilos[NUM_HILOS]; // crea identificadores para los hilos
    int id[NUM_HILOS] = {1, 2, 3, 4, 5};  // crea los id para los hilos
    int error; // define la variable error como entera
    int *salida; // define la varible salida como entera
    for (h = 0; h < NUM_HILOS; h++){ // este for se ejecuta 5 veces para crear los 5 hilos
        error = pthread_create(&hilos[h], NULL, codigo_del_hilo, &id[h]); // guarda en error lo que regresa pthread_create
        // si regresa algo distinto de cero habra ocurrido un error
        if (error){ // si error es distinto de cero
          fprintf(stderr, "Error %d %s\n", error, strerror (error)); // Imprime el error
          // stderr
          exit(-1); // sal con error
        }
    }
    for (h = 0; h < NUM_HILOS; h++){ // si no hay error ejecuta este bloque de codigo para h desde 0 hasta 4
        error = pthread_join(hilos[h], (void **)&salida); // Espera a los hilos, si 
        if (error)
          fprintf(stderr, "Error %d %s\n", error, strerror (error));
        else
          printf("hilo %d terminado\n", *salida);
    }
}