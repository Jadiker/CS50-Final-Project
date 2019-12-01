# by London Lowmanstone (from high school)

def print_percent(index_number, out_of, increment_amt=1, round_amt=0):
    '''Prints the progress through a loop.

    If you're running a for loop like `for i in range(max_val)`
    then in the loop you can call printPercent(i, max_val) to print the percentage that the loop is done.
    This doens't work perfectly because of rounding error, but it's close enough.
    (Sometimes it will skip or double print a number.)
    '''
    print_pc = 100.0 * (index_number + 1) / out_of
    if print_pc % increment_amt < (100.0 / out_of):
        print("{}%...".format(round(print_pc, round_amt)))
