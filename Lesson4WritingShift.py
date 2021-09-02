# Writing Shift

# We are currently looking at chart[i] and we see x => ab . cd from j. The input is tokens.

# Your procedure, shift, should either return None, at which point there is
# nothing to do or will return a single new parsing state that presumably
# involved shifting over the c if c matches the ith token.

def shift(tokens, i, x, ab, cd, j):
    if len(cd) != 0:
        next = cd[0]
        if tokens[i] == next:
            return (x, ab + [next], cd[1:], j)
    return None



print shift(["exp", "+", "exp"], 2, "exp", ["exp", "+"], ["exp"], 0) == ('exp', ['exp', '+', 'exp'], [], 0)
print shift(["exp", "+", "exp"], 0, "exp", [], ["exp", "+", "exp"], 0) == ('exp', ['exp'], ['+', 'exp'], 0)
print shift(["exp", "+", "exp"], 3, "exp", ["exp", "+", "exp"], [], 0) == None
print shift(["exp", "+", "ANDY LOVES COOKIES"], 2, "exp", ["exp", "+"], ["exp"], 0) == None
