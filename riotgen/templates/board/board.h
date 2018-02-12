/*
 * Copyright (C) {year} {copyright_group}
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @defgroup    boards_{board} {board_name}
 * @ingroup     boards
 * @brief       Support for the {board_name} board.
 * @{
 *
 * @file
 * @brief       Board specific definitions for the {board_name}
 *
 * @author      Alexandre Abadie <alexandre.abadie@inria.fr>
 */

#ifndef BOARD_H
#define BOARD_H

#include "cpu.h"
#include "periph_conf.h"
#include "periph_cpu.h"

#ifdef __cplusplus
extern "C" {
#endif

{xtimer_config}
{led_defs}
{btn_defs}

/**
 * @brief   Initialize board specific hardware
 */
void board_init(void);

#ifdef __cplusplus
}
#endif

#endif /* BOARD_H */
/** @} */