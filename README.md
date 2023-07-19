WolfNet -- A simple LoRa based network for deterrents
=====================================================

The [mAInZaun-Project](https://intelligenter-herdenschutz.de/) is aiming on
extending existing fence by using adaptive deterrents to scare away predators.

This part implements a simple protocol for the sensors and actuators: How can
the deterrents be activated wirelessly if a predator is detected?


What is in here?
----------------

This directory contains basically everything regarding the LoRa communication
and actuator part of the mAInZaun project.


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


Authors
-------

- Jens Dede, ComNets University of Bremen, jd@comnets.uni-bremen.de
