# 300 lines of straight waffle
# if you find a bug, issue an issue
# if you can make a bug fix or improve performance / readability, pull a pull request


# libraries
import re
from decimal import Decimal
import numpy as np


# configs

LENGTH_ERROR = "This row is too short / too long, please try again."
FORMAT_ERROR = "Incorrectly formatted, please try again."
EXPRESSION_FORMAT_ERROR = "Expression formatted incorrectly, please try again."
EXPRESSION_DEFICIENCY_ERROR = "Expression must contain at least two terms with uncertainties, please try again."
UNCERTAINTY_FORMAT_ERROR = "Your uncertainties were not formatted properly, please try again."
INVALID_NUMBER_ERROR = "Your number was not formatted properly, please try again."


# utility functions

# these next two functions are ripped straight off from stack overflow and editted

def round_to_sig_figs(num: float, num_of_sf : int):
    if abs(num) < 999 and abs(num) > 0.001: 
        txt = np.format_float_positional(num, precision=num_of_sf, unique=False, fractional=False, trim='k')
        if txt[-1] == ".": txt = txt[:-1] # sometimes ends in . for no
        return txt
    else:
        # huh? these two ifs resolve to the same thing but without it, it doesn't work for negatives?
        # probably some branch prediction nonsense
        # im not gonna question it: if it ain't broke, don't fix it.
        if num >= 0: return f"{Decimal(num):.{max(0, num_of_sf-1)}E}".replace("E", "e").replace("+", "")
        if num < 0: return f"{Decimal(num):.{max(0, num_of_sf-1)}E}".replace("E", "e").replace("+", "")

def count_sigfigs(numstr) -> int:
    return len(Decimal(numstr).normalize().as_tuple().digits)


def expand_single_sci_notation(xpr):
    e_index = xpr.find("e")
    pre = xpr[:e_index]
    post = int(xpr[e_index+1:])
    if post < 0: return f"0.{'0' * (-post - 1)}{pre}"
    if post == 0: return pre
    if post > 0: return f"{pre}{'0' * post}"

def expand_scientific_notation(xpr):
    while "e" in xpr:
        e_index = xpr.find("e")
        left_index = e_index - 1
        right_index = e_index + 1
        while left_index > 0 and xpr[left_index].isdigit():
            left_index -= 1
        if left_index != 0: left_index += 1
        while right_index < len(xpr) and (xpr[right_index].isdigit() or xpr[right_index] == "-"):
            right_index += 1

        region = xpr[left_index:right_index]
        xpr = xpr.replace(region, expand_single_sci_notation(region))
    return xpr


def is_valid_number(s: str) -> float | bool:
    try:
        x: float = float(s)
        return x
    except ValueError:
        return False


def addition(a: str, b: str) -> str:
    a_value, a_uncertainty = parse_value_and_uncertainty(a)
    b_value, b_uncertainty = parse_value_and_uncertainty(b)
    return f"{a_value + b_value}[{a_uncertainty + b_uncertainty}]"


def subtraction(a: str, b: str) -> str:
    a_value, a_uncertainty = parse_value_and_uncertainty(a)
    b_value, b_uncertainty = parse_value_and_uncertainty(b)
    return f"{a_value - b_value}[{a_uncertainty + b_uncertainty}]"


def multiplication(a: str, b: str) -> str:
    a_value, a_uncertainty = parse_value_and_uncertainty(a)
    b_value, b_uncertainty = parse_value_and_uncertainty(b)
    result = a_value * b_value
    uncertainty = result * ((a_uncertainty / a_value) + (b_uncertainty / b_value))
    return f"{result}[{uncertainty}]"


def division(a: str, b: str) -> str:
    a_value, a_uncertainty = parse_value_and_uncertainty(a)
    b_value, b_uncertainty = parse_value_and_uncertainty(b)
    result = a_value / b_value
    uncertainty = result * ((a_uncertainty / a_value) + (b_uncertainty / b_value))
    return f"{result}[{uncertainty}]"


def parse_value_and_uncertainty(n: str) -> tuple[float, float]:
    uncertainty_left_index = n.find("[")
    value = float(n[0:uncertainty_left_index])
    uncertainty = float(n[uncertainty_left_index + 1:-1])
    return value, uncertainty


def parse(s: str) -> str:
    def evaluate(expression: str) -> str:

        expression = expand_scientific_notation(expression)
        expression = expression.replace("+-", "-").replace("-+", "-").replace("--", "+")



        while "(" in expression:
            last_open_bracket_index = expression.rfind("(")
            first_close_bracket_index = expression.find(")", last_open_bracket_index)
            inner_result = evaluate(expression[last_open_bracket_index + 1:first_close_bracket_index])
            expression = expression[:last_open_bracket_index] + inner_result + expression[first_close_bracket_index + 1:]

        operators = {"*": multiplication, "/": division, "+": addition, "-": subtraction}
        rawOperatorSet = set("*/+-")
        for operator in rawOperatorSet:
            while operator in expression:
                subCount = expression.count("-")

                if subCount == 1:

                    hasOtherOperations = False
                    hasCompleted = False
                    for nonSubOperator in "*+/":
                        if expression.count(nonSubOperator) > 0: hasOtherOperations = True; break
                    hasCompleted = expression.count("[") == 1
                    if not hasOtherOperations and hasCompleted: return expression

                    
                operator_index = expression.find(operator)
                left, right = get_arguments(expression, operator_index)
                expression = expression.replace(f"{left}{operator}{right}", operators[operator](left, right), 1)
        return expression

    def get_arguments(expression: str, operator_index: int) -> tuple[str, str]:
        special_characters = set("*+-/()")
        start_index = operator_index - 1
        end_index = operator_index + 1

        while start_index > 0 and expression[start_index] not in special_characters:
            start_index -= 1
        if expression[start_index] in special_characters:
            start_index += 1
            if expression[start_index] == "-":
                if expression[start_index-1] in special_characters:
                    start_index -= 1


        while end_index < len(expression) and expression[end_index] not in special_characters:
            end_index += 1

        left = expression[start_index:operator_index]
        right = expression[operator_index + 1:end_index]
        return left, right

    return evaluate(s)

def is_valid_number_with_uncertainty(n) -> bool:
    pattern = r'^-?\d+(\.\d+)?(e[+-]?\d+)?\[-?\d+(\.\d+)?(e[+-]?\d+)?\]$'
    return bool(re.match(pattern, n))

def populate_column_variables(column : int) -> list[str]:
    return [chr(97+i) for i in range(column)]

# introduction

print("enter your table of results 1 row at a time; each value must have an uncertainty")
print("this can be achieved by adding square brackets afterwards, e.g. 4[0.01]")
print("separate the columns in the rows using commas; incorrectly formatted rows must be redone")
print("end the table by entering \"end\" without quotes")
print("use e for x10^: e.g. 1e3 = 1000, 1e-3 = 0.001 ")
print("(e.g. 1 row would be \"24[0.01], 40[0.001]\". spaces do not matter.)")

# gathering data

table = []
column_widths = []
columns = 0

x = "n"


while x:
    x = input()
    if x == "end": break
    row = x.split(",")
    if columns !=  0 and len(row) != columns: print(LENGTH_ERROR); continue

    row_for_table = []

    while len(column_widths) < len(row):
        column_widths.append(0)

    has_failed_conversion = False
    for e, num in enumerate(row):
        num = num.strip()
        if not is_valid_number_with_uncertainty(num): print(FORMAT_ERROR); has_failed_conversion = True; break
        
        column_widths[e] = max(column_widths[e], len(num))

        row_for_table.append(num)

    if has_failed_conversion: continue
    table.append(row_for_table)
    columns = len(row)


# expression
print("what would you like to calculate?")
print("each row is of the form a, b, c, d ...")
print("for example, enter \"a * (b + 50)\" without quotes to get the product of a and 50 more than b")
print("* for multiply, / for divide, + for add, - for subtract, () for brackets")
print("keep entering expressions; type \"end\" without quotes to finish")

y = "n"

variables = populate_column_variables(columns)
special_characters = set("+-*/()[]")
expressions = []

# each entry is a column
results = []

expression_column_width_index = len(column_widths)

while y:

    y = input()

    if y == "end": break

    is_invalid_expression = any(
        char not in variables and char not in special_characters and not char.isdigit()
        for char in y.replace(" ", "")
    )
    if is_invalid_expression: print(EXPRESSION_FORMAT_ERROR); continue

    expressions.append(y)

    y = re.sub(r'(\d+)', r'\1[0]', y) # add uncertainty of 0 to every number in the expression

    expression_column = []

    for row in table:
        variable_to_value = {var: value for var, value in zip(variables, row)}
        expression = y
        minimum_sf = 999
        for var, value in variable_to_value.items():
            minimum_sf = min(count_sigfigs(parse_value_and_uncertainty(value)[0]), minimum_sf)
            expression = expression.replace(var, str(value))

        n = parse_value_and_uncertainty(parse(expression))
        value_formatted = str(round_to_sig_figs(n[0], minimum_sf))
        uncertainty_formatted = str(round_to_sig_figs(n[1], 1))
        if value_formatted[-1] == ".": value_formatted = value_formatted[:-1]
        if uncertainty_formatted[-1] == ".": uncertainty_formatted = uncertainty_formatted[:-1]
        final_result = f"{value_formatted}[{uncertainty_formatted}]"
        expression_column.append(final_result)

    results.append(expression_column)
    column_widths.append(max([len(h) for h in expression_column] + [len(y)]))

table_headers : str = "|"

for e, variable in enumerate(variables):
    table_headers += f"{variable}".center(column_widths[e]) + "|"

for e, expression in enumerate(expressions):
    table_headers += f"{expression}".center(column_widths[expression_column_width_index + e]) + "|"

row_to_print = []

for n, row in enumerate(table):
    txt = "|"
    for e, num in enumerate(row):
        txt += f"{num}".center(column_widths[e]) + "|"
    for e, result in enumerate(results):
        txt += f"{result[n]}".center(column_widths[expression_column_width_index + e]) + "|"
    row_to_print.append(txt)


print(table_headers)
for row in row_to_print:
    print(row)




        




    


