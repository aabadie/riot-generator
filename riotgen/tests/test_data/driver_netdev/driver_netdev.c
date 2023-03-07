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
 * @file
 * @brief       Netdev adaptation for the Test driver
 *
 * @author      test_name <test_email>
 * @}
 */

#include <assert.h>
#include <stddef.h>
#include <string.h>
#include <errno.h>

#include "iolist.h"
#include "net/netopt.h"
#include "net/netdev.h"

#include "test.h"
#include "test_netdev.h"

#define ENABLE_DEBUG 0
#include "debug.h"

static int _send(netdev_t *netdev, const iolist_t *iolist)
{
    test_t *dev = (test_t *)netdev;

    uint8_t size = iolist_size(iolist);

    /* Ignore send if packet size is 0 */
    if (!size) {
        return 0;
    }

    DEBUG("[test] netdev: sending packet now (size: %d).\n", size);
    /* Write payload buffer */
    for (const iolist_t *iol = iolist; iol; iol = iol->iol_next) {
        if (iol->iol_len > 0) {
            /* write data to payload buffer */
        }
    }

    state = NETOPT_STATE_TX;
    netdev->driver->set(netdev, NETOPT_STATE, &state, sizeof(uint8_t));
    DEBUG("[test] netdev: send: transmission in progress.\n");

    return 0;
}

static int _recv(netdev_t *netdev, void *buf, size_t len, void *info)
{
    DEBUG("[test] netdev: read received data.\n");

    test_t *dev = (test_t *)netdev;
    uint8_t size = 0;

    /* Get received packet info and size here */

    if (buf == NULL) {
        return size;
    }

    if (size > len) {
        return -ENOBUFS;
    }

    /* Read the received packet content here and write it to buf */

    return 0;
}

static int _init(netdev_t *netdev)
{
    test_t *dev = (test_t *)netdev;

    /* Launch initialization of driver and device */
    DEBUG("[test] netdev: initializing driver...\n");
    if (test_init(dev) != 0) {
        DEBUG("[test] netdev: initialization failed\n");
        return -1;
    }

    DEBUG("[test] netdev: initialization successful\n");
    return 0;
}

static void _isr(netdev_t *netdev)
{
    test_t *dev = (test_t *)netdev;

    /* Handle IRQs here */
}

static int _get_state(test_t *dev, void *val)
{
    netopt_state_t state = NETOPT_STATE_OFF;
    memcpy(val, &state, sizeof(netopt_state_t));
    return sizeof(netopt_state_t);
}

static int _get(netdev_t *netdev, netopt_t opt, void *val, size_t max_len)
{
    (void)max_len; /* unused when compiled without debug, assert empty */
    test_t *dev = (test_t *)netdev;

    if (dev == NULL) {
        return -ENODEV;
    }

    switch (opt) {
    case NETOPT_STATE:
        assert(max_len >= sizeof(netopt_state_t));
        return _get_state(dev, val);

    default:
        break;
    }

    return -ENOTSUP;
}

static int _set_state(test_t *dev, netopt_state_t state)
{
    switch (state) {
    case NETOPT_STATE_STANDBY:
        DEBUG("[test] netdev: set NETOPT_STATE_STANDBY state\n");
        break;

    case NETOPT_STATE_IDLE:
        DEBUG("[test] netdev: set NETOPT_STATE_RX state\n");
        break;

    case NETOPT_STATE_RX:
        DEBUG("[test] netdev: set NETOPT_STATE_RX state\n");
        break;

    case NETOPT_STATE_TX:
        DEBUG("[test] netdev: set NETOPT_STATE_TX state\n");
        break;

    case NETOPT_STATE_RESET:
        DEBUG("[test] netdev: set NETOPT_STATE_RESET state\n");
        break;

    default:
        return -ENOTSUP;
    }
    return sizeof(netopt_state_t);
}

static int _set(netdev_t *netdev, netopt_t opt, const void *val, size_t len)
{
    (void)len; /* unused when compiled without debug, assert empty */
    test_t *dev = (test_t *)netdev;
    int res = -ENOTSUP;

    if (dev == NULL) {
        return -ENODEV;
    }

    switch (opt) {
    case NETOPT_STATE:
        assert(len == sizeof(netopt_state_t));
        return _set_state(dev, *((const netopt_state_t *)val));

    default:
        break;
    }

    return res;
}

const netdev_driver_t test_driver = {
    .send = _send,
    .recv = _recv,
    .init = _init,
    .isr = _isr,
    .get = _get,
    .set = _set,
};
