#!/usr/bin/env python3

# Copyright (C) 2025 test_orga
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

import sys

from testrunner import run


def testfunc(child):
    # put here the pexpect code that checks the output of the test application.
    pass


if __name__ == "__main__":
    sys.exit(run(testfunc))
