# Implementing RE
# Challenge Problem 
#
# Focus: All Units
#
#
# In this problem you will write a lexer, parser and interpreter for
# strings representing regular expressions. Your program will output 
# a non-deterministic finite state machine that accepts the same language
# as that regular expression. 
#
# For example, on input 
#
# ab*c
#
# Your program might output
# 
# edges = { (1,'a')  : [ 2 ] ,
#           (2,None) : [ 3 ] ,    # epsilon transition
#           (2,'b')  : [ 2 ] ,
#           (3,'c')  : [ 4 ] } 
# accepting = [4]
# start = 1
#
# We will consider the following regular expressions:
#
#       single characters       #       a       
#       regexp1 regexp2         #       ab
#       regexp *                #       a*
#       regexp1 | regexp2       #       a|b
#       ( regexp )              #       (a|b)* -- same as (?:a|b) 
#
# That's it. We won't consider [a-c] because it's just a|b|c, and we won't
# consider a+ because it's just aa*. We will not worry about escape
# sequences. Single character can be a-z, A-Z or 0-9 -- that's it. No need
# to worry about strange character encodings. We'll use ( ) for regular
# expression grouping instead of (?: ) just to make the problem simpler.
#
# Don't worry about precedence or associativity. We'll fully parenthesize
# all regular expressions before giving them to you. 
#
# You will write a procedure re_to_nfsm(re_string). It takes as input a
# single argument -- a string representing a regular expression. It returns
# a tuple (edges,accepting,start) corresponding to an NSFM that accepts the
# same language as that regular expression.
#
# Hint: Make a lexer and a paser and an interpreter. Your interpreter may
# find it handy to know the current state and the goal state. Make up as
# many new states as you need. 
# 
import ply.lex as lex
import ply.yacc as yacc

# Fill in your code here. 
tokens = ('SINGLE_CHAR', 'STAR', 'OR', 'LPAREN', 
          'RPAREN')
def t_single_char(token):
    r'[^\*\|\(\)]'
    token.type = 'SINGLE_CHAR'
    return token

def t_star(token):
    r'\*'
    token.type = 'STAR'
    return token

def t_or(token):
    r'\|'
    token.type = 'OR'
    return token

def t_left_paren(token):
    r'\('
    token.type = 'LPAREN'
    return token

def t_right_paren(token):
    r'\)'
    token.type = 'RPAREN'
    return token

def t_error(token):
    print("Illegal character '%s'" % token.value[0])
    token.lexer.skip(1)

start = 'exp'

def p_single_char_exp(p):
    'exp : SINGLE_CHAR'
    p[0] = p[1]

def p_compose(p):
    'exp : exp exp'
    p[0] = ['compose', p[1], p[2]]

def p_zero_more(p):
    'exp : exp STAR'
    p[0] = ['zero_more', p[1]]

def p_or(p):
    'exp : exp OR exp'
    p[0] = ['or', p[1], p[3]]

def p_pack(p):
    'exp : LPAREN exp RPAREN'
    p[0] = p[2]

def p_error(p):
        raise SyntaxError

lexer = lex.lex() 
parser = yacc.yacc() 

def interpret(tree):
    start = 0
    edges = {}
    accepting = []
    currentState = start

    def addToEdges(path, dest):
        if path in edges:
            edges[path].append(dest)
        else:
            edges[path] = [dest]

    def consSingleCharFrom(state, subTree):
        char = subTree
        next = state + 1
        addToEdges((state, char), next)
        return next
    def consComposeFrom(state, subTree):
        exp1 = subTree[1]
        exp2 = subTree[2]
        newState = consFrom(state, exp1)
        return consFrom(newState, exp2)
    def consOrFrom(state, subTree):
        exp1 = subTree[1]
        exp2 = subTree[2]
        start1 = state + 1

        addToEdges((state, None), start1)
        end1 = consFrom(start1, exp1)
        start2 = end1 + 1
        addToEdges((state, None), start2)
        end2 = consFrom(start2, exp2)
        end = end2 + 1
        addToEdges((end1, None), end)
        addToEdges((end2, None), end)
        return end
    def consZeroMoreFrom(state, subTree):
        exp = subTree[1]
        newState = consFrom(state, exp)
        addToEdges((state, None), newState)
        addToEdges((newState, None), state)
        return newState

    def consFrom(state, subTree):
        type = subTree[0]
        if type == 'compose':
            return consComposeFrom(state, subTree)
        elif type == 'or':
            return consOrFrom(state, subTree)
        elif type == 'zero_more':
            return consZeroMoreFrom(state, subTree)
        else:
            return consSingleCharFrom(state, subTree)
    
    accepting = [consFrom(currentState, tree)]
    return (edges, accepting, start)

def re_to_nfsm(re_string): 
        # Feel free to overwrite this with your own code. 
        lexer.input(re_string)
        parse_tree = parser.parse(re_string, lexer=lexer) 
        return interpret(parse_tree) 

# We have included some testing code ... but you really owe it to yourself
# to do some more testing here.

def nfsmaccepts(edges, accepting, current, string, visited): 
        # If we have visited this state before, return false. 
        if (current, string) in visited:
                return False
        visited.append((current, string))       

        # Check all outgoing epsilon transitions (letter == None) from this
        # state. 
        if (current, None) in edges:
                for dest in edges[(current, None)]:
                        if nfsmaccepts(edges, accepting, dest, string, visited):
                                return True

        # If we are out of input characters, check if this is an
        # accepting state. 
        if string == "":
                return current in accepting

        # If we are not out of input characters, try all possible
        # outgoing transitions labeled with the next character. 
        letter = string[0]
        rest = string[1:]
        if (current, letter) in edges:
                for dest in edges[(current, letter)]:
                        if nfsmaccepts(edges, accepting, dest, rest, visited):
                                return True
        return False

def test(re_string, e, ac_s, st_s, strings):
  my_e, my_ac_s, my_st_s = re_to_nfsm(re_string) 
  print my_e
  for string in strings:
      print nfsmaccepts(e,ac_s,st_s,string,[]) == \
            nfsmaccepts(my_e,my_ac_s,my_st_s,string,[]) 

edges = { (1,'a')  : [ 2 ] ,
          (2,None) : [ 3 ] ,    # epsilon transition
          (2,'b')  : [ 2 ] ,
          (3,'c')  : [ 4 ] } 
accepting_state = [4]
start_state = 1

test("a(b*)c", edges, accepting_state, start_state, 
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 

edges = { (1,'a')  : [ 2 ] ,
          (2,'b') :  [ 1 ] ,    
          (1,'c')  : [ 3 ] ,
          (3,'d')  : [ 1 ] } 
accepting_state = [1]
start_state = 1

test("((ab)|(cd))*", edges, accepting_state, start_state, 
  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 
