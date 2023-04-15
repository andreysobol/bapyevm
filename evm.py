class EVMState:
    def __init__(self, bytecode, address, origin):
        self.code = bytecode
        self.stack = []
        self.memory = []
        self.storage = {}
        self.logs = []
        self.pc = 0

        # eth values
        self.address = address
        self.origin = origin

        # block values
        self.blockhashes = {}
        self.blocknumber = 0
        self.coinbase = 0
        self.timestamp = 0
        self.prevrandao = 0
        self.number = 0
        self.gaslimit = 0
        self.chainid = 0
        self.basefee = 0

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

def opcode_sha3(state) -> EVMState:

    ofset = state.pop()
    size = state.pop()

    if ofset + 32 > len(state.memory):
        state.memory += [0] * (ofset + 32 - len(state.memory))

    values = state.memory[ofset:ofset + 32]

    # TODO: implement real keccak256
    result = 0x29045A592007D0C246EF02C2223570DA9522D0CF0F73282C79A1BC8F0BB2C238

    state.stack = state.stack + [result]
    
    return state

def opcode_address(state) -> EVMState:
    address = state.address
    state.stack = state.stack + [address]
    return state

def opcode_balance(state) -> EVMState:
    # TODO: implement
    return state

def opcode_origin(state) -> EVMState:
    origin = state.origin
    state.stack = state.stack + [origin]
    return state

def opcode_caller(state) -> EVMState:
    # TODO: implement
    # To implement this we need to implement DELEGATECALL and CALL
    return state

def opcode_callvalue(state) -> EVMState:
    # TODO: implement
    return state

def opcode_calldataload(state) -> EVMState:
    # TODO: implement
    return state

def opcode_calldatasize(state) -> EVMState:
    # TODO: implement
    return state

def opcode_calldatacopy(state) -> EVMState:
    # TODO: implement
    return state

def opcode_codesize(state) -> EVMState:
    # TODO: implement
    return state

def opcode_codecopy(state) -> EVMState:
    # TODO: implement
    return state

def opcode_gasprice(state) -> EVMState:
    # TODO: implement
    return state

def opcode_extcodesize(state) -> EVMState:
    # TODO: implement
    return state

def opcode_extcodecopy(state) -> EVMState:
    # TODO: implement
    return state

def opcode_returndatasize(state) -> EVMState:
    # TODO: implement
    return state

def opcode_returndatacopy(state) -> EVMState:
    # TODO: implement
    return state

def opcode_blockhash(state) -> EVMState:
    block_number = state.pop()
    if block_number < state.blocknumber:
        state.stack = state.stack + state.blockhashes[block_number]
    else:
        state.stack = state.stack + [0]
    return state

def opcode_coinbase(state) -> EVMState:
    coinbase = state.coinbase
    state.stack = state.stack + [coinbase]
    return state

def opcode_timestamp(state) -> EVMState:
    timestatmp = state.timestamp
    state.stack = state.stack + [timestatmp]
    return state

def opcode_number(state) -> EVMState:
    number = state.number
    state.stack = state.stack + [number]
    return state

def opcode_prevrandao(state) -> EVMState:
    prevrandao = state.prevrandao
    state.stack = state.stack + [prevrandao]
    return state

def opcode_gaslimit(state) -> EVMState:
    gas_limit = state.gas_limit
    state.stack = state.stack + [gas_limit]
    return state

def opcode_chainid(state) -> EVMState:
    chain_id = state.chain_id
    state.stack = state.stack + [chain_id]
    return state

def opcode_selfbalance(state) -> EVMState:
    # TODO: implement
    return state

def opcode_basefee(state) -> EVMState:
    basefee = state.basefee
    state.stack = state.stack + [basefee]
    return state

def opcode_pop(state) -> EVMState:
    state.stack = state.stack[:-1]
    return state

def opcode_mload(state) -> EVMState:
    ofset = state.pop()

    if ofset + 32 > len(state.memory):
        state.memory += [0] * (ofset + 32 - len(state.memory))

    values = state.memory[ofset:ofset + 32]

    value = sum([values[i] * (256 ** i) for i in range(32)])

    state.stack = state.stack + [value]

    return state

def opcode_mstore(state) -> EVMState:
    ofset = state.pop()
    value = state.pop()
    mask = lambda value, i: value >> (i * 8) & 0xff
    values = [mask(value, i) for i in range(32)]
    if ofset + 32 > len(state.memory):
        state.memory += [0] * (ofset + 32 - len(state.memory))

    state.memory = state.memory[:ofset] + values + state.memory[ofset + 32:]

    return state

def opcode_mstore8(state) -> EVMState:
    
    ofset = state.pop()
    value = state.pop()
    if ofset + 1 > len(state.memory):
        state.memory += [0] * (ofset + 1 - len(state.memory))
    
    state.memory[ofset] = value & 0xff

    return state

def opcode_sload(state) -> EVMState:
    key = state.pop()
    if key not in state.storage:
        value = 0
    else:
        value = state.storage[key]
    state.stack = state.stack + [value]
    return state

def opcode_sstore(state) -> EVMState:
    key = state.pop()
    value = state.pop()
    state.storage[key] = value
    return state

def opcode_jump(state) -> EVMState:
    # TODO: implement
    return state

def opcode_jumpi(state) -> EVMState:
    # TODO: implement
    return state

def opcode_pc(state) -> EVMState:
    pc = state.pc
    state.stack = state.stack + [pc]
    return state

def opcode_msize(state) -> EVMState:
    # TODO: implement
    return state

def opcode_gas(state) -> EVMState:
    # TODO: implement
    return state

def opcode_jumpdest(state) -> EVMState:
    # TODO: implement
    return state

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

def opcode_swap1(state) -> EVMState:
    return metaopcode_swap(state, 1)

def opcode_swap2(state) -> EVMState:
    return metaopcode_swap(state, 2)

def opcode_swap3(state) -> EVMState:
    return metaopcode_swap(state, 3)

def opcode_swap4(state) -> EVMState:
    return metaopcode_swap(state, 4)

def opcode_swap5(state) -> EVMState:
    return metaopcode_swap(state, 5)

def opcode_swap6(state) -> EVMState:
    return metaopcode_swap(state, 6)

def opcode_swap7(state) -> EVMState:
    return metaopcode_swap(state, 7)

def opcode_swap8(state) -> EVMState:
    return metaopcode_swap(state, 8)

def opcode_swap9(state) -> EVMState:
    return metaopcode_swap(state, 9)

def opcode_swap10(state) -> EVMState:
    return metaopcode_swap(state, 10)

def opcode_swap11(state) -> EVMState:
    return metaopcode_swap(state, 11)

def opcode_swap12(state) -> EVMState:
    return metaopcode_swap(state, 12)

def opcode_swap13(state) -> EVMState:
    return metaopcode_swap(state, 13)

def opcode_swap14(state) -> EVMState:
    return metaopcode_swap(state, 14)

def opcode_swap15(state) -> EVMState:
    return metaopcode_swap(state, 15)

def opcode_swap16(state) -> EVMState:
    return metaopcode_swap(state, 16)

def metaopcode_log(state, topic_size) -> EVMState:
    offset = state.stack.pop()
    size = state.stack.pop()
    if topic_size > 0:
        topics = [state.stack.pop() for _ in range(topic_size)]
    else:
        topics = []

    state.logs.append((offset, size, topics))
    return state

def opcode_log0(state) -> EVMState:
    state = metaopcode_log(state, 0)
    return state

def opcode_log1(state) -> EVMState:
    state = metaopcode_log(state, 1)
    return state

def opcode_log2(state) -> EVMState:
    state = metaopcode_log(state, 2)
    return state

def opcode_log3(state) -> EVMState:
    state = metaopcode_log(state, 3)
    return state

def opcode_log4(state) -> EVMState:
    state = metaopcode_log(state, 4)
    return state

def opcode_create(state) -> EVMState:
    # TODO: implement CREATE
    return state

def opcode_call(state) -> EVMState:
    # TODO: implement CALL
    return state

def opcode_callcode(state) -> EVMState:
    # TODO: implement CALLCODE
    return state

def opcode_return(state) -> EVMState:
    # TODO: implement RETURN
    return state

def opcode_delegatecall(state) -> EVMState:
    # TODO: implement DELEGATECALL
    return state

def opcode_create2(state) -> EVMState:
    # TODO: implement CREATE2
    return state

def opcode_staticcall(state) -> EVMState:
    # TODO: implement STATICCALL
    return state

def opcode_revert(state) -> EVMState:
    # TODO: implement REVERT
    return state

def opcode_invalid(state) -> EVMState:
    # TODO: implement INVALID
    return state

def opcode_selfdestruct(state) -> EVMState:
    # TODO: implement SELFDESTRUCT
    return state