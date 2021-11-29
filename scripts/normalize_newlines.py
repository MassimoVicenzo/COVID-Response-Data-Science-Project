import os.path as op
from os import getcwd
import argparse as ap
import csv

def parse_input():
    parser = ap.ArgumentParser()
    parser.add_argument('-p', '--csvpath', required=True)

    args = parser.parse_args()

    path = op.normpath(op.join(getcwd(), args.csvpath))

    return path

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append(row)
    return header, rows

    
def write(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            text = row[1]
            text = '\n'.join(text.splitlines())
            writer.writerow(row[:1] + [text] + row[2:])

def main():
    path = parse_input()
    header, rows = read(path)
    write(path, header, rows)



if __name__ == '__main__':
    main()