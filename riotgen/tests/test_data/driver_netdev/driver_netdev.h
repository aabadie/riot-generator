/*
 * Copyright (C) 2021 test_orga
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     drivers_test
 * @{
 * @file
 * @brief       Netdev driver definitions for Test driver
 *
 * @author      test_name <test_email>
 */

#ifndef TEST_H
#define TEST_H

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

#endif /* TEST_H */
/** @} */
