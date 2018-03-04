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

The ``application`` subcommand requires a ``<path>`` argument to set the
directory where the application code will be generated::

    riotgen application <output directory>

Then this command starts a command line wizard with questions about the new
application: target board, RIOT base directory, author name, etc.

Once complete, the new application can be built using::

    make -C <output directory>

``example``, ``pkg``, ``test`` and ``board`` subcommands can just be called
without parameters, the code is generated directly in the RIOT base directory::

    riotgen example
    riotgen pkg
    riotgen board
    riotgen test

Use ``--config`` option to pass a configuration file with predefined parameters
to ``riotgen``.
`Samples <https://github.com/aabadie/riot-generator/tree/master/riotgen/samples>`_
are provided in the source code::

    riotgen board --config path/to/config/file.cfg
