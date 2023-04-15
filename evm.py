class EVMState:
    def __init__(self, bytecode):
        self.code = bytecode
        self.stack = []
        self.memory = bytearray()
        self.storage = {}
        self.pc = 0

def metaopcode_math(state, op, size) -> EVMState:

    if size == 1:
        x = state.stack.pop()
        state.stack = state.stack + op(x)
    elif size == 2:
        x = state.stack.pop()
        y = state.stack.pop()
        state.stack = state.stack + op(x, y)
    elif size == 3:
        x = state.stack.pop()
        y = state.stack.pop()
        z = state.stack.pop()
        state.stack = state.stack + op(x, y, z)

    return state