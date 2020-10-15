#include <pthread.h> //incluye la libreria para manejar hilos POSIX
#include <stdio.h> // esta es la libreia standar de llamadas al sistema


void *codigo_del_hilo(void *id) // define la funcion que va ejecutar el hilo y le permite pasar a la funcion del hilo el id
{
 int i; // define i como entero
 for(i = 0; i < 50; i++) // itera i desde 0 hasta 49
  printf("\n Soy el hilo: %d, iter = %d", *(int*)id, i); // Imprime el ID del hilo junto a la iteracion en la que se encuentra
 pthread_exit(id); // Termina el hilo con identificador id
}

// codigo del proceso principal
int main(void) // define la funcion principal como que no regresa nada
{
  pthread_t hilo; // Identifica al hilo como "hilo"
  int id = 245; // Define el ID como 245
  int *salida;  // Trabaja con salida en su direccion de memoria
  pthread_create(&hilo, NULL, codigo_del_hilo, &id); // NULL se creará con sus atributos por defecto, codigo_del_hilo le indica al hilo que se va a crear la funci'on que este hilo va a ejecutar, &hilo (Su direccion de memoria), &id su id
  pthread_join(hilo, NULL); // Espera a que el hilo identificado como hilo termine
  printf("\n Hilo %d terminado \n", *salida); // imprime que ha terminado el hilo con if salida
  return(0); // termina la funcion
}