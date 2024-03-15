# Data should be in following format:
# 1. row - min for minimize, max for maximize
# then coefficients in objective function
# n. row - coefficients in constraint equations, </>, constant

import sys
import math 

# Math

class number:
    s: bool
    n: int
    d: int
    def __init__(self, sign, numerator, denominator):
        self.s = sign
        self.n = numerator
        self.d = denominator

def update_fraction(number):
    if number.n == 0:
        number.d = 1
        number.s = False
        return number
    if number.d == 0:
        number.n == 1
        return number
    div = math.gcd(number.n, number.d)
    number.n //= div
    number.d //= div
    return number

def mul(number_1, number_2):
    new_s = (number_1.s != number_2.s)
    new_n = number_1.n * number_2.n
    new_d = number_1.d * number_2.d
    return update_fraction(number(new_s, new_n, new_d))

def add(number_1, number_2):
    new_d = math.lcm(number_1.d, number_2.d)
    new_n = number_1.n * (new_d // number_1.d)
    if number_1.s:
        new_n *= -1
    if number_2.s:
        new_n -= number_2.n * (new_d // number_2.d)
    else:
        new_n += number_2.n * (new_d // number_2.d)
    new_s = (True if new_n < 0 else False)
    new_n = abs(new_n)
    return update_fraction(number(new_s, new_n, new_d))

def inv(number_0):
    return number(number_0.s, number_0.d, number_0.n)

def neg(number_0):
    return number(not number_0.s, number_0.n, number_0.d)

def parse_num(item, neg_flag):
    sign_flag = False
    num, den = 0, 1
    if item[0] == "-":
        sign_flag = True
        item = item[1:]
    if "/" in item:
        num, den = [int(x) for x in item.split("/")]
    else:
        num = int(item)
        den = 1
    return number((sign_flag != neg_flag), num, den)

def greater(number_1, number_2):
    if number_1.s and not number_2.s:
        return False
    if number_2.s and not number_1.s:
        return True
    if number_1.n == 0 and number_2.n == 0:
        return False
    if number_1.s:
        number_1, number_2 = number_2, number_1
    left = number_1.n * number_2.d
    right = number_2.n * number_1.d
    return left > right

def write_num(number_0):
    result = ""
    if number_0.s:
        result += "-"
    if number_0.d == 1:
        result += str(number_0.n)
        return result
    elif number_0.d == 0:
        result += "\infty"
        return result
    else:
        result += "\\frac{"
        result += str(number_0.n)
        result += "}{"
        result += str(number_0.d)
        result += "}"
        return result

ZERO = number(False, 0, 1)

# Printer

def M_printer(print_val, print_val_M):
    to_print = ""
    M_part = False
    if greater(print_val_M,ZERO) or greater(ZERO,print_val_M):
        to_print += write_num(print_val_M)
        to_print += "M"
        M_part = True
    if greater(print_val,ZERO) or greater(ZERO,print_val):
        if M_part and greater(print_val,ZERO):
            to_print += "+"
        to_print += write_num(print_val)
    if to_print == "":
        to_print = "0"
    print(f" & {to_print}",end="")

# Get variables

file_name = sys.argv[1]
# file_name = input()
# file_name = "in.txt"
lines = open(file_name).readlines()
x_num = len(lines[0].strip().split(" ")) - 1
rows = len(lines) - 1

# Start LaTeX

print("""\\documentclass[12p]{article}
\\usepackage{amsmath}
\\usepackage{geometry}
\\geometry{legalpaper, landscape, margin=1in}
\\begin{document}""")

# Add find greater rows

equations_list = [line.strip().split(" ") for line in lines[1:]]
greater_rows = [False for _ in range(rows)]
greater_rows_num = 0
for i, eq in enumerate(equations_list):
    if eq[-2] == ">":
        greater_rows[i] = True
        greater_rows_num += 1
    equations_list[i] = eq[:-2] + [eq[-1]]

cols = x_num + rows + greater_rows_num + 1

# Make objective function

objective_list = lines[0].split(" ")
min_flag = False
if objective_list[0] == "min":
    min_flag = True
objective_list = objective_list[1:]

objective = [number(False, 0, 1) for _ in range(cols)]
objective_M = [number(False, 0, 1) for _ in range(cols)]

for i, item in enumerate(objective_list):
    objective[i] = parse_num(item, min_flag)

for i in range(cols-greater_rows_num-1,cols-1):
    objective_M[i] = number(True, 1, 1)

# Make equations
equations = [[number(False, 0, 1) for _ in range(cols)] for _ in range(rows)]
neg_flag = False
neg_counter = 0
for i, eq in enumerate(equations_list):
    if greater_rows[i]:
        neg_flag = True
        equations[i][x_num+rows+neg_counter] = number(False, 1, 1)
        neg_counter += 1
    for j, item in enumerate(eq[:-1]):
        equations[i][j] = parse_num(item, False)
    equations[i][x_num+i] = number(neg_flag,1,1)
    equations[i][-1] = parse_num(eq[-1], False)

# generate variables

variables = [f"x_{{{x+1}}}" for x in range(x_num)] + [f"s_{{{x+1}}}" for x in range(rows)] + [f"a_{{{x+1}}}" for x in range(neg_counter)]

# find base

base = []
j = 0
for i, x in enumerate(greater_rows):
    if x:
        j+=1
        base.append(f"a_{{{j}}}")
    else:
        base.append(f"s_{{{i+1}}}")
cb = [number(False, 0, 1) for _ in range(rows)]
cb_M = [number(True if x else False, int(x), 1) for x in greater_rows]

# anti-loop
tried_bases = []

# THE MAIN LOOP:

con = True
itr = 0
while con:
    itr += 1
    # Calculating pointer row
    pointer_row = [number(False,0,1) for _ in range(cols)]
    pointer_row_M = [number(False,0,1) for _ in range(cols)]
    con = False
    minp = number(False, 0, 1)
    minp_M = number(False, 0, 1)
    coln = 0
    for i in range(cols):
        pointer = number(False, 0, 1)
        pointer_M = number(False, 0, 1)
        for j in range(rows):
            pointer = add(pointer, mul(cb[j], equations[j][i]))
            pointer_M = add(pointer_M, mul(cb_M[j], equations[j][i]))
        pointer = add(pointer, neg(objective[i]))
        pointer_M = add(pointer_M, neg(objective_M[i]))
        pointer_row[i] = pointer
        pointer_row_M[i] = pointer_M
        if i < cols - 1 and not (base + [variables[i]]) in tried_bases:
            if greater(ZERO, pointer_M):
                con = True
            elif not greater(pointer_M, ZERO) and greater(ZERO, pointer):
                con = True
            if greater(minp_M, pointer_M):
                    coln = i
                    minp_M = pointer_M
                    minp = pointer
            elif not greater(pointer_M, minp_M) and greater(minp, pointer):
                coln = i
                minp = pointer
    tried_bases.append(base + [variables[coln]])
    if con:
        ratio_col = [mul(equations[x][-1], inv(equations[x][coln])) for x in range(rows)]
    # begin print
    print(f"\\[\n\\begin{{array}}{{|{'c|'*(cols+2+int(con))}}}")
    print("\\hline\n &",end="")
    for col in range(cols-1):
        to_write = ""
        if greater(objective_M[col],ZERO) or greater(ZERO,objective_M[col]):
            to_write += write_num(objective_M[col])
            to_write += "M"
        else:
            to_write += write_num(objective[col])
        print(f" & {to_write}",end="")
    print(f" &{' &' if con else ''} \\\\\n\\hline\nB & cb",end="")
    for var in variables:
        print(f" & {var}",end="")
    print(f" & RHS {' & ratio' if con else ''} \\\\\n\\hline\n",end="")
    for row in range(rows):
        print(f"{base[row]}",end="")
        M_printer(cb[row],cb_M[row])
        for col in range(cols):
            print(f" & {write_num(equations[row][col])}",end="")
        if con:
            print(f" & {write_num(ratio_col[row])}",end="")
        print(" \\\\\n\\hline\n",end="")
    print(f"&",end="")
    for col in range(cols):
        M_printer(pointer_row[col],pointer_row_M[col])
    print(f"{' &' if con else ''} \\\\\n\hline\n\\end{{array}}\n\\]\n")
    # end print
    if not con:
        break
    # Finding row for base change
    minval = number(False, 1, 0)
    rown = 0
    for i in range(rows):
        if greater(minval, ratio_col[i]) and greater(ratio_col[i], ZERO): # originally x>=0, now x>0
            rown = i
            minval = ratio_col[i]
    if minval == number(False, 1, 0):
        con = False
        break
    # Update the table
    leaving = base[rown]
    base[rown] = variables[coln]
    cb[rown] = objective[coln]
    cb_M[rown] = objective_M[coln]
    new_equations = [[number(False,0,1) for col in range(cols)] for row in range(rows)]
    for col in range(cols):
        new_equations[rown][col] = mul(equations[rown][col],inv(equations[rown][coln]))
    for row in range(rows):
        if row == rown:
            continue
        for col in range(cols):
            new_equations[row][col] = add(equations[row][col], neg(mul(mul(equations[rown][col], equations[row][coln]), inv(equations[rown][coln]))))
    if leaving[0] != 'a':
        equations = [[new_equations[row][col] for col in range(cols)] for row in range(rows)]
    else:
        leaving_column = variables.index(leaving)
        equations = [[(new_equations[row][col] if col < leaving_column else new_equations[row][col+1]) for col in range(cols-1)] for row in range(rows)]
        variables = variables[:leaving_column] + variables[(leaving_column+1):]
        objective = objective[:leaving_column] + objective[(leaving_column+1):]
        objective_M = objective_M[:leaving_column] + objective_M[(leaving_column+1):]
        cols -= 1
    if itr > 10:
        break

print("\\end{document}")