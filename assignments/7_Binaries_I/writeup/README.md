# Writeup 7 - Binaries I

Name: Daniel Kelly
Section: 0101

I pledge on my honor that I have not given or received any unauthorized
assistance on this assignment or examination.

Digital acknowledgement: Daniel Kelly

## Assignment Writeup

### Part 1 (90 Pts)

*Put your code here as well as in main.c*
```c
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
```

### Part 2 (10 Pts)

This program stores the value `0x1ceb00da` in one variable, which I am calling b, and the value `0xfeedface` in another variable, which I am calling a.
It prints the signed integer value of a, showing `a = -17958194`, and the signed integer value of b, showing `b = 485163226`.
It then swaps a and b using the XOR swap algorithm, and prints the values of a and b again, showing `a = 485163226` and `b = -17958194` respectively.
