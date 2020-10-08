#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main(void){

	printf("ID de proceso: %d \n", getpid());  // getpid regresa el ID del proceso en ejecucion
	printf("ID de proceso padre: %d\n", getppid());  // getpid regresa el ID del proceso  padre que creo el proceso en ejecucion
	printf("ID de usuario propietario: %d\n", getuid()); // getuid() regresa el ID del propietario que inicio el proceso



	return(0);  // termina el codigo y regresa 0
}