RIOT code generator
-------------------

RIOT generator provides a command line interface for generating `RIOT
<http://github.com/RIOT-OS/RIOT>`_ source files for new applications, board
support and tests applications.

Installation
------------

Clone this repository::

    git clone git://github.com/aabadie/riot-generator.git

Install ``riotgen`` using ``pip``::

    cd riot-generator
    pip install .

The packages is not yet available on PyPI.

Usage
-----

RIOT code generator has subcommands for generating starting for applications,
tests and board support.

The ``application`` requires a <path> argument. This is where the application
code will be generated::

    riotgen application <output directory>

This command will start a command line wizard with some questions for
correctly initializing the application code (target board, RIOT base directory,
etc).

Once done, the new application can be built using::

    make -C <output directory>

``test`` and ``board`` subcommands can be called without parameters, the code
will be generated directly in the RIOT base directory::

    riotgen board
    riotgen test

Use ``--config`` option to pass a predefined configuration file to ``riotgen``.
`Samples <https://github.com/aabadie/riot-generator/tree/master/riotgen/samples>`_
are provided in the source code::

    riotgen board --config path/to/config/file.cfg
