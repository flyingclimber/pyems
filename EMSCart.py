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

class GameBoyRom:
    '''GameBoyRom - Rom header definitions'''
    # ROM DEFINITIONS
    ROM_HEADER_START = 0x134
    HEADER_LENGTH = 0x200

    def __init__(self):
        self.data = []

class EMSCart:
    '''EMSCart - EMS cart constants'''
    # USB DEFINITIONS
    VENDOR = 0x4670
    PRODUCT = 0x9394

    READ_ENDPOINT = 0x81
    WRITE_ENDPOINT = 0x2
    READ_TIMEOUT = 200
    WRITE_TIMEOUT = 400
  
    # CART
    BANKS = [1, 2]
    BANK_START = [None, '\x00\x00\x00\x00', '\x00\x40\x00\x00']

    # EMS COMMANDS
    READ_ROM = '\xff'
    READ_SRAM = '\x6d'
    END_ROM = '\x00\x00\x02\x00'
    END_SRAM = '\x00\x00\x10\x00'

    def __init__(self):
        self.data = []
