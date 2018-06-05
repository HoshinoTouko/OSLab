"""
@File: Problem1.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2017, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-05-28 21:15
@Desc: 
"""
# 时间片轮转算法
from collections import deque


class ProcessorDeque:
    def __init__(self):
        self.process = deque()
        self.finish = deque()
        self.pointer = 0
        self.length = 0

    def load_file(self, filename):
        with open(filename, 'r') as fi:
            lines = fi.readlines()
        count = 0
        for line in lines:
            process = Process(int(line))
            process.label = count
            count += 1
            self.process.append(process)

    def all_wait(self):
        list(map(lambda x: x.wait(), self.process))

    def show_all_process(self):
        for process in self.process:
            print(
                'Process: %3d;\t status: %s;\t Effective run time: %d;\t Already run time: %d;' %
                (process.label, process.status,
                 process.effective_run_times,
                 process.already_run_times)
            )

    def show_all_finished_process(self):
        for process in self.finish:
            print(
                'Process: %3d;\t status: %s;\t Effective run time: %d;\t Already run time: %d;' %
                (process.label, process.status,
                 process.effective_run_times,
                 process.already_run_times)
            )

    def start(self):
        count = 1
        while len(self.process) > 0:
            print('Iter %3d times....' % count)
            count += 1

            process = self.process.popleft()
            process.run()
            print('Process: %3d;\t status: Running;\t Effective run time: %d;\t Already run time: %d;' %
                (process.label,
                 process.effective_run_times,
                 process.already_run_times))
            self.all_wait()
            self.show_all_process()
            if process.status == Status.End:
                self.finish.append(process)
            else:
                self.process.append(process)
            print()
        print('Result ---------------------------------------------------------')
        self.show_all_finished_process()


class Processor:
    def __init__(self):
        self.process = []
        self.pointer = 0

    def pointer_add(self):
        self.pointer = (self.pointer + 1) % len(self.process)

    def load_file(self, filename):
        with open(filename, 'r') as fi:
            lines = fi.readlines()
        count = 0
        for line in lines:
            process = Process(int(line))
            process.label = count
            count += 1
            self.process.append(process)

    def show_all_process(self):
        for process in self.process:
            print(
                'Process: %d;\t status: %s;\t Effective run time: %d;\t Already run time: %d;' %
                (process.label, process.status,
                 process.effective_run_times,
                 process.already_run_times)
            )

    def check_all_end(self):
        for process in self.process:
            if process.status == Status.Ready:
                return False
        return True

    def run_process(self):
        for process_num in range(len(self.process)):
            if process_num == self.pointer:
                self.process[process_num].run()
            else:
                if self.process[process_num].status == Status.Ready:
                    self.process[process_num].wait()

    def start(self):
        while not self.check_all_end():
            if self.process[self.pointer].status == Status.Ready:
                self.run_process()
                self.pointer_add()
                self.show_all_process()
            else:
                self.pointer_add()


class Process:
    def __init__(self, demand_run_times):
        self.label = 0
        self.demand_run_times = demand_run_times
        self.status = Status.Ready
        self.already_run_times = 0
        self.effective_run_times = 0

    def run(self):
        if self.status == Status.End:
            return

        self.already_run_times += 1
        self.effective_run_times += 1
        if self.effective_run_times >= self.demand_run_times:
            self.status = Status.End
        return

    def wait(self):
        self.already_run_times += 1


class Status:
    Ready = 'Ready'
    End = 'End'


if __name__ == '__main__':
    processor = ProcessorDeque()
    processor.load_file('data.txt')
    processor.start()
