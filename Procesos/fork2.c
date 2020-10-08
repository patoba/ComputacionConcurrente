#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h> 


int main(void){   // Inicia el programa

	int i = 1; // Inicia un contador
	
	switch(fork()){  // switch es una manera de anidar condicionales
		case -1:   // cuando fork tiene un error en generar un proceso regresa -1
		// Codigo para el error
			perror("Error al crear el proceso"); // imprime que ha ocurrido un error
			exit(-1); // termina el codigo por error
			break;
		case 0:  // Cuando fork regresa 0 es que se gener'o un proceso hijo
		// codigo para el proceso hijo
			while(i<=10){
				sleep(1);  // espera una unidad de tiempo
				printf("\t Soy el proceso hijo: %d\n", i++);  // imprime el contador del proceso hijo
			}
			break; // sal de esta seccion 

		default: // para todos los demas casos
		// codigo para el padre
			while(i<=10){  // mientras i sea menor que 10
				printf("Soy el proceso padre: %d\n", i++);  // imprime el contador del proceso padre
				sleep(1);  // espera una unidad de tiempo
			}

	}
	return(0);   // termina el programa y regresa 0
}