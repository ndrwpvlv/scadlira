# -*- coding: utf-8 -*-

import argparse
import sys

from scadlira.converter import ScadModel


def args_get() -> dict:
    parser = argparse.ArgumentParser(
            prog='SCAD to LIRA-SAPR input file converter',
            description='Converter of SCAD text file to Lira-SAPR text file', )
    parser.add_argument('-f', '--filename',
                        help="Enter filename of Scad text file", type=str)
    args = parser.parse_args(sys.argv[1:])
    return {'filename': args.filename}


def main():
    args = args_get()
    print('-----------------\nSCAD to LIRA-SAPR input file converter\n-----------------\n')
    print('Solution variables:')
    for key in args:
        print('{}: {}'.format(key, args[key]))
    print('-----------------\n')
    model = ScadModel(args['filename'])
    model.write_liratxt()


if __name__ == '__main__':
    main()
