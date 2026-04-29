#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 test_orga
# SPDX-License-Identifier: LGPL-2.1-only

import sys

from testrunner import run


def testfunc(child):
    # put here the pexpect code that checks the output of the test application.
    pass


if __name__ == "__main__":
    sys.exit(run(testfunc))
