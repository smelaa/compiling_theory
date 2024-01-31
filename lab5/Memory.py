

class Memory:

    def __init__(self): # memory name
        # self.name = name
        self.values = dict()

    def has_key(self, name):  # variable name
        return name in self.values.keys()

    def get(self, name):         # gets from memory current value of variable <name>
        if self.has_key(name):
            return self.values.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.values.update({name : value})


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        mem = []
        if memory != None:
            mem.append(memory)
        else:
            mem.append(Memory())
        self.memory = mem

    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in self.memory:
            if memory.has_key(name):
                return memory.get(name)

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.memory[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for memory in self.memory:
            if memory.has_key(name):
                memory.put(name, value)
                break

    def push(self, memory): # pushes memory <memory> onto the stack
        self.memory.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.memory.pop()

    def contains(self, name):
        for memory in self.memory:
            if memory.has_key(name):
                return True
        return False


