#include "a.h"

/**
 * This is the entry point for the demo program for taks A.
 * It creates a traffic semaphore process and a random
 * number of cars. This program will terminate when all
 * child processes finish.
 */
int main(void) {
    printf("Entry: Lab 1a demo started.\n");

    // init randomness and pick n_cars randomly
    srand(time(NULL));
    unsigned int n_cars = rand() % (MAX_CARS - MIN_CARS + 1) + MIN_CARS;
    printf("Entry: will create %u cars\n", n_cars);

    // Create the traffic semaphore process
    switch (fork()) {
        case -1:
            perror("Entry: Could not run the traffic semaphore!");
            exit(1);
        case 0:
            execl("./a_semaphore", "semaphore", NULL);
            perror("Entry: Problem with ./a_semaphore");
            exit(1);
        default:
            break;
    }

    // Create all cars
    for (unsigned int i = 0; i < n_cars; i++) {
        char car_id[10], car_direction[100];
        sprintf(car_id, "%u", i + 1);

        // Pick direction randomly
        if (rand() % 2 == 0) {
            memcpy(car_direction, RIGHT, strlen(RIGHT) + 1);
        } else {
            memcpy(car_direction, LEFT, strlen(LEFT) + 1);
        }

        // Create process for car
        switch (fork()) {
            case -1:
                perror("Entry: New car process could not be created!");
                break;
            case 0:
                execl("./a_car", car_id, car_id, car_direction, NULL);
                perror("Entry: Problem with ./a_car");
                exit(1);
            default:
                continue;
        }
    }

    // Wait for all children to terminate
    pid_t wpid;
    int status = 0;
    while ((wpid = wait(&status)) > 0);

    printf("Entry: Lab 1a demo finished.\n");
    return 0;
}