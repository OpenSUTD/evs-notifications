from os.path import join

ROOT_DIR = '.'
DATA_DIR = 'data'
FILENAME = 'accounts.csv'


def parse_line(line):
    line = line.strip()
    username, password, *rest = line.split(',')  # third column optional
    name = ''.join(rest)
    return username, password, name


def parse_accounts():
    path = join(ROOT_DIR, DATA_DIR, FILENAME)
    print(path)
    with open(path, 'r') as f:
        accounts = [parse_line(line) for line in f]
    return accounts


if __name__ == '__main__':
    print(parse_accounts())

