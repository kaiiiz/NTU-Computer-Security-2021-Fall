#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SECRET_SIZE 0x20
#define BUF_SIZE 0x200
#define FILENAME_TEMPLATE "/tmp/filenote-XXXXXX"

FILE *fp;
char *note_buf;
char *debug_secret;

void init_proc()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    debug_secret = (char*) malloc(SECRET_SIZE);
    note_buf = (char*) malloc(BUF_SIZE);
    printf("Here is a gift for you: %p\n", note_buf);
}

void print_menu()
{
    puts("----- FILE Note -----");
    puts("1) create note");
    puts("2) write note");
    puts("3) save note");
    puts("4) load note");
    printf("> ");
}

int read_choice()
{
    char buf[0x10];
    scanf("%9s", buf);
    getc(stdin);
    return atoi(buf);
}

void create_note()
{
    int tmp_fd;
    if (!fp) {
        char tmpfile_name[sizeof(FILENAME_TEMPLATE) + 1];
        strncpy(tmpfile_name, FILENAME_TEMPLATE, sizeof(FILENAME_TEMPLATE) + 1);
        tmp_fd = mkstemp(tmpfile_name);
        if (tmp_fd > 0) {
            fp = fdopen(tmp_fd, "rw");
        } else {
            perror("failed to mkstemp()");
            exit(0);
        }
    } else {
        exit(0);
    }
}

void write_note()
{
    printf("data> ");
    gets(note_buf);
}

void save_note()
{
    puts("Not implemented yet.");
}

void load_note()
{
    fscanf(fp, "%s", note_buf);
}

void _check_debug_secret()
{
    if (!strcmp(debug_secret, "gura_50_cu73")) {
        system("/bin/sh");
    }
}

int main() {
    init_proc();
    while (1) {
        print_menu();
        switch (read_choice()) {
        case 1:
            create_note();
            break;
        case 2:
            write_note();
            break;
        case 3:
            save_note();
            break;
        case 4:
            load_note();
            break;
        default:
            exit(0);
            break;
        }
        _check_debug_secret();
    }    
    return 0;
}
