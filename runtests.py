#!/usr/bin/env python
import argparse
import os
import sys

from django.core.management import execute_from_command_line


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only-checks', dest='only_checks',
                        action='store_const', const=True, default=False,
                        help='Run only checks.')
    return parser.parse_known_args()


def run_checks():
    execute_from_command_line([
        sys.argv[0],
        'check'
    ])
    execute_from_command_line([
        sys.argv[0],
        'makemigrations',
        '--dry-run',
        '--check'
    ])


def run_tests(args):
    execute_from_command_line([sys.argv[0], 'test'] + args)


def main():
    args, rest_args = parse_args()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_pdf.tests.demosite.' \
                                           'demo_settings'
    if args.only_checks:
        run_checks()
        return
    run_tests(rest_args)


if __name__ == "__main__":
    main()
