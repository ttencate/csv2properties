#!/usr/bin/python3

import csv
import os.path
import re
import sys

USAGE = '''Usage: csv2properties CSV_FILE OUT_DIR [PREFIX]

Reads a CSV file (e.g. exported from Google Sheets) and converts it to a series
of .properties files used for localization.

If CSV_FILE is "-", input is read from stdin.

If PREFIX is not given, it defaults to "strings", resulting in files named
"strings.properties", "strings_en_US.properties", and so on.'''

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
    if len(sys.argv) < 3:
        print(USAGE, file=sys.stderr)
        sys.exit(0)

    file_name = sys.argv[1]
    out_dir = sys.argv[2]
    prefix = sys.argv[3] if len(sys.argv) > 3 else 'strings'

    with open_input(file_name) as input:
        data = parse_input(input)

    for suffix, lines in data.items():
        output_file_name = os.path.join(out_dir, prefix + suffix + '.properties')
        print('Writing %s...' % output_file_name, file=sys.stderr)
        with open(output_file_name, 'w', encoding='utf8') as output:
            for line in lines:
                print(line, file=output)
