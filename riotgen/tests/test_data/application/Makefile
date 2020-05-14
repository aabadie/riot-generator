# name of the application
APPLICATION = test

# If no BOARD is found in the environment, use this default:
BOARD ?= board_test

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= 

# required modules
USEMODULE += fmt
USEMODULE += xtimer

# required features
FEATURES_REQUIRED += periph_gpio

# Comment this out to disable code in RIOT that does safety checking
# which is not needed in a production environment but helps in the
# development process:
DEVELHELP ?= 1

# Change this to 0 show compiler invocation lines by default:
QUIET ?= 1

include $(RIOTBASE)/Makefile.include
