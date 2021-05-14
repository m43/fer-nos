#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>

#define MAXREAD 20 /* najveca duljina poruke*/

int main(void) {
    int pfd;
    char buf[MAXREAD] = "";
    char message[] = "Kroz cijev!";

    unlink("./cjev");

    if (mknod("./cjev", S_IFIFO | 00600, 0) == -1)
        exit(1);

    switch (fork()) {
        case -1: /* dijete nije kreirano*/
            exit(1);

        case 0:/* dijete cita */
            pfd = open("./cjev", O_RDONLY);
            (void) read(pfd, buf, MAXREAD);
            puts(buf);
            exit(0);

        default:/* roditelj pise */
            pfd = open("./cjev", O_WRONLY);
            (void) write(pfd, message, strlen(message) + 1);
            wait(NULL);/* roditelj ceka da dijete zavrsi*/

    }
    return 0;
}