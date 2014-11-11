#!/usr/bin/python

import usb.core
import usb.util

VENDOR = 0x4670
PRODUCT = 0x9394

dev = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)

if dev is None:
    raise ValueError('Device not found')

dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

print dev