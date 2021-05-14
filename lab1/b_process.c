#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <unistd.h>

#include "b.h"

void print_database(struct db_entry *db, int n) {
    for (int i = 0; i < n; i++) {
        printf("pid:%02d logclk:%04d c:%d\n", db[i].pid, db[i].logical_clock, db[i].n_critical);
    }
}

void sleep_ms(int ms) {
    int seconds = ms / 1000;
    ms = ms % 1000;
    nanosleep((const struct timespec[]) {{seconds, ms * 1000000}}, NULL);
}

int get_random_int_in_interval(int mini, int maxi) {
    return rand() % (maxi - mini + 1) + mini;
}

void write_wrapper(int pid, int pipe, struct PipeMessage msg, int i) {
    if (write(pipe, &msg, sizeof(msg)) == -1) {
        printf("pid=%d: Failed to send request to %d. Terminating\n", pid, i);
        exit(-1);
    }
}

void start_process_loop(int pid, int n, struct db_entry *db, int *out_pipes, int *in_pipes, int debug) {
    if (debug) printf("pid=%d: Started\n", pid);

    // Init logical clock
    int logical_clock;
    if (INIT_LOGICAL_CLOCKS_RANDOMLY == 1) {
        srand(pid);
        logical_clock = rand() % 30 + 10;
    } else {
        logical_clock = 0;
    }

    // structure to remember which processes to notify
    int pids_to_notify[n - 1];
    int n_pids_to_notify = 0;

    // Ask N_CRITICAL times for to use the database
    for (int c = 0; c < N_CRITICAL; c++) {

        // Sleep for a random amount of time
        if (debug) printf("pid=%d: Gonna sleep now.\n", pid);
        long random_sleep_ms = get_random_int_in_interval(MIN_SLEEP_MS, MAX_SLEEP_MS * (1 + pid));
        sleep_ms(random_sleep_ms);

        // Start requesting db access from all processes
        if (debug) printf("pid=%d: I want to use the database\n", pid);
        struct PipeMessage myRequest = {REQUEST, logical_clock};
        for (int i = 0; i < n; i++) {
            if (i == pid) continue;
            write_wrapper(pid, out_pipes[i], myRequest, i);
        }

        // Collect all responses
        int n_responses = 0;
        struct PipeMessage inbox;
        if (debug) printf("pid=%d: Waiting for responses\n", pid);
        while (n_responses < n - 1) {
            // loop through all processes until all responses arrive. also process requests
            for (int i = 0; i < n; i++) {
                if (i == pid) continue;

                // Check if process i has any message for me
                int bytes_read = read(in_pipes[i], &inbox, sizeof(inbox));
//                if (bytes_read == -1) {
//                    printf("pid=%d: Error while trying to read from %d. Terminating\n", pid, i);
//                    exit(-1);
//                } else
                if (bytes_read > 0) {
                    if (debug)
                        printf("pid=%d: New message in inbox from %d, its a %s\n", pid, i,
                               inbox.type == REQUEST ? "request" : "response");
                    if (inbox.type == REQUEST) {
                        if (inbox.timestamp < myRequest.timestamp ||
                            inbox.timestamp == myRequest.timestamp && i > pid) {
                            write_wrapper(pid, out_pipes[i], (struct PipeMessage) {RESPONSE, -1}, i);
                            if (debug) printf("pid=%d: Told him to go ahead\n", pid);
                        } else {
                            pids_to_notify[n_pids_to_notify++] = i;
                            if (debug) printf("pid=%d: I'll notify him later on\n", pid);
                        }
                        logical_clock = logical_clock > inbox.timestamp ? logical_clock + 1 : inbox.timestamp + 1;
                    } else {
                        logical_clock++;
                        n_responses++;
                    }
                    if (debug)
                        printf("pid=%d: Got %d responses and %d pids to notify\n", pid, n_responses,
                               n_pids_to_notify);

                }
            }

            // Sleep a bit till the responses arrive
            sleep_ms(30);
        }

        // Enter the critical code as all the responses are collected
        if (debug) printf("pid=%d: Got all responses\n", pid);
        db[pid].logical_clock = logical_clock;
        db[pid].n_critical++;
        printf("pid=%d: database at local_logical_time=%d\n", pid, logical_clock);
        print_database(db, n);
        if (!debug) printf("\n");

        // Notify the process that are waiting for my response.
        if (debug) printf("pid=%d: Done with critical code. Gonna notify %d processes now\n", pid, n_pids_to_notify);
        for (int p = 0; p < n_pids_to_notify; p++) {
            write_wrapper(pid, out_pipes[pids_to_notify[p]], (struct PipeMessage) {RESPONSE, -1}, pids_to_notify[p]);
        }
        n_pids_to_notify = 0;
        if (debug) printf("pid=%d: Notified everybody.\n", pid);
    }

    // Setup timing
    struct timeval tval_before, tval_after;
    gettimeofday(&tval_before, NULL);
    gettimeofday(&tval_after, NULL);
    long time_elapsed_us = 0;

    // Check inbox. Quit if inbox empty for TIMEOUT_TILL_QUIT_S. Process only requests (no responses should arrive!)
    if (debug) printf("pid=%d: No more critical code for me.\n", pid);
    struct PipeMessage inbox;
    while (time_elapsed_us <= TIMEOUT_TILL_QUIT_S * 1000 * 1000) {
        for (int i = 0; i < n; i++) {
            if (i == pid) continue;
            int bytes_read = read(in_pipes[i], &inbox, sizeof(inbox));
            if (bytes_read > 0) {
                if (inbox.type != REQUEST) {
                    printf("pid=%d: Got invalid response message from %d.\n", pid, i);
                }
                write_wrapper(pid, out_pipes[i], (struct PipeMessage) {RESPONSE, -1}, i);
                logical_clock = logical_clock > inbox.timestamp ? logical_clock + 1 : inbox.timestamp + 1;
                gettimeofday(&tval_before, NULL);
                if (debug) printf("pid=%d: Told %d to go ahead\n", pid, i);
                logical_clock = logical_clock > inbox.timestamp ? logical_clock + 1 : inbox.timestamp + 1;
            }
        }
        sleep_ms(50);

        gettimeofday(&tval_after, NULL);
        time_elapsed_us =
                (tval_after.tv_sec - tval_before.tv_sec) * 1000000 + (tval_after.tv_usec - tval_before.tv_usec);
    }

    // Timeout. Quit now.
    printf("pid=%d: Got no messages for %d seconds, gonna quit with status code 0. Final local time: %d\n", pid,
           TIMEOUT_TILL_QUIT_S, logical_clock);
    exit(0);
}