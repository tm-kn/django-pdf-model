#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line


def runtests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_pdf.tests.demosite.' \
                                           'demo_settings'

    execute_from_command_line([sys.argv[0], 'test'] + sys.argv[1:])


if __name__ == "__main__":
    runtests()
