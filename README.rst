riotgen: a RIOT source code generator
-------------------------------------

|CI| |codecov| |PyPi|

.. |CI| image:: https://github.com/aabadie/riot-generator/workflows/CI/badge.svg
    :target: https://github.com/aabadie/riot-generator/actions?query=workflow%3ACI+branch%3Amain
    :alt: CI status

.. |codecov| image:: https://codecov.io/gh/aabadie/riot-generator/branch/main/graph/badge.svg
  :target: https://codecov.io/gh/aabadie/riot-generator

.. |PyPi| image:: https://badge.fury.io/py/riotgen.svg
    :target: https://badge.fury.io/py/riotgen
    :alt: riotgen version

``riotgen`` is a command line interface helper tool that is used to bootstrap
`RIOT <http://github.com/RIOT-OS/RIOT>`_ source files for standalone applications,
board supports, driver modules, system modules, packages and example/test applications.

Installation
............

Install ``riotgen`` using ``pip``::

    pip install riotgen

Installing from source
......................

Clone this repository::

    git clone git://github.com/aabadie/riot-generator.git

Install using ``pip`` from the source directory::

    cd riot-generator
    pip install .

Usage
.....

``riotgen`` uses subcommands for generating the code for applications,
tests, packages and board support::

    riotgen --help
    Usage: riotgen [OPTIONS] COMMAND [ARGS]...

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      application  Bootstrap a RIOT application
      board        Bootstrap a RIOT board support
      driver       Bootstrap a RIOT driver module
      example      Bootstrap a RIOT example application
      module       Bootstrap a RIOT system module
      pkg          Bootstrap a RIOT external package
      test         Bootstrap a RIOT test application


Examples
........

Generate an application in the current directory that build against the RIOT
source located in /opt/RIOT and using the interactive wizzard::

    riotgen application -i -r /opt/RIOT

or::

    RIOTBASE=/opt/RIOT riotgen application -i

The command line wizard will ask for questions about the new
application: target board, RIOT base directory, author name, etc.

Generate an application using a configuration file (see the
`samples <https://github.com/aabadie/riot-generator/tree/main/riotgen/samples>`_
provided in the source code)::

    riotgen application --riotbase /opt/RIOT --config path/to/config/file.cfg


In both cases, once complete, the new application can be built using::

    make

``example``, ``driver``, ``module``, ``pkg``, ``test`` and ``board`` subcommands generate
the skeleton code directly in the RIOT base directory::

    riotgen example --riotbase /opt/RIOT -i
    riotgen driver --riotbase /opt/RIOT -i
    riotgen module --riotbase /opt/RIOT -i
    riotgen pkg --riotbase /opt/RIOT -i
    riotgen board --riotbase /opt/RIOT -i
    riotgen test --riotbase /opt/RIOT -i


Testing
.......

Testing is performed using the `Tox <http://github.com/tox-dev/tox>`_
automation tool. You can install Tox using pip::

    pip install tox

To run the whole tests and checks, use::

    tox

To only run the tests, use::

    tox -e tests

To only run the static checks (``flake8``, ``black``, ``twine --check``), use::

    tox -e check

To reformat your code following the `black <https://black.readthedocs.io/en/stable>`_
tool, use::

    tox -e format
