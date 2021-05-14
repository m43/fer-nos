/**
 * This file contains constants, includes, functions and
 * all global variables used by programs for task A.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/time.h>
#include <signal.h>
#include <time.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

// Global constants
#define MAX_CARS 120
#define MIN_CARS 10
#define MAX_CARS_ON_BRIDGE 3
#define MAX_SEMAPHORE_WAITING_TIME_BEFORE_QUIT_IN_S 10
#define TICKET_REGISTRATION_QUEUE_KEY 720
#define TICKET_RECEIVAL_QUEUE_KEY 900
#define CROSSED_BRIDGE_QUEUE 1080
char LEFT[] = "--->";
char RIGHT[] = "<---";

/**
 * Buffer used when exchanging messages using message queues.
 */
struct my_msgbuf {
    long mtype;
    char mtext[200];
};

int register_id, receival_id, crossed_id;

/**
 * Help function to close all message queues.
 * @param failure dummy variable needed for using sigint
 */
void retreat(int failure) {
    if (
            msgctl(register_id, IPC_RMID, NULL) == -1 ||
            msgctl(receival_id, IPC_RMID, NULL) == -1 ||
            msgctl(crossed_id, IPC_RMID, NULL) == -1
            ) {
        perror("msgctl in retreat");
        exit(1);
    }
    exit(0);
}

/**
 * Help function used to check if all queues are created.
 */
void init_queues() {
    register_id = msgget(TICKET_REGISTRATION_QUEUE_KEY, 0600 | IPC_CREAT);
    receival_id = msgget(TICKET_RECEIVAL_QUEUE_KEY, 0600 | IPC_CREAT);
    crossed_id = msgget(CROSSED_BRIDGE_QUEUE, 0600 | IPC_CREAT);

    if (register_id == -1 || receival_id == -1 || crossed_id == -1) { /* connect to the queue */
        perror("msgget in init_queues");
        exit(1);
    }
}