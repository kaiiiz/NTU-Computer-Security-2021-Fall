#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 0x200
#define FILENAME_TEMPLATE "/tmp/filenote-XXXXXX"

FILE *fp;
char *note_buf;

void init_proc()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    note_buf = (char*) malloc(BUF_SIZE);
}

void print_menu()
{
    puts("----- FILE Note -----");
    puts("1) create note");
    puts("2) write note");
    puts("3) save note");
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
            fp = fdopen(tmp_fd, "w");
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
    fwrite(note_buf, 1, BUF_SIZE, fp);    
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
        default:
            exit(0);
            break;
        }
    }    
    return 0;
}
