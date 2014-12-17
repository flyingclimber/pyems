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
import io

from EMSCart import EMSCart
from EMSCart import GameBoyRom

PARSER = argparse.ArgumentParser(
    description='EMS flashcart utility')

PARSER.add_argument('-r', '--header', action="store_true",
                    help='read header')
PARSER.add_argument('-s', '--sram', action="store_true",
                    help='read sram')
PARSER.add_argument('-o', '--output', help='output filename')

ARGS = PARSER.parse_args()

ems = EMSCart()
gb = GameBoyRom()

BLOCK_READ = 4096

DEV = usb.core.find(idVendor=ems.VENDOR, idProduct=ems.PRODUCT)


### UTIL ###
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

def _usbbulktransfer(msg, length):
    '''_usbbulktransfer - send the given msg to the USB device'''

    DEV.write(ems.WRITE_ENDPOINT, msg, ems.WRITE_TIMEOUT)
    ret = DEV.read(ems.READ_ENDPOINT, length, ems.WRITE_TIMEOUT)
    sret = ''.join([chr(x) for x in ret])

    return sret

def _write(data):
    '''_write - write out data to file'''
    output = io.FileIO(ARGS.output, 'wb')
    output.write(data)

### END OF UTIL ###

### CART ###
def _readcart():
    '''_readcart - read bank 1 and 2 headers'''
    print "Reading EMS Cart Headers"

    for bank in ems.BANKS:
        addr = ems.BANK_START[bank]
        msg = ems.READ_ROM + addr + ems.END_ROM
        res = _usbbulktransfer(msg, gb.HEADER_LENGTH)
        print "Game: " + res[gb.ROM_HEADER_START:0x144]

def _readsram():
    '''_readsram - reads the sram of the cart'''
    print "Reading SRAM"

    addr = '\x00\x00\x00\x00'
    msg = ems.READ_SRAM + addr + ems.END_SRAM
    res = _usbbulktransfer(msg, 4096)
    return res

### END OF CART ###

### MAIN ###
def main():
    '''main - master of all'''
    _init()
    if ARGS.header:
        _readcart()
    elif ARGS.sram:
        sram = _readsram()
        if sram:
            _write(sram)

### END OF MAIN ###

main()
