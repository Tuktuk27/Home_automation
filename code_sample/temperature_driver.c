#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    // Update this part to manage errors
    //if (argc != 3) {
    //    fprintf(stderr, "Usage: %s <controller_url> <temperature>\n", argv[0]);
    //    return EXIT_FAILURE;
    //}
    
    char *input = strdup(argv[1]);  // Allocate dynamic memory for the URL
    
    char *controller_url = strtok(input,",");

    char *temp = strtok(NULL,",");

    //char *controller_url = strdup(argv[1]);  // Allocate dynamic memory for the URL
    if (controller_url == NULL) {
        perror("strdup");
        free(input);
        return EXIT_FAILURE;
    }

    //char *temperature = strdup(argv[2]);  // Allocate dynamic memory for the temperature
    if (temp == NULL) {
        perror("strdup");
        // Free the previously allocated memory
        free(input);
        return EXIT_FAILURE;
    }

    char temperature[20]; // Adjust the size as needed
    sprintf(temperature, "temperature=%s", temp);

    // Transmit the temperature to the controller at the specified URL
    printf("Transmitting temperature '%s' to controller at URL: %s\n", temperature, controller_url);

    // Send an HTTP request to the specified URL with the temperature
    char *curl_args[] = {"/bin/curl", "-X", "POST", controller_url, "--data", temperature, NULL};

    if (execv("/bin/curl", curl_args) == -1) {
        perror("execv");
        fprintf(stderr, "Error: Failed to execute curl command\n");
        return EXIT_FAILURE;
    }

    // This point is reached only if execv fails
    fprintf(stderr, "Error: Unexpected control flow\n");

    free(input);
    //free(controller_url);  // Free the allocated memory for the URL
    //(temperature);     // Free the allocated memory for the temperature
    return EXIT_FAILURE;    // Return a non-zero value to indicate an error
}
