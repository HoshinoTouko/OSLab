"""
@File: problem3.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-05-29 16:28
@Desc: 
"""
from prettytable import PrettyTable

import os


class HardDisk:
    def __init__(self):
        self.storage = ['0'] * 64
        self.files = []

    def clear(self):
        os.system('cls')

    def run_command(self):
        while True:
            try:
                line = input(
                    'Show storage(S)  '
                    'Show files(F)  '
                    'Add file(A `filename` `storage number`)  '
                    'Delete file(D `filename`)  '
                    'End(E)\n'
                )
                command = line.split()
                if command[0] == 'E':
                    # Command 'END'
                    break
                elif command[0] == 'S':
                    # Command 'Show memory'
                    self.clear()
                    self.show_storage()
                elif command[0] == 'F':
                    # Command 'Show process'
                    self.clear()
                    self.show_files()
                elif command[0] == 'A':
                    if len(command) >= 2:
                        filename = str(command[1])
                        storage_number = int(command[2])
                        self.clear()
                        self.distribute_storage(filename, storage_number)
                        self.show_storage()
                    else:
                        self.clear()
                        print('Illegal input')
                elif command[0] == 'D':
                    if len(command) >= 1:
                        filename = str(command[1])
                        self.clear()
                        self.delete_file(filename)
                        self.show_storage()
                    else:
                        self.clear()
                        print('Illegal input')
                else:
                    continue
            except Exception as e:
                print(str(e))
                continue

    def show_storage(self):
        print()
        print('Storage table.')
        table = PrettyTable(['Cylinder'] + list(map(str, range(8))))
        for i in range(0, 64, 8):
            table.add_row([str(int(1 + i / 8))] + self.storage[i:i + 8])
        print(table)

    def show_files(self):
        print()
        print('Files table')
        table = PrettyTable(['File name', 'Storage block number'])
        for file in self.files:
            table.add_row([file.name, str(file.storage_block_number)])
        print(table)

    def delete_file(self, name):
        print()
        print('Delete file %s......' % name)
        find = False
        for file in self.files:
            if file.name == name:
                find = True
                self.files.pop(self.files.index(file))
                for i in file.storage_block_number:
                    self.storage[i] = '0'
                break
        if find:
            print('Delete success!')
        else:
            print('Not found')

    def distribute_storage(self, name, storage_demand):
        print()
        print('Distribute storage %d for file %s......' % (storage_demand, name))
        # If storage is not enough, return.
        if self.storage.count('0') < storage_demand:
            print('No enough storage.')
            return

        storage_distributed = 0
        storage_block_number = []
        for i in range(len(self.storage)):
            if storage_distributed >= storage_demand:
                break
            if self.storage[i] == '0':
                self.storage[i] = '1'
                print('Cylinder %2d\t Head %2d\t Sector: %2d' %
                      HardDisk.get_storage_distribution(i))
                storage_distributed += 1
                storage_block_number.append(i)
        self.files.append(File(name, storage_block_number))

    @staticmethod
    def get_storage_distribution(storage_number):
        x = storage_number
        return x / 8 + 1, x / 4 % 2, x % 4


class File:
    def __init__(self, name, storage_block_number):
        self.name = name
        self.storage_block_number = storage_block_number


if __name__ == '__main__':
    hdd = HardDisk()
    hdd.show_storage()
    hdd.run_command()
