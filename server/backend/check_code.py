def check_code(code, args):
    for i in args:
        if type(i) == str:
            code = code.replace('input()', f"'{str(i)}'", 1)
        else:
            code = code.replace('input()', str(i), 1)

    exec(code)


if __name__ == '__main__':
    check_code("""a = input()\nb = input()\nprint(a + b)""", (1, 2))
