pyems
=====
ems.py is a utility script that currently allows bi-directional communication
with the GB USB smart card 64M. Currently you can read the header, save the
ROMS in bank 1 and 2 to disk, and write roms to bank 1 and 2 of the cart. 

I wrote it to better understand how the cart worked.

It's experimental at best so use it at your own risk.

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

Plus an additional 32 byte payload if writting data. Total command plus payload should not exceed 41 bytes.

All commands conform the the following format

<pre>
+---------------------+-----------+------------+------------+
|        1byte        |   4byte   |    4byte   |   32byte   |
+---------------------+-----------+------------+------------+
|READ/WRITE (ROM/SRAM)|  Address  |    Value   |    Value   |
+---------------------+-----------+------------+------------+
</pre>

Thus the command above breaks down to the following which reads the cartridge header 

* '0xFF' - Read
* '0x0' - Cart location 0x0 [4byte padded]
* 'x00\x00\x02\x00' - ?

Available commands include
* '0xFF' - Read ROM
* '0x57' - Write ROM
* '0x6d' - Read SRAM
* '0x4d' - Write SRAM

Hardware
====
* E28F640J3A-120 - INTEL FLASH STORAGE (64M)
* ICE65L84F L - SiliconBlue FPGA
* PL-8810 - EagleTech Technology USB controller (or variants mc9508jm8 cld 1m61j ctap0946e)
* CR 1220 - Removable 3V Lithium Battery

Thanks
====
Big thanks to Mike Ryan & co. at https://lacklustre.net/projects/ems-flasher/ for 
doing all the heavy lifting to reverse engineer this cart

