import argparse

parser = argparse.ArgumentParser(description='py2musicxml')

parser.add_argument(
    '-o', '--output-dir', help='write any output files to this directory'
)


def _output(msg):
    print(msg)


def main():
    args = parser.parse_args()

    _output('** py2musicxml {}'.format('*' * 30))


if __name__ == '__main__':
    main()
