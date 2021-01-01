/*
 * Copyright (C) 2021 test_orga
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @defgroup    drivers_test Test
 * @ingroup     drivers_misc
 * @brief       test brief description
 *
 * @{
 *
 * @file
 *
 * @author      test_name <test_email>
 */

#ifndef TEST_H
#define TEST_H

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
    /** Device initialization parameters */
    test_params_t params;
} test_t;

/**
 * @brief   Initialize the given device
 *
 * @param[inout] dev        Device descriptor of the driver
 * @param[in]    params     Initialization parameters
 *
 * @return                  0 on success
 */
int test_init(test_t *dev, const test_params_t *params);

#ifdef __cplusplus
}
#endif

#endif /* TEST_H */
/** @} */
