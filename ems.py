#!/usr/bin/python

'''
    ems - Simple reader for EMS flashcart

    Copyright (C) 2014, Tomasz Finc <tomasz@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

'''

import usb.core
import usb.util

VENDOR = 0x4670
PRODUCT = 0x9394

DEV = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)

if DEV is None:
    raise ValueError('Device not found')

DEV.set_configuration()

# get an endpoint instance
CFG = DEV.get_active_configuration()
INTF = CFG[(0, 0)]

EP = usb.util.find_descriptor(
    INTF,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert EP is not None

print DEV