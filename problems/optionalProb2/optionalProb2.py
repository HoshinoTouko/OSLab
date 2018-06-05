

class Resource:
    def __init__(self, resource_number):
        self.resource_number = resource_number
        self.activated_process = []
        self.waiting_process = []

    def P(self, process):
        if process in self.activated_process or process in self.waiting_process:
            return False

        self.resource_number -= 1
        if self.resource_number < 0:
            self.waiting_process.append(process)
            return ProcessStatus.waited
        self.activated_process.append(process)
        return ProcessStatus.activated

    def V(self, process):
        if process not in self.activated_process:
            return False

        self.resource_number += 1
        if self.resource_number < 0 and len(self.waiting_process) > 0:
            next_process = self.waiting_process.pop(0)


class ProcessStatus:
    waited = -1
    activated = 1
