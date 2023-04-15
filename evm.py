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

def opcode_address(state) -> EVMState:
    # TODO: implement
    return

def opcode_balance(state) -> EVMState:
    # TODO: implement
    return

def opcode_origin(state) -> EVMState:
    # TODO: implement
    return

def opcode_caller(state) -> EVMState:
    # TODO: implement
    return

# TODO: implement much more opcodes

def metaopcode_push(state, size) -> EVMState:
    elements = state.code[state.pc:state.pc+size]
    stack_element = sum([elements[i] * (256 ** i) for i in range(size)])
    state.stack = state.stack + [stack_element]
    state.pc += size
    return state

def opcode_push1(state) -> EVMState:
    return metaopcode_push(state, 1)

def opcode_push2(state) -> EVMState:
    return metaopcode_push(state, 2)

def opcode_push3(state) -> EVMState:
    return metaopcode_push(state, 3)

def opcode_push4(state) -> EVMState:
    return metaopcode_push(state, 4)

def opcode_push5(state) -> EVMState:
    return metaopcode_push(state, 5)

def opcode_push6(state) -> EVMState:
    return metaopcode_push(state, 6)

def opcode_push7(state) -> EVMState:
    return metaopcode_push(state, 7)

def opcode_push8(state) -> EVMState:
    return metaopcode_push(state, 8)

def opcode_push9(state) -> EVMState:
    return metaopcode_push(state, 9)

def opcode_push10(state) -> EVMState:
    return metaopcode_push(state, 10)

def opcode_push11(state) -> EVMState:
    return metaopcode_push(state, 11)

def opcode_push12(state) -> EVMState:
    return metaopcode_push(state, 12)

def opcode_push13(state) -> EVMState:
    return metaopcode_push(state, 13)

def opcode_push14(state) -> EVMState:
    return metaopcode_push(state, 14)

def opcode_push15(state) -> EVMState:
    return metaopcode_push(state, 15)

def opcode_push16(state) -> EVMState:
    return metaopcode_push(state, 16)

def opcode_push17(state) -> EVMState:
    return metaopcode_push(state, 17)

def opcode_push18(state) -> EVMState:
    return metaopcode_push(state, 18)

def opcode_push19(state) -> EVMState:
    return metaopcode_push(state, 19)

def opcode_push20(state) -> EVMState:
    return metaopcode_push(state, 20)

def opcode_push21(state) -> EVMState:
    return metaopcode_push(state, 21)

def opcode_push22(state) -> EVMState:
    return metaopcode_push(state, 22)

def opcode_push23(state) -> EVMState:
    return metaopcode_push(state, 23)

def opcode_push24(state) -> EVMState:
    return metaopcode_push(state, 24)

def opcode_push25(state) -> EVMState:
    return metaopcode_push(state, 25)

def opcode_push26(state) -> EVMState:
    return metaopcode_push(state, 26)

def opcode_push27(state) -> EVMState:
    return metaopcode_push(state, 27)

def opcode_push28(state) -> EVMState:
    return metaopcode_push(state, 28)

def opcode_push29(state) -> EVMState:
    return metaopcode_push(state, 29)

def opcode_push30(state) -> EVMState:
    return metaopcode_push(state, 30)

def opcode_push31(state) -> EVMState:
    return metaopcode_push(state, 31)

def opcode_push32(state) -> EVMState:
    return metaopcode_push(state, 32)

def metaopcode_dup(state, index) -> EVMState:
    state.stack = state.stack + [state.stack[-index]]
    return state

def opcode_dup1(state) -> EVMState:
    return metaopcode_dup(state, 1)

def opcode_dup2(state) -> EVMState:
    return metaopcode_dup(state, 2)

def opcode_dup3(state) -> EVMState:
    return metaopcode_dup(state, 3)

def opcode_dup4(state) -> EVMState:
    return metaopcode_dup(state, 4)

def opcode_dup5(state) -> EVMState:
    return metaopcode_dup(state, 5)

def opcode_dup6(state) -> EVMState:
    return metaopcode_dup(state, 6)

def opcode_dup7(state) -> EVMState:
    return metaopcode_dup(state, 7)

def opcode_dup8(state) -> EVMState:
    return metaopcode_dup(state, 8)

def opcode_dup9(state) -> EVMState:
    return metaopcode_dup(state, 9)

def opcode_dup10(state) -> EVMState:
    return metaopcode_dup(state, 10)

def opcode_dup11(state) -> EVMState:
    return metaopcode_dup(state, 11)

def opcode_dup12(state) -> EVMState:
    return metaopcode_dup(state, 12)

def opcode_dup13(state) -> EVMState:
    return metaopcode_dup(state, 13)

def opcode_dup14(state) -> EVMState:
    return metaopcode_dup(state, 14)

def opcode_dup15(state) -> EVMState:
    return metaopcode_dup(state, 15)

def opcode_dup16(state) -> EVMState:
    return metaopcode_dup(state, 16)

def metaopcode_swap(state, index) -> EVMState:
    state.stack = state.stack[:-index] + [state.stack[-1]] + state.stack[-index:-1]
    return state