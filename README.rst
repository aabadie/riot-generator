RIOT code generator
-------------------

|PyPi|

.. |PyPi| image:: https://badge.fury.io/py/riotgen.svg
    :target: https://badge.fury.io/py/riotgen
    :alt: riotgen version

RIOT generator is a command line interface helper that initiates `RIOT
<http://github.com/RIOT-OS/RIOT>`_ source files for applications, boards
support, packages and test applications.

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

RIOT code generator uses subcommands for generating the code for applications,
tests, packages and board support.

    riotgen --help
    Usage: riotgen [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      application  Bootstrap a RIOT application
      board        Bootstrap a RIOT board support
      example      Bootstrap a RIOT example application
      pkg          Bootstrap a RIOT external package
      test         Bootstrap a RIOT test application


Examples
........

Generate an application in the current directory that build against the RIOT
source located in /opt/RIOT and using the interactive wizzard:

    riotgen application -i -r /opt/RIOT

or

    RIOTBASE=/opt/RIOT riotgen application -i

The command line wizard will ask for questions about the new
application: target board, RIOT base directory, author name, etc.

Generate an application using a configuration file (see the
`samples <https://github.com/aabadie/riot-generator/tree/master/riotgen/samples>`_
provided in the source code::):

    riotgen application --riotbase /opt/RIOT --config path/to/config/file.cfg


In both cases, once complete, the new application can be built using::

    make

``example``, ``pkg``, ``test`` and ``board`` will generated the skeleton code
directly in the RIOT base directory::

    riotgen example --riotbase /opt/RIOT -i
    riotgen pkg --riotbase /opt/RIOT -i
    riotgen board --riotbase /opt/RIOT -i
    riotgen test --riotbase /opt/RIOT -i
