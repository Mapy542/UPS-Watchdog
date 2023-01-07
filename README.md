# UPS Watchdog
 Ping checking script to power down a server given a loss of local internet service. It's not elegant, but its dirt simple.

 ## Purpose
 Cheap battery backup un-interruptable power supplies can be had on amazon for $100. The purpose of the device is to maintain mains voltage to a computer during a blackout so the computer can survive a temporary loss of power, or safely power down for an extended power outage. The device is intended to be connected to a Windows PC via usb, and then complimentary software powers down the computer on the UPS's command. \
 The software only works on WINDOWS though. Linux isn't compatible directly. Rather than attempt to emulate the software or fine another one, I made my own that checks for a local internet connection. This will not work if the router or modem is also connected to the UPS. \

 ## Use
The program is intended to be used as a systemd service that is always running in the background. It will ping against a lan device that is ideally always active but not UPS protected.\
If the lan ping to a designated device, like the router, fails, the program waits for a small amount of time, and then checks again.\
If the lan ping fails 5 pings over at least a minute and a half, then the program sends a shutdown command.\

The program is based around a proportion of time of the UPS max runtime. If the UPS has a small or large runtime, the program will scale to check as least often as possible while still having time to safely shutdown.

