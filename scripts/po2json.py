#!/usr/bin/env python3
import argparse
import json

import polib


def main(args):
    out = {}
    po = polib.pofile(args.infile)
    for item in po:
        key = item.msgid
        # key = key.replace('{', '/').replace('}', '/')  # .replace('.', '_')
        out[key] = item.msgstr or item.msgid

    outargs = {
        'sort_keys': True,
        'indent': 4,
        'ensure_ascii': False,
    }
    if args.output == '-':
        print(json.dumps(out, **outargs))
    else:
        with open(args.output, 'w') as f:
            json.dump(out, f, **outargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="Input file (.po)")
    parser.add_argument("-o", "--output", type=str, help="Output file (.json)", default='-')
    args = parser.parse_args()
    main(args)
