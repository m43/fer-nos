/**
 * This file contains constants, function declarations and
 * all global variables used by programs for task B.
 */


#ifndef FER_NOS_B_H
#define FER_NOS_B_H

// Global constants
#define DEBUG 0 // 0 - no debugging messages, 1 - print debugging messages
#define MIN_PROCESSES 3
#define MAX_PROCESSES 10
#define MIN_SLEEP_MS 200
#define MAX_SLEEP_MS 1000
#define INIT_LOGICAL_CLOCKS_RANDOMLY 1
#define N_CRITICAL 5
#define TIMEOUT_TILL_QUIT_S 20

#define PIPE_READ 0
#define PIPE_WRITE 1

// database entry structure
struct db_entry {
    int pid;
    int logical_clock;
    int n_critical;
};

// All pipe messages will be either a request or a response
enum PipeMessageType {
    REQUEST = 0, RESPONSE = 1
};

// A pipe message has a type and a timestamp
// In R&A I will use both when sending requests, and only the type without
// the timestamp when sending the response
struct PipeMessage {
    enum PipeMessageType type;
    int timestamp;
};

/**
 * Start a process that will write to the database with distributed synchronization
 * using pipes and the Ricarta i Agrawala protocol
 *
 * @param pid The id of this process
 * @param n The total number of processes that interact with the database
 * @param db pointer to shared memory with the database written in it
 * @param out_pipes Pipes used for writing messages to other processes
 * @param in_pipes Pipes used for reading messages from other processes
 * @param debug whether this process should print debug messages
 */
void start_process_loop(int pid, int n, struct db_entry *db, int *out_pipes, int *in_pipes, int debug);

/**
 * Print the content of the database
 *
 * @param db database
 * @param n number of entries in the database
 */
void print_database(struct db_entry *db, int n);

/**
 * Sleep for given amount of milliseconds
 * @param ms Milliseconds to sleep
 */
void sleep_ms(int ms);

/**
 * Get a random integer from given interval [mini, maxi]
 *
 * @param mini minimum
 * @param maxi maximum
 * @return a random integer
 */
int get_random_int_in_interval(int mini, int maxi);

/**
 * Help functino used for writing a PipeMessage to given pipe
 *
 * @param pid Source process id (for printing error messages)
 * @param pipe pipe to write to
 * @param msg the message object
 * @param i Target process id ((for printing error messages))
 */
void write_wrapper(int pid, int pipe, struct PipeMessage msg, int i);

#endif //FER_NOS_B_H
