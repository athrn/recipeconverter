import sys
    
from argparse import ArgumentParser, FileType

from convert import convert
from codecs import open

from units import units

def run_parse_args(args):
    systems = list(units.by_system)
    p = ArgumentParser(description="Convert recipes from US to European measures and vice versa")
    p.add_argument('-f', '--from', dest='from_', default='us', choices=systems)
    p.add_argument('-t', '--to', default='eur', choices=systems)
    p.add_argument('FILE',
                   nargs='?',
                   type=FileType('rb'),
                   default=sys.stdin)
    # TODO: Add output file
    x = p.parse_args(args)
    text = x.FILE.read()
    
    # TODO: HACK: Assume utf-8
    text = text.decode('utf-8')
    return convert(text, to=x.to, from_=x.from_)

def main():
    ret = run_parse_args(sys.argv[1:])
    print(ret)

if __name__ == "__main__":
    main()
