#!/usr/bin/python

'''
    ems - EMS flashcart utility

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
import argparse

PARSER = argparse.ArgumentParser(
    description='EMS flashcart utility')

PARSER.add_argument('-r', '--header', action="store_true",
                    help='read header')
PARSER.add_argument('-s', '--sram', action="store_true",
                    help='read sram')
PARSER.add_argument('-o', '--output', help='output filename')

ARGS = PARSER.parse_args()

# USB DEFINITIONS
VENDOR = 0x4670
PRODUCT = 0x9394

READ_ENDPOINT = 0x81
WRITE_ENDPOINT = 0x2
READ_TIMEOUT = 200
WRITE_TIMEOUT = 400

# ROM DEFINITIONS
HEADER_LENGTH = 0x200
ROM_HEADER_START = 0x134
BANKS = [1, 2]
BANK1_START = '\x00\x00\x00\x00'
BANK2_START = '\x00\x40\x00\x00'

# EMS COMMANDS
EMS_READ = '\xff'

DEV = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)

def _init():
    '''_init - initalize and capture the usb device'''

    if DEV is None:
        raise ValueError('Device not found')

    DEV.set_configuration()

    # get an endpoint instance
    cfg = DEV.get_active_configuration()
    intf = cfg[(0, 0)]

    ep_ = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

    assert ep_ is not None

def _readcart():
    '''_readcart - read the header of bank 1 and 2 the cart'''
    print "Reading Cart Headers"

    for bank in BANKS:
        addr = BANK1_START if bank == 1 else BANK2_START
        msg = EMS_READ + addr + '\x00\x00\x02\x00'
        res = _usbbulktransfer(msg, HEADER_LENGTH)
        print "Game: " + res[ROM_HEADER_START:0x144]

def _usbbulktransfer(msg, length):
    '''_usbbulktransfer - send the given msg to the USB device'''

    DEV.write(WRITE_ENDPOINT, msg, WRITE_TIMEOUT)
    ret = DEV.read(READ_ENDPOINT, length, WRITE_TIMEOUT)
    sret = ''.join([chr(x) for x in ret])

    return sret

def main():
    '''main - master of all'''
    _init()
    if ARGS.header:
        _readcart()

main()