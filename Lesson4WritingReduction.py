# Writing Reductions

# We are looking at chart[i] and we see x => ab . cd from j.

# Hint: Reductions are tricky, so as a hint, remember that you only want to do
# reductions if cd == []

# Hint: You'll have to look back previously in the chart.

def reductions(chart, i, x, ab, cd, j):
    if len(cd) == 0:
        candidates = [item for item in chart[j] if len(item[2]) != 0 and item[2][0] == x]
        moveds = []
        for item in candidates:
            moveds.append((item[0], item[1] + [x], item[2][1:], item[3]))
        return moveds

    return []

chart = {
    0: [
        ('exp', ['exp'], ['+', 'exp'], 0),
        ('exp', [], ['num'], 0), 
        ('exp', [], ['(', 'exp', ')'], 0),
        ('exp', [], ['exp', '-', 'exp'], 0),
        ('exp', [], ['exp', '+', 'exp'], 0)], 
    1: [('exp', ['exp', '+'], ['exp'], 0)],
    2: [('exp', ['exp', '+', 'exp'], [], 0)]
}

print reductions(chart, 2, 'exp', ['exp', '+', 'exp'], [], 0) == [('exp', ['exp'], ['-', 'exp'], 0), ('exp', ['exp'], ['+', 'exp'], 0)]
