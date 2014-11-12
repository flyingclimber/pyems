pyems
=====
ems.py is a utility script that currently allows unidirectional communication
with the GB USB smart card 64M. Currently you can read the header and save the
ROMS in bank 0 and 1 to disk. 

I wrote it to better understand how the cart worked and may extend it later for
writting functionality.

Background
=====
The GB USB smart card 64M is a very simple flash rom based cartridge sold by
various distributors. It has two banks of 32M that can save a combination of
various GameBoy rom formats. While the cart can save multiple roms within its
two 32M pages, the SRAM is shared between both pages causing an overwrite
whenever a ROM decides to save its SRAM

Communicating with the cart is fairly straightfoward as all communications
can be done through USB bulk transfers. Bidrectional communication is possible
once the device is claimed using the proper vendor and product id's

<pre>
VENDOR = 0x4670
PRODUCT = 0x9394
</pre>

Commands
===
Communicaton with the cart consists of sending 9 byte messages similar to
<pre>
\xff\x00\x00\x00\x00\x00\x00\x02\x00
</pre>

All commands conform the the following format

<pre>
+---------------------+-----------+------------+
|        1byte        |   4byte   |    4byte   | 
+---------------------+-----------+------------+
|READ/WRITE (ROM/SRAM)|  Address  |    Value   |
+---------------------+-----------+------------+
</pre>

Thus the command above breaks down to the following which reads the cartridge header 

* '\xFF' - Read
* '\x00\x00\x00\x00' - Cart location 0x0000
* 'x00\x00\x02\x00' - ?

Available commands include
* '\xFF' - Read ROM
* '\x57' - Write ROM
* '\x6d' - Read SRAM
* '\x4d' - Write SRAM
