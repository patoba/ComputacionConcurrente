#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>   // Biblioteca estandar de llamadas al sistema

#include <string.h>  //


int main(void){

    int pid, pipefd[2];  // define a pid como un entero y pipe como un arreglo de dos numeros enteros

    float x, y;  // define x, y como flotantes (numeros reales)


    pipe(pipefd);  // pipe hace a la variable pipefd como el canal de comunicacion entre procesos
    pid = fork(); // haz el fork

    if (pid) {  // si pid es distinto de cero es el padre
        close(pipefd[0]);  //  bloquea pipefd[0] (el canal de lectura) para que no sea escrito por otro proceso mientras esta en uso
        printf("\n Soy el padre, dame un numero real:");
        scanf("%f", &x);  // entra input del usuario
        printf("\n");
        write(pipefd[1], &x, sizeof(float));  // escribe en pipefd[1] el valor de x como un float
    }
    else{
        printf("\n Soy el hijo, ");  
        close(pipefd[1]); // cierra pipefd[1] el canal de escritura
        read(pipefd[0], &y, sizeof(float));  // lee lo que hay en el canal de lectura
        printf(" mensaje recibido: %f \n\n", y);  // despliega el mensaje recibido
    }


    return(0);
}