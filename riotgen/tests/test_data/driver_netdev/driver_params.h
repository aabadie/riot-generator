/*
 * SPDX-FileCopyrightText: 2026 test_orga
 * SPDX-License-Identifier: LGPL-2.1-only
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
#  define TEST_PARAM_PARAM1
#endif

#ifndef TEST_PARAMS
#  define TEST_PARAMS
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
