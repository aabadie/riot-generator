/*
 * SPDX-FileCopyrightText: 2026 test_orga
 * SPDX-License-Identifier: LGPL-2.1-only
 */

#pragma once

/**
 * @defgroup    drivers_test Test
 * @ingroup     drivers_netdev
 * @brief       test brief description
 * @{
 *
 * @file
 *
 * @author      test_name <test_email>
 */

#include "net/netdev.h"
/* Add header includes here */

#ifdef __cplusplus
extern "C" {
#endif

/* Declare the API of the driver */

/**
 * @brief   Device initialization parameters
 */
typedef struct {
    /* add initialization params here */
} test_params_t;

/**
 * @brief   Device descriptor for the driver
 */
typedef struct {
    netdev_t netdev;                        /**< Netdev parent struct */
    /** Device initialization parameters */
    test_params_t *params;
} test_t;

/**
 * @brief   Setup the radio device
 *
 * @param[in] dev                       Device descriptor
 * @param[in] params                    Parameters for device initialization
 * @param[in] index                     Index of @p params in a global parameter struct array.
 *                                      If initialized manually, pass a unique identifier instead.
 */
void test_setup(test_t *dev, const test_params_t *params, uint8_t index);

/**
 * @brief   Initialize the given device
 *
 * @param[inout] dev                    Device descriptor of the driver
 *
 * @return                  0 on success
 */
int test_init(test_t *dev);

#ifdef __cplusplus
}
#endif

/** @} */
