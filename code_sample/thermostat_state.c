#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_URL_LENGTH 256

void process_json_response(const char *json_response) {
    // Print only the JSON response
    printf("%s\n", json_response);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <temperature_controller_url>\n", argv[0]);
        return EXIT_FAILURE;
    }

    char temperature_controller_url[MAX_URL_LENGTH];
    strncpy(temperature_controller_url, argv[1], sizeof(temperature_controller_url) - 1);
    temperature_controller_url[sizeof(temperature_controller_url) - 1] = '\0';

    // Receive information from the temperature controller
    //printf("Requesting information from temperature controller at URL: %s\n", temperature_controller_url);

    // Create a pipe for communication between parent (Raspberry Pi) and child (curl)
    int pipe_fd[2];
    if (pipe(pipe_fd) == -1) {
        perror("pipe");
        return EXIT_FAILURE;
    }

    pid_t child_pid = fork();

    if (child_pid == -1) {
        perror("fork");
        return EXIT_FAILURE;
    }

    if (child_pid == 0) {
        // Child process (curl)
        close(pipe_fd[0]);  // Close the read end of the pipe

        // Redirect stdout to the write end of the pipe
        dup2(pipe_fd[1], STDOUT_FILENO);
        close(pipe_fd[1]);

        // Execute curl
        execl("/bin/curl", "/bin/curl", temperature_controller_url, NULL);

        // If execl fails
        perror("execl");
        exit(EXIT_FAILURE);
    } else {
        // Parent process (Raspberry Pi)
        close(pipe_fd[1]);  // Close the write end of the pipe

        // Read the JSON response from the pipe
        char buffer[4096];
        ssize_t bytesRead = read(pipe_fd[0], buffer, sizeof(buffer));
        close(pipe_fd[0]);

        if (bytesRead == -1) {
            perror("read");
            return EXIT_FAILURE;
        }

        buffer[bytesRead] = '\0';

        // Wait for the child process to finish
        int status;
        waitpid(child_pid, &status, 0);

        if (WIFEXITED(status) && WEXITSTATUS(status) == 0) {
            // If the child process (curl) exited successfully
            process_json_response(buffer);
        } else {
            fprintf(stderr, "Error: Failed to execute curl command\n");
            return EXIT_FAILURE;
        }
    }

    return EXIT_SUCCESS;
}
