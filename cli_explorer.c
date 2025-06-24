#include <ncurses.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define MAX_FILES 1024
char *files[MAX_FILES];
int file_count = 0;
char cwd[1024];

void list_files() {
    file_count = 0;
    getcwd(cwd, sizeof(cwd));
    DIR *dir = opendir(cwd);
    if (!dir) return;

    struct dirent *entry;
    while ((entry = readdir(dir)) && file_count < MAX_FILES) {
        files[file_count++] = strdup(entry->d_name);
    }
    closedir(dir);
}

void free_files() {
    for (int i = 0; i < file_count; i++)
        free(files[i]);
}

void rename_file(const char *old_name) {
    echo();
    char new_name[256];
    mvprintw(file_count + 3, 0, "Rename to: ");
    getnstr(new_name, 255);
    noecho();

    if (strlen(new_name) > 0) {
        if (rename(old_name, new_name) == 0) {
            mvprintw(file_count + 4, 0, "Renamed successfully.");
        } else {
            mvprintw(file_count + 4, 0, "Failed to rename.");
        }
    } else {
        mvprintw(file_count + 4, 0, "Name cannot be empty.");
    }
    getch();
}

void delete_file(const char *path) {
    struct stat st;
    if (stat(path, &st) != 0) return;

    int status = S_ISDIR(st.st_mode) ? rmdir(path) : remove(path);
    if (status == 0) {
        mvprintw(file_count + 3, 0, "Deleted successfully.");
    } else {
        mvprintw(file_count + 3, 0, "Failed to delete.");
    }
    getch();
}

void open_file(const char *path) {
    pid_t pid = fork();
    if (pid == 0) {

        fclose(stdin);
        fclose(stdout);
        fclose(stderr);

        // Choose platform-specific file opener
        #ifdef __APPLE__
            execlp("open", "open", path, NULL); // macOS
        #else
            execlp("xdg-open", "xdg-open", path, NULL); // Linux
        #endif

  
        exit(1);
    }
}

void explorer() {
    int ch, selected = 0;
    initscr();
    noecho();
    cbreak();
    keypad(stdscr, TRUE);

    while (1) {
        clear();
        mvprintw(0, 0, "CLI File Explorer - Current Dir: %s", cwd);
        for (int i = 0; i < file_count; i++) {
            if (i == selected) attron(A_REVERSE);
            mvprintw(i + 1, 0, "%s", files[i]);
            if (i == selected) attroff(A_REVERSE);
        }

        mvprintw(file_count + 2, 0, "[Enter] Open | [r] Rename | [d] Delete | [q] Quit");
        ch = getch();

        char path[2048];
        snprintf(path, sizeof(path), "%s/%s", cwd, files[selected]);

        if (ch == 'q') break;
        else if (ch == KEY_UP && selected > 0) selected--;
        else if (ch == KEY_DOWN && selected < file_count - 1) selected++;
        else if (ch == '\n') {
            struct stat st;
            stat(path, &st);
            if (S_ISDIR(st.st_mode)) {
                chdir(path);
                free_files();
                list_files();
                selected = 0;
            } else {
                open_file(path);
            }
        } else if (ch == 'r') {
            rename_file(path);
            free_files();
            list_files();
        } else if (ch == 'd') {
            delete_file(path);
            free_files();
            list_files();
            if (selected >= file_count) selected = file_count - 1;
        }
    }
    endwin();
}

int main() {
    list_files();
    explorer();
    free_files();
    return 0;
}
