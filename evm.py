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

def opcode_add(state) -> EVMState:
    def add(x, y) -> list:
        return [(x + y) % 2**256]
    return metaopcode_math(state, add, 2)

def opcode_mul(state) -> EVMState:
    def mul(x, y) -> list:
        return (x * y) % 2**256
    return metaopcode_math(state, mul, 2)

def opcode_sub(state) -> EVMState:
    def sub(x, y) -> list:
        return [(x - y) % 2**256]
    return metaopcode_math(state, sub, 2)

def opcode_div(state) -> EVMState:
    def div(x, y) -> list:
        return [x // y]
    return metaopcode_math(state, div, 2)

def opcode_sdiv(state) -> EVMState:
    def sdiv(x, y) -> list:
        return [x // y]
    return metaopcode_math(state, sdiv, 2)

def opcode_mod(state) -> EVMState:
    def mod(x, y) -> list:
        return [x % y]
    return metaopcode_math(state, mod, 2)

def opcode_smod(state) -> EVMState:
    def smod(x, y) -> list:
        return [x % y]
    return metaopcode_math(state, smod, 2)

def opcode_addmod(state) -> EVMState:
    def addmod(x, y, z) -> list:
        return [(x + y) % z]
    return metaopcode_math(state, addmod, 3)

def opcode_mulmod(state) -> EVMState:
    def mulmod(x, y, z) -> list:
        return [(x * y) % z]
    return metaopcode_math(state, mulmod, 3)

def opcode_exp(state) -> EVMState:
    def exp(x, y) -> list:
        return [x ** y % 2**256]
    return metaopcode_math(state, exp, 2)

def opcode_signextend(state) -> EVMState:
    # mb this is wrong
    def signextend(x, y) -> list:
        sign_bit = 1 << (y * 8 - 1)
        mask = (1 << (y * 8)) - 1
        if x & sign_bit:
            return [(x & mask) - sign_bit]
        else:
            return [x & mask]
    return metaopcode_math(state, signextend, 2)

def opcode_lt(state) -> EVMState:
    def lt(x, y) -> list:
        if x < y:
            return [1]
        else:
            return [0]
    return metaopcode_math(state, lt, 2)

def opcode_gt(state) -> EVMState:
    def gt(x, y) -> list:
        if x > y:
            return [1]
        else:
            return [0]
    return metaopcode_math(state, gt, 2)

def opcode_slt(state) -> EVMState:
    def slt(x, y) -> list:
        if x < y:
            return [1]
        else:
            return [0]
    return metaopcode_math(state, slt, 2)

def opcode_sgt(state) -> EVMState:
    def sgt(x, y) -> list:
        if x > y:
            return [1]
        else:
            return [0]
    return metaopcode_math(state, sgt, 2)

def opcode_eq(state) -> EVMState:
    def eq(x, y) -> list:
        if x == y:
            return [1]
        else:
            return [0]
    return metaopcode_math(state, eq, 2)

def opcode_iszero(state) -> EVMState:
    def iszero(x) -> list:
        if x == 0:
            return [1]
        else:
            return [0]
    return metaopcode_math(state, iszero, 1)

def opcode_and(state) -> EVMState:
    def land(x, y) -> list:
        return [x & y]
    return metaopcode_math(state, land, 2)

def opcode_or(state) -> EVMState:
    def lor(x, y) -> list:
        return [x | y]
    return metaopcode_math(state, lor, 2)

def opcode_xor(state) -> EVMState:
    def lxor(x, y) -> list:
        return [x ^ y]
    return metaopcode_math(state, lxor, 2)

def opcode_not(state) -> EVMState:
    def lnot(x) -> list:
        return [~x]
    return metaopcode_math(state, lnot, 1)

def opcode_byte(state) -> EVMState:
    def byte(x, y) -> list:
        return [(y >> (x * 8)) & 0xff]
    return metaopcode_math(state, byte, 2)

def opcode_shl(state) -> EVMState:
    def shl(x, y) -> list:
        return [y << x]
    return metaopcode_math(state, shl, 2)

def opcode_shr(state) -> EVMState:
    def shr(x, y) -> list:
        return [y >> x]
    return metaopcode_math(state, shr, 2)

def opcode_sar(state) -> EVMState:
    # mb this is wrong
    def sar(x, y) -> list:
        return [y >> x]
    return metaopcode_math(state, sar, 2)