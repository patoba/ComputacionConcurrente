/*
Este programa crea 5 procesos hijos (numero definido por la variable NUM_PROCESOS)
y en cada proceso ejecuta la funcion codigo_del_proceso. Esta funcion cuenta desde
0 hasta 49, imprimiendo tambien el id del proceso.
Cuando todos los procesos hijos han acabado de ejecutar, imprime el codigo de 
retorno de cada uno. Esta impresion algunas veces puede desincronizarse debido
a que los distintos procesos hijos intentan escribir a stdout al mismo tiempo.
*/

#include <stdio.h> // Biblioteca estandar para entrada y salida de datos
#include <stdlib.h> // Biblioteca que incluye funcion importantes e ne llos progrmas (como exit)
#include <sys/wait.h> // Para poder usar la funcion wait
#include <unistd.h> // Biblioteca que permite usar la funcion fork

#define NUM_PROCESOS 5 //Inicializa la variable global NUM_PROCESOS. 

int I = 0;  // define I como un entero y inicializalo en 0

void codigo_del_proceso (int id)  // define la funcion codigo_del_proceso con entrara id entera
{
   int i;  // declara la variable i como entero

   for (i = 0; i < 50; i++)  // para i desde 0 hasta i < 50 incrementa i de uno en uno
        printf("Proceso %d: i = %d, I = %d\n", id, i, I++ ); // imprime i, el id y I aumentandola I en 1 cada vez
   exit (id); // termina el proceso y regresa el codigo

}

int main(void) // proceso principal
{
    int p; // define p como entero
    int id[NUM_PROCESOS] = {1, 2, 3, 4, 5};  // define el arreglo id como entero
    int pid;  // define pid como entero
    int salida;  // define salida como entero

    for (p = 0; p < NUM_PROCESOS; p++)
    {
        pid = fork(); // crea un proceso nuevo
        if (pid == -1) // si el id del proceso es negativo (hubo un error al crear el proceso)
        {
            perror("Error al crear un proceso: "); // tira un error
            exit(-1); // termina la ejecucion con codigo de retorno -1
        }
        else if (pid == 0) // si el id del proceso es 0 (es un proceso hijo)
            codigo_del_proceso (id[p]); // imprime 
    }


    // codigo proceso padre
    for (p = 0; p < NUM_PROCESOS; p++)  // para p desde 0 hasta p el numero de procesos aumentando en 1
    {
        pid = wait(&salida); // obtiene el codigo de salida del proceso
        printf("Proceso %d con id = %x terminado\n", pid, salida >> 8);
        // imprime el id del proceso y el codigo de salida (obtenido desplazando la funcion de salida 8 bits a la derecha)
    }

    return(0); // termina el codigo
}
