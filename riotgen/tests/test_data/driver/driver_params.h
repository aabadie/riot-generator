/*
 * Copyright (C) 2025 test_orga
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

#pragma once

/**
 * @ingroup     drivers_test
 *
 * @{
 * @file
 * @brief       Default configuration
 *
 * @author      test_name <test_email>
 */

#include "board.h"
#include "test.h"
#include "test_constants.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @name    Set default configuration parameters
 * @{
 */
#ifndef TEST_PARAM_PARAM1
#define TEST_PARAM_PARAM1
#endif

#ifndef TEST_PARAMS
#define TEST_PARAMS
#endif
/**@}*/

/**
 * @brief   Configuration struct
 */
static const test_params_t test_params[] =
{
    TEST_PARAMS
};

#ifdef __cplusplus
}
#endif

/** @} */
