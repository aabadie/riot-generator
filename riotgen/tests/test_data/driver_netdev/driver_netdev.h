/*
 * SPDX-FileCopyrightText: 2026 test_orga
 * SPDX-License-Identifier: LGPL-2.1-only
 */

#pragma once

/**
 * @ingroup     drivers_test
 * @{
 *
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
