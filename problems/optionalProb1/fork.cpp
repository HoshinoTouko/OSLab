#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <iostream>

using namespace std;

int main() {
    int pid;
    int localcount = 0;
    int sharedcount_instance = 5;
    int *sharedcount = &sharedcount_instance;
    cout<<"Process start."<<endl;
    pid = fork();

    if (pid == 0){
        localcount ++;
        *sharedcount = 10;

        cout<<"This is father process."<<endl;
        cout<<"Father localcount: "<<localcount<<endl;
        cout<<"Father sharedcount: "<<*sharedcount<<endl;
    }
    else{
        localcount ++;
        *sharedcount = 20;

        cout<<"This is child process, pid is "<<pid<<"."<<endl;
        cout<<"Child localcount: "<<localcount<<endl;
        try{
            cout<<"Child sharedcount: "<<*sharedcount<<endl;
        }
        catch (std::exception& e) {
            cout<<"Child process cannot share memory space with father process."<<endl;
        }
    }

    cout<<"Test after fork."<<endl;
    cin.get();
    
    return 0;
}
