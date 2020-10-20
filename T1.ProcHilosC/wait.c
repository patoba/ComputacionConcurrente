#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>  //Tipos adicionales
#include <unistd.h>   // Biblioteca estandar de llamadas al sistema

#include <sys/wait.h>  // Biblioteca para hacer llamada a wait

int main(void){
    pid_t pid;  // define la variable pid como tipo pid_t
    // investiga el tipo de variable pid_t
    int status, died; // define las variables status y died como enteros

    switch(pid = fork()){   // empieza a separar el codigo en segmentos condicionales

    case -1: printf("error.... \n");  //  si  hubo error imprime error
             exit(-1);  // sal con error

    case 0: printf("\t Codigo del hijo: \n");  // Si no hubo error y el PID corresponde al proceso hijo
            int i = 1;  // inicia i como 1
            while(i<10){  // Mientras i < 10
                printf("\t\t Tarea del proceso hijo: %d\n", i++); // contador para el proceso hijo
                sleep(1);  // Espera una unidad de tiempo
            }
            exit(1);  // Sal

    default: printf("Codigo del padre \n");   // Si el PID es del proceso padre
             died = wait(&status);  // wait toma por parámetro un puntero a un entero que contendrá el estado de salida de ese programa. 
                                    //Devuelve el ID de proceso del hijo que terminó.
             printf("Termino el proceso hijo %d \n", died);  // imprimir el PID del proceso hijo que acabo

    }

    return(0);  // termina el programa
}
