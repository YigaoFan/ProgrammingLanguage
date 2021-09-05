def addtochart(chart, index, state):
    if state in chart[index]:
        return False
    else:
        chart[index].append(state)
        return True

def closure(grammar, i, x, ab, cd):
    if len(cd) == 0:
        return []
    else:
        next = cd[0]
        states = []
        for rule in [x for x in grammar if x[0] == next]:
            states.append((next, [], rule[1], i))
        return states

def shift(tokens, i, x, ab, cd, j):
    if len(cd) != 0:
        next = cd[0]
        if tokens[i] == next:
            return (x, ab + [next], cd[1:], j)
    return None

def reductions(chart, i, x, ab, cd, j):
    if len(cd) == 0:
        candidates = [item for item in chart[j]
                      if len(item[2]) != 0 and item[2][0] == x]
        moveds = []
        for item in candidates:
            moveds.append((item[0], item[1] + [x], item[2][1:], item[3]))
        return moveds

    return []

def log(*messages, end='\n'):
    pass
    # print(*messages, end=end)

def parse(tokens, grammar):
    tokens = tokens + ['end_of_input_marker']
    chart = {}
    startRule = grammar[0]
    for i in range(len(tokens)+1):
        chart[i] = []
    startState = (startRule[0], [], startRule[1], 0)
    chart[0] = [startState]
    for i in range(len(tokens)):
        log('== chart', str(i))
        while True:
            changes = False
            for state in chart[i]: # python for 循环里尽管改变(addToChart)遍历容器不会出问题，但还是不太好
                x = state[0]
                ab = state[1]
                cd = state[2]
                j = state[3]

                # log begin
                log('    ', x, '->', end='')
                for sym in ab:
                   log(sym, end='')
                log('.', end='')
                for sym in cd:
                    log(' ' + sym, end='')
                log(' from', str(j))
                # log end
                nextStates = closure(grammar, i, x, ab, cd)
                for nextState in nextStates:
                    #actually here change the iterating container
                    changes = addtochart(chart, i, nextState) or changes
                
                nextState = shift(tokens, i, x, ab, cd, j)
                if nextState != None:
                    addtochart(chart, i+1, nextState)
                
                nextStates = reductions(chart, i, x, ab, cd, j)
                for nextState in nextStates:
                    changes = addtochart(chart, i, nextState) or changes

            if not changes:
                break
    acceptingState = (startRule[0], startRule[1], [], 0)
    return acceptingState in chart[len(tokens)-1]

tokens = ['(', '(', ')', ')']
grammar = [
    ('S', ['P']),
    ('P', ['(', 'P', ')']),
    ('P', []),
]
result = parse(tokens, grammar)
print(result)
