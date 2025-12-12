// Rishabh Pandey, rp36723
#include <stdio.h>
#include <stdlib.h>

int global_var = 42;

int main(void) {
    int stack_var = 123;
    int *heap_var = malloc(sizeof(int));
    if (!heap_var) {
        perror("malloc");
        return 1;
    }
    *heap_var = 456;

    //print addresses of diff memory regions
    printf("STACK %p\n", (void*)&stack_var);
    printf("HEAP %p\n", (void*)heap_var);
    printf("GLOBAL %p\n", (void*)&global_var);
    printf("LIBC_PRINTF %p\n", (void*)&printf);
    printf("MAIN %p\n", (void*)&main);

    free(heap_var);
    return 0;
}