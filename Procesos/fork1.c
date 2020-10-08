#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>


int main(void){

	int fpid; // define fpid como entero

	fpid = fork();     // fork() crea un proceso y almacena a su ID en fpid

	printf("ID del proceso: %d\n", fpid);   // Imprime el ID del proceso

	if (fpid == 0){  // si fpid es cero es el proceso hijo
		// Se crea el proceso hijo
		printf("Proceso hijo \n");
	}
	else {  // si fpid no es cero es un proceso padre
		//Ejecuta la continuacion del proceso padre]
		printf("Proceso padre \n");
	}

	return(0);
}