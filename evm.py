class EVMState:
    def __init__(self, bytecode):
        self.code = bytecode
        self.stack = []
        self.memory = bytearray()
        self.storage = {}
        self.pc = 0