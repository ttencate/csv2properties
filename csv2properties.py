#!/usr/bin/python3

import argparse
import csv
import os.path
import re
import sys

DESCRIPTION='Reads a CSV file (e.g. exported from Google Sheets) and converts it to a series of .properties files used for localization.'

def open_input(file_name):
    if file_name == '-':
        return sys.stdin
    else:
        return open(file_name, encoding='utf8')

def get_suffixes(header):
    suffixes = header[2:]
    for index, suffix in enumerate(suffixes):
        if not re.match(r'^(_[a-zA-Z]{2})*$', suffix):
            raise RuntimeError('invalid language/country/region code "%s" in column %d' % (suffix, index + 2))
    return suffixes

def parse_input(input):
    reader = csv.reader(input)
    header = next(reader)
    suffixes = get_suffixes(header)

    outputs = {suffix: [] for suffix in suffixes}

    for line in reader:
        key = line[0]
        for index, value in enumerate(line[2:]):
            if value:
                if value == '***EMPTY***':
                    value = ''
                outputs[suffixes[index]].append('%s=%s' % (key, value))

    return outputs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('csv_file', help='CSV file to read from; "-" to read from stdin')
    parser.add_argument('out_dir', help='output directory to write .properties files to')
    parser.add_argument('--prefix', default='strings', help='prefix for generated .properties files; defaults to "strings"')
    args = parser.parse_args()

    with open_input(args.csv_file) as input:
        data = parse_input(input)

    for suffix, lines in data.items():
        output_file_name = os.path.join(args.out_dir, args.prefix + suffix + '.properties')
        print('Writing %s...' % output_file_name, file=sys.stderr)
        with open(output_file_name, 'w', encoding='utf8') as output:
            for line in lines:
                print(line, file=output)
