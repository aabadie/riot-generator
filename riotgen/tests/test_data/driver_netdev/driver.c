/*
 * Copyright (C) 2023 test_orga
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     drivers_test
 * @{
 *
 * @file
 * @brief       Device driver implementation for the Test
 *
 * @author      test_name <test_email>
 *
 * @}
 */

#include "test.h"
#include "test_constants.h"
#include "test_params.h"
#include "test_netdev.h"

void test_setup(test_t *dev, const test_params_t *params, uint8_t index)
{
    netdev_t *netdev = (netdev_t *)dev;

    netdev->driver = &test_driver;
    dev->params = (test_params_t *)params;
    netdev_register(&dev->netdev, NETDEV_TEST, index);
}

int test_init(test_t *dev)
{
    /* Initialize peripherals, gpios, setup registers, etc */

    return 0;
}
