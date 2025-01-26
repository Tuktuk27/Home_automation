#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    // Update this part to manage errors
    //if (argc != 3) {
    //    fprintf(stderr, "Usage: %s <controller_url> <action>\n", argv[0]);
    //    return EXIT_FAILURE;
    //}

    char *input = strdup(argv[1]);  // Allocate dynamic memory for the URL
    
    if (input == NULL) {
        perror("strdup");
        return EXIT_FAILURE;
    }

    char *controller_url = strtok(input,",");
    //char *command = strtok(NULL,",");

    char* command = strtok(NULL,",");

    char action[20]; // Adjust the size as needed

    if (strcmp(command, "on") == 0) {
        sprintf(action, "action=on");
    } else if (strcmp(command, "off") == 0) {
        sprintf(action, "action=off");
    } else {
        // Handle the case when command is neither "on" nor "off"
        printf("Invalid command\n");
        return 1; // might need to handle this appropriately
    }

    // Transmit the action to the controller at the specified URL
    printf("\nTransmitting action '%s' to controller at URL: %s\n", action, controller_url);

    // Send an HTTP request to the specified URL with the action

    char *curl_args[] = {"/bin/curl", "-X", "POST", "-d", action, controller_url, NULL};

    if (execv("/bin/curl", curl_args) == -1) {
        perror("execv");
        fprintf(stderr, "\nError: Failed to execute curl command\n");
        return EXIT_FAILURE;
    }

    // This point is reached only if execv fails
    fprintf(stderr, "\nError: Unexpected control flow\n");

    free(controller_url);  // Free the allocated memory
    
    return EXIT_FAILURE;
}
