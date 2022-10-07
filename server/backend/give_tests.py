import os


def give_tests():
    tests = []

    for file in os.listdir('../tests'):
        if file.endswith('.txt'):
            with open('../tests/' + file) as f:
                try:
                    tests.append(eval(f.read()))
                except:
                    continue

    return tests


if __name__ == '__main__':
    print(give_tests())
