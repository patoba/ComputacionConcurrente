#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h> 


int main(void){

	int i; // Inicia un contador
	int padre = 1; //inicializa padre con 1
	
	for (i=1;i<=3;i++){   // para i entre 1 y 3 con pasos de 1
		if (fork() == 0) // si el fork regresa 0 es el proseso hijo
		{
			printf("\t Proceso hijo %d, con ID: %d y padre ID: %d\n", i, getpid(), getppid() );  
			// imprime el IP del proceso hijo con getpid() y el del proceso padre con getppid()
			padre = 0;  // no es el padre
		}
		else { // Si fork regresa cualquier otra cosa es el proceso padre
			printf("Proceso padre con ID: %d \n", getpid()); // Muestra el ID del proceso con getpid()
			padre = 1;  // es el padre
		}
	}
	return(0);   // termina el programa y regresa 0
}