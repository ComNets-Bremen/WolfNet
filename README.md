WolfNet - A simple LoRa based network for deterrents
====================================================

The [mAInZaun-Project](https://intelligenter-herdenschutz.de/) is aiming on
extending existing fence by using adaptive deterrents to scare away predators.

This part implements a simple protocol for the sensors and actuators: How can
the deterrents be activated wirelessly if a predator is detected?


What is in here?
----------------

This directory contains basically everything regarding the LoRa communication
and actuator part of the mAInZaun project.

Looking for the packet format? Check the file [packets.md](packets.md) in this directory.


What is in the subdirectories?
==============================

controlbox
----------

The idea is to have a box for the management of the complete (LoRa) system. It
should have a touchscreen and basic interface for changing parameters like
beaconing intervals or reading out the battery state.

Datasheets
----------

Collection of all relevant datasheets

Schematic
---------

Contains the schematics as KICad files -- currently mainly the ones for the
actuator boxes.

testing\_firmware
----------------

Simple firmware for testing the newly build boxes.

tools
-----

General tools which might be handy for debugging

wolfnet
-------

The firmware itself which makes the sensors and the actuators communicate. It
is a Visual Studio Code project and using the Pymakr-plugin.

Issues
======

The known issues can be found in the [github issue tracker](https://github.com/ComNets-Bremen/WolfNet/issues)

License
=======

WolfNet
-------

The license of the code can be found in the [LICENSE](LICENSE) file.

3rd Party
---------

- The used AES library is licensed using the MIT license and available here: https://github.com/iyassou/mpyaes
- The driver sx127x.py for the sx127x LoRa transceiver is licensed under the Apache 2.0 license and available here: https://github.com/lemariva/uPyLoRaWAN

Authors
=======

- Jens Dede, ComNets University of Bremen, jd@comnets.uni-bremen.de
