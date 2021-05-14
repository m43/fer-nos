#include "a.h"

/**
 * Program that models cars.
 *
 * @param argc Must be 3
 * @param argv argv[1] - car_id, argv[2] - car direction string (as in "a.h")
 */
int main(int argc, char const *argv[]) {
    // Parse program arguments
    if (argc != 3) {
        perror("car needs to have argc==2!");
    }
    long car_id = atoi(argv[1]);
    char car_direction[strlen(argv[2]) + 1];
    memcpy(car_direction, argv[2], strlen(argv[2]) + 1);

    // Init
    struct my_msgbuf buf;
    srand(time(NULL) + car_id);
    init_queues();


    // 1. Register for a ticket
    buf.mtype = car_id;
    memcpy(buf.mtext, car_direction, strlen(car_direction) + 1);
    if (msgsnd(register_id, (struct msgbuf *) &buf, strlen(car_direction) + 1, 0) == -1) {
        perror("Car: msgsnd at register");
        exit(1);
    }
    printf("Car %s %s waiting for the ticket\n", argv[2], argv[1]);

    // 2. Wait for ticket and then cross the bridge
    if (msgrcv(receival_id, (struct msgbuf *) &buf, 1, car_id, 0) == -1) {
        perror("Car: msgrcv at receive");
        exit(1);
    }

    // 3. Crossing the bridge
    printf("Car %s %s crossing the bridge\n", argv[2], argv[1]);
    long sleep_ms = rand() % 2001 + 1000;
    nanosleep((const struct timespec[]) {{sleep_ms/1000, sleep_ms%1000 * 1000000}}, NULL);

    // 4. Tell the semaphore that you crossed the bridge
    buf.mtype = car_id;
    if (msgsnd(crossed_id, (struct msgbuf *) &buf, 1, 0) == -1) {
        perror("Car: msgsnd at bridge crossed");
        exit(1);
    }
    printf("Car %s %s crossed the bridge\n", argv[2], argv[1]);
    return 0;
}



