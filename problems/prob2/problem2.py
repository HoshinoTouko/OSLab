"""
@File: problem2.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2017, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-05-29 10:14
@Desc: 
"""
from prettytable import PrettyTable

import os


class Memory:
    def __init__(self, filename):
        self.blocks = []
        self.processes = []
        with open(filename, 'r') as fi:
            lines = fi.readlines()
        for line in lines:
            data = line.split()
            self.blocks.append(MemBlock(data[0], data[1]))
        self.auto_adjust()

    def clear(self):
        os.system('cls')

    def add_process(self, require_mem):
        for block in self.blocks:
            if block.free_space >= require_mem:
                process = Process(block.start_addr, require_mem)
                self.processes.append(process)
                block.start_addr += require_mem
                block.free_space -= require_mem
                print('Add to block %d, start at: %d require: %d' %
                      (self.blocks.index(block), process.start_addr, process.require_mem))
                self.auto_adjust()
                break
        print('----------- No space can be given.')

    def release_process(self, release_index):
        if release_index > len(self.processes)-1:
            print('Index invalid.')
            return
        process = self.processes.pop(release_index)
        self.blocks.append(MemBlock(process.start_addr, process.require_mem))
        self.auto_adjust()

    def run_command(self):
        while True:
            try:
                line = input(
                    'Show memory(M)  '
                    'Show process(P)  '
                    'Add process(A `require_mem`)  '
                    'Release process(R `process_id`)  '
                    'End(E)\n'
                )
                command = line.split()
                if command[0] == 'E':
                    # Command 'END'
                    break
                elif command[0] == 'M':
                    # Command 'Show memory'
                    self.clear()
                    self.show_mem()
                elif command[0] == 'P':
                    # Command 'Show process'
                    self.clear()
                    self.show_process()
                elif command[0] == 'A':
                    if len(command) >= 1:
                        require_mem = int(command[1])
                        self.clear()
                        self.add_process(require_mem)
                        self.show_mem()
                    else:
                        self.clear()
                        print('No require mem')
                elif command[0] == 'R':
                    if len(command) >= 1:
                        release_index = int(command[1])
                        self.clear()
                        self.release_process(release_index)
                        self.show_mem()
                    else:
                        self.clear()
                        print('No release index')
                else:
                    continue
            except Exception as e:
                print(str(e))
                continue

    def auto_adjust(self):
        while True:
            reload = False

            self.blocks = sorted(self.blocks, key=lambda x: x.free_space)
            self.blocks = sorted(self.blocks, key=lambda x: x.start_addr)
            for block_num in range(len(self.blocks) - 1):
                if self.blocks[block_num].free_space == 0:
                    self.blocks.pop(block_num)
                    reload = True
                    break
                if self.blocks[block_num].start_addr + \
                        self.blocks[block_num].free_space > self.blocks[block_num + 1].start_addr:
                    exit('Block %d illegal!' % block_num)
                # Combine
                if self.blocks[block_num].start_addr + \
                        self.blocks[block_num].free_space == self.blocks[block_num + 1].start_addr:
                    self.blocks[block_num].free_space += self.blocks[block_num + 1].free_space
                    self.blocks.pop(block_num + 1)
                    reload = True
                    break
            if not reload:
                break

    def show_mem(self):
        count = 0
        print('Memory block table')
        table = PrettyTable(['No.', 'Start address', 'Free space'])
        for block in self.blocks:
            table.add_row([count, block.start_addr, block.free_space])
            count += 1
        print(table)

    def show_process(self):
        count = 0
        print('Process table')
        table = PrettyTable(['No.', 'Start address', 'Require space'])
        for process in self.processes:
            table.add_row([count, process.start_addr, process.require_mem])
            count += 1
        print(table)


class MemBlock:
    def __init__(self, start_addr, free_space):
        self.start_addr = int(start_addr)
        self.free_space = int(free_space)


class Process:
    def __init__(self, start_addr, require_mem):
        self.start_addr = start_addr
        self.require_mem = require_mem


if __name__ == '__main__':
    memory = Memory('mem.txt')
    memory.show_mem()
    memory.run_command()
