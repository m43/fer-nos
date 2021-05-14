#include "a.h"

/**
 * This is the traffic semaphore program.
 */
int main(void) {
    // Init
    long total_collected_cars_count = 0;
    struct my_msgbuf buf; // Buffer used for all upcoming communication
    srand(time(NULL));
    init_queues();
    sigset(SIGINT, retreat); // If interupted, queues must be closed!


    printf("Traffic semaphore started\n");
    long n_left, left[MAX_CARS_ON_BRIDGE]; // Counter and car if list for left side
    long n_right, right[MAX_CARS_ON_BRIDGE]; // Counter and car if list for right side

    // Main semaphore loop. When loop exits, the sempahore will terminate.
    for (;;) {
        struct timeval tval_before, tval_after;
        time_t waiting_time_us = (rand() % 501 + 500) * 1000;
        gettimeofday(&tval_before, NULL);

        long time_elapsed_us;
        // This loop takes ticket registrations from register_id queue until:
        // 1. MAX_SEMAPHORE_WAITING_TIME_BEFORE_QUIT_IN_S is exceeded
        // 2. Current waiting_time_us is exceeded AND there are some registered tickets
        // 3. There are MAX_CARS_ON_BRIDGE registered cars for any of the two directions
        for (;;) {

            for (; n_left < MAX_CARS_ON_BRIDGE && n_right < MAX_CARS_ON_BRIDGE;) {
                if (msgrcv(register_id, (struct msgbuf *) &buf, sizeof(buf) - sizeof(buf.mtype), 0, IPC_NOWAIT) == -1)
                    break;

                printf("Semaphore: saw registration %ld\n", buf.mtype);

                if (strcmp(buf.mtext, LEFT)) {
                    left[n_left] = buf.mtype;
                    n_left++;
                } else if (strcmp(buf.mtext, RIGHT)) {
                    right[n_right] = buf.mtype;
                    n_right++;
                } else {
                    printf("Semaphore cannot understand direction '%s'", buf.mtext);
                }
            }

            gettimeofday(&tval_after, NULL);
            time_elapsed_us =
                    (tval_after.tv_sec - tval_before.tv_sec) * 1000000 + (tval_after.tv_usec - tval_before.tv_usec);

            if (time_elapsed_us > MAX_SEMAPHORE_WAITING_TIME_BEFORE_QUIT_IN_S * 1000 * 1000) {
                break;
            } else if (time_elapsed_us > waiting_time_us && (n_left > 0 || n_right > 0)) {
                break;
            }
        }
        printf("Semaphore - time elapsed: %05ldms\n", time_elapsed_us / 1000);


        // Pick direction and prepare cars. Reset counters
        long n_cars_to_cross = 0; // How many cars will cross this time
        long *cars_to_cross; // Which cars will cross the bridge
        if (n_left > 0 && n_left > n_right) {
            n_cars_to_cross = n_left;
            cars_to_cross = left;
            n_left = 0;
        } else if (n_right > 0) {
            n_cars_to_cross = n_right;
            cars_to_cross = right;
            n_right = 0;
        } else {
            // This means that the maximum waiting time was exceeded, so the semaphore terminates!
            break;
        }

        // Send tickets to cars that were picked
        for (int i = 0; i < n_cars_to_cross; i++) {
            printf("Semaphore: sending ticket to %ld\n", cars_to_cross[i]);
            buf.mtype = cars_to_cross[i];
            buf.mtext[0] = '\0';
            if (msgsnd(receival_id, (struct msgbuf *) &buf, 1, 0) == -1) {
                perror("Semaphore: msgsnd for ticket receival");
                exit(1);
            }
        }

        // Collect cars
        for (int i = 0; i < n_cars_to_cross; i++) {
            if (msgrcv(crossed_id, (struct msgbuf *) &buf, 1, 0, 0) == -1) {
                perror("Semaphore: msgrcv at crossed");
                exit(1);
            }
            total_collected_cars_count++;
            printf("Semaphore: collected car %ld\n", buf.mtype);
        }
        printf("Semaphore: collected all cars. nice\n");
    }

    // MAX_SEMAPHORE_WAITING_TIME_BEFORE_QUIT_IN_S was exceeded, semaphore gonna quit.
    printf("Traffic semaphore quit. Collected %ld cars in total.\n", total_collected_cars_count);
    retreat(0);

    return 0;
}
