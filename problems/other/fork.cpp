#include<stdio.h>
#include<iostream>
#include<stdlib.h>
#include<unistd.h>

using namespace std;

int main() {
    printf("Test at first.");
    fork();
    printf("Test after fork.");
    
    return 0;
}
