#!/usr/bin/python3

import argparse
import csv
import os
import os.path
import re
import sys

DESCRIPTION='Reads a CSV file (e.g. exported from Google Sheets) and converts it to a series of .properties files used for localization. See README.md for the expected input format.'

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

    keys = []
    outputs = {suffix: [] for suffix in suffixes}

    for line in reader:
        key = line[0]
        keys.append(key)
        for index, value in enumerate(line[2:]):
            if value:
                if value == '***EMPTY***':
                    value = ''
                outputs[suffixes[index]].append('%s=%s' % (key, value))

    return keys, outputs

def generate_enum(output, enum_name, keys):
    package_name, class_name = enum_name.rsplit('.', 1)

    if package_name:
        print('package %s;' % package_name, file=output)
        print('', file=output)
    print('// Generated by csv2properties. Do not modify!', file=output)
    print('public enum %s {' % class_name, file=output)
    for key in keys:
        print('\t%s,' % key, file=output)
    print('}', file=output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('csv_file', help='CSV file to read from; "-" to read from stdin')
    parser.add_argument('--properties_dir', default='.', help='output directory to write .properties files to; defaults to the current directory')
    parser.add_argument('--properties_prefix', default='strings', help='prefix for generated .properties files; defaults to "strings"')
    parser.add_argument('--java_dir', default='.', help='directory to output Java sources to (excluding package subdirs); defaults to the current directory')
    parser.add_argument('--java_enum', help='fully qualified name of Java enum to generate')
    args = parser.parse_args()

    with open_input(args.csv_file) as input:
        keys, outputs = parse_input(input)

    for suffix, lines in outputs.items():
        output_file_name = os.path.join(args.properties_dir, args.properties_prefix + suffix + '.properties')
        print('Writing %s...' % output_file_name, file=sys.stderr)
        with open(output_file_name, 'w', encoding='utf8') as output:
            for line in lines:
                print(line, file=output)

    if args.java_enum:
        java_file_name = os.path.join(args.java_dir, args.java_enum.replace('.', os.sep) + '.java')
        print('Writing %s...' % java_file_name, file=sys.stderr)
        with open(java_file_name, 'w', encoding='utf8') as java_output:
            generate_enum(java_output, args.java_enum, keys)
