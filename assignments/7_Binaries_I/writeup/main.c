#include <stdio.h>

int main()
{
    // Assign values to a and b
    int b = 0x1ceb00da;
    int a = 0xfeedface;

    // Print the value of a
    printf("a = %d\n", a);

    // Print the value of b
    printf("b = %d\n", b);

    // Swap the values of a and b
    a ^= b;
    b ^=a;
    a ^= b;

    // Print the value of a
    printf("a = %d\n", a);

    // Print the value of b
    printf("b = %d\n", b);

    return 0;
}
