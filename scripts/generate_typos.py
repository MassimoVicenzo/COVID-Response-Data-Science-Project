import os.path as op
from os import getcwd
import argparse as ap
import spellchecker as sc
from spellchecker import SpellChecker

def parse_input():
    parser = ap.ArgumentParser()
    parser.add_argument('-k', '--keywords', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-d', '--distance', default=1)

    args = parser.parse_args()

    keywords_path = op.normpath(op.join(getcwd(), args.keywords))
    out_path = op.normpath(op.join(getcwd(), args.output))

    return keywords_path, out_path, int(args.distance)

def is_comment(line):
    return line[:2] == '//'

def generate_typos(word, spellchecker):
    typos = [word]
    possible_typos = sc.edit_distance_1(word)
    for possible_typo in possible_typos:
        if spellchecker.correction(word) == word:
            typos.add(possible_typo)
    return typos


def generate_typoed_line(line):
    words = line.split()
    for word in words:
        typos = 


def main():
    keywords_path, out_path, d = parse_input()

    spell = SpellChecker(distance=d)

    with open(keywords_path, 'r', encoding='utf-8') as in_f:
        with open(out_path, 'r', encoding='utf-8') as out_f:
            for line in in_f.readlines():
                if line[:2] == '//':
                

                new_keywords = line.split()
                for kw in new_keywords:
                    if kw 
                keywords.append(line)
    return keywords



if __name__ == '__main__':
    main()