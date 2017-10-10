from __future__ import print_function
import re
from pdb import set_trace


class ValidationError(Exception):
    def __init__(self, message):
        super(ValidationError, self).__init__(message)

def cast(cast_type):
    if cast_type == "Sym":
        return str
    elif cast_type == "Num":
        return float
    else:
        raise TypeError("Invalid element type")


def is_valid_row(row, head):
    """
    Checks for bad lines; i.e. Wrong number of cells.
    """
    if not len(row) == len(head):
        raise ValidationError("ValidationError: Incorrect row size. Skipping row.")

    return True


def read_csv(fname="POM3A.csv"):
    """
    Read each line, kill whitepsace and anything after comment characters (#), 
    break each line on comma, read rows into a list of lists (one list per row), 
    converting strings to numbers where appropriate. Note that some column 
    headers contain ?: all such columns should be ignored. For now you can 
    ignore the other magic characters in row1.
    """
    head = list()
    body = list()
    with open(fname) as f:
        lis = [re.sub("\n", "", line).split(",") for line in f]
        col_type = ["Num" if "$" in col else "skip" if "?" in col else "Sym"
                    for col in lis[0]]
        head = [re.sub("\$", "", el) for el in lis[0]]
        # set_trace()
        for row in lis[1:]:
            try:
                if is_valid_row(row, head): # Check #1: Is the row size correct
                    """
                    Check #2: try-except skips over elements that can't be 
                    properly converted
                    """
                    try:
                        body.append([cast(el_type)(el)
                                    for el, el_type in zip(row, col_type)])
                    except:
                        raise ValidationError("ValidationError: Row element type doesn't match column header. Skipping row.")
            except Exception as E:
                print(E)

    
    return body.insert(0, head)


def test_time_to_read_csv():
    from time import time
    t = time()
    read_csv(fname="POM3A.csv")
    print("Time to read file={0:.2f} seconds".format(time() - t))

def test_read_bad_csv():
    read_csv(fname="POM3A_bad.csv")


if __name__ == "__main__":
    test_time_to_read_csv()
    test_read_bad_csv()
