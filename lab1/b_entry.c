#include <stdio.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>
#include <unistd.h>
#include<fcntl.h>

#include "b.h"

int n;
struct db_entry *database;

/**
 * Help function to close the shared memory.
 * @param failure dummy variable needed for using sigint
 */
void retreat(int failure) {
    int err = munmap(database, n * sizeof(struct db_entry));
    if (err != 0) {
        printf("UnMapping Failed!\n");
        exit(1);
    }
    exit(0);
}

/**
 * This is the entry point for the demo program for taks B.
 */
int main(void) {
    printf("Main: Lab 1b demo started.\n");

    // Init randomness and pick n_cars randomly
    srand(time(NULL));
    int n = get_random_int_in_interval(MIN_PROCESSES, MAX_PROCESSES);
    printf("Main: will create %u processes\n", n);


    // Create shared db
    database = mmap(
            NULL,
            n * sizeof(struct db_entry),
            PROT_READ | PROT_WRITE,
            MAP_SHARED | MAP_ANONYMOUS,
            0, 0
    );
    if (database == MAP_FAILED) {
        printf("mmap failed :-(");
        exit(0);
    }
    sigset(SIGINT, retreat); // If interupted, queues must be closed!

    // Init db
    for (int i = 0; i < n; i++) {
        database[i].pid = i;
        database[i].logical_clock = 0;
        database[i].n_critical = 0;
    }

    // Create all pipes, n*(n-1) in total
    int pipes[n][n][2];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) continue;

            if (pipe(pipes[i][j]) == -1) {
                printf("Main: Could not create pipe %d-->%d! Terminating\n", i, j);
                exit(-1);
            }

            // Setup non blocking reads
            fcntl(pipes[i][j][PIPE_READ], F_SETFL, fcntl(pipes[i][j][PIPE_READ], F_GETFL) | O_NONBLOCK);

            if (DEBUG) {
                printf("%d-->%d, %d in f%d   ", i, j, pipes[i][j][0], fcntl(pipes[i][j][0], F_GETFL));
                printf("%d-->%d, %d out f%d\n", i, j, pipes[i][j][1], fcntl(pipes[i][j][1], F_GETFL));
            }
        }
    }

    // Create all processes
    for (int pid = 0; pid < n; pid++) {
        int out_pipes[n], in_pipes[n];

        switch (fork()) {
            case -1:
                perror("Main: New process could not be created!");
                break;
            case 0:
                // Prepare pipes for this process
                out_pipes[pid] = -1;
                in_pipes[pid] = -1;
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        if (i == j) continue;
                        if (i == pid) {
                            out_pipes[j] = pipes[i][j][PIPE_WRITE];
                        } else {
                            if (close(pipes[i][j][PIPE_WRITE]) == -1) {
                                printf("pid=%02d: Could not close a pipe %d-->%d. Terminating.", pid, i, j);
                                exit(-1);
                            }
                        }
                        if (j == pid) {
                            in_pipes[i] = pipes[i][j][PIPE_READ];
                        } else {
                            if (close(pipes[i][j][PIPE_READ]) == -1) {
                                printf("pid=%02d: Could not close a pipe %d-->%d. Terminating.", pid, i, j);
                                exit(-1);
                            }
                        }
                    }
                }

                // Run the process with given pid and respective pipes.
                start_process_loop(pid, n, database, out_pipes, in_pipes, DEBUG);
                exit(0);
            default:
                continue;
        }
    }

    // Wait for all children to terminate
    pid_t wpid;
    int status = 0;
    while ((wpid = wait(&status)) > 0);

    // Close the shared memory
    retreat(0);

    printf("Main: Lab 1b demo finished.\n");
    return 0;
}




