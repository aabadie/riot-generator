/*
 * Copyright (C) {year} {organization}
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     boards_{name}
 * @{{
 *
 * @file
 * @brief       Board specific definitions for the {displayed_name}
 *
 * @author      {author_name} <{author_email}>
 */

#ifndef BOARD_H
#define BOARD_H

#include "cpu.h"
#include "periph_conf.h"
#include "periph_cpu.h"

#ifdef __cplusplus
extern "C" {{
#endif

/**
 * @brief   Initialize board specific hardware
 */
void board_init(void);

#ifdef __cplusplus
}}
#endif

#endif /* BOARD_H */
/** @}} */