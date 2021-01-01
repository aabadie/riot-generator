/*
 * Copyright (C) 2021 test_orga
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     boards_test
 * @{
 *
 * @file
 * @brief       Board specific implementations for the Test board
 *
 * @author      test_name <test_email>
 *
 * @}
 */

#include "cpu.h"
#include "board.h"
#include "periph/gpio.h"

void board_init(void)
{
    /* initialize the CPU */
    cpu_init();
}
