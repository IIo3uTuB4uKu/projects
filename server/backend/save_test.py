import os


def save(test):
    if os.listdir('../tests') == []:
        with open('../tests/test1.txt', 'w') as f:
            f.write(test)
        return

    for file in os.listdir('../tests'):
        if file.endswith('.txt'):
            end_num = int(file.replace('test', '').replace('.txt', ''))

    with open('../tests/test' + str(end_num + 1) + '.txt', 'w') as f:
        f.write(test)


if __name__ == '__main__':
    save("test")
