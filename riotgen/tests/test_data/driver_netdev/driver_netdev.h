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
 * @{
 * @file
 * @brief       Netdev driver definitions for Test driver
 *
 * @author      test_name <test_email>
 */

#include "net/netdev.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief   Reference to the netdev device driver struct
 */
extern const netdev_driver_t test_driver;

#ifdef __cplusplus
}
#endif

/** @} */
