import constants
import functions
from sys import argv

if __name__ == '__main__':
    script, text, k, n = argv
    if not k:
        k = constants.DEFAULT_K
    else:
        k = int(k)

    if not n:
        n = constants.DEFAULT_N
    else:
        n = int(n)

    functions.get_info_about_text(text, n, k)
