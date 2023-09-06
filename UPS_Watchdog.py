#!/usr/bin/env python3
import os, time

CheckIP = "10.0.0.1"  # ip to check for valid connection against. A router is the best option, but another server could work.
UPSRuntime = 7 * 60  # runtime of UPS in seconds.
SudoPass = "password"  # sudo password for shutdown command. Better yet, make shutdown a non-sudo command.
LogPath = "/home/pi/UPS_Watchdog.log"  # path to log file.


def ping(ip):
    result = os.system("ping -c 1 " + str(ip))  # ping the ip
    if result == 0:  # if ping is successful
        return True
    return False  # if ping fails error result returns something like 256, so this will catch that.


def Shutdown(password):
    os.system(
        "echo " + str(SudoPass) + " | sudo -S shutdown -P +1"
    )  # shutdown command with password
    # full system power off on ubuntu as defined by "-P" 1 minute after command is issued.
    # no full system power puts ubuntu into "halt" state, unable to be restarted by Wake on LAN.


while True:
    if ping(CheckIP):
        time.sleep(
            UPSRuntime / 4
        )  # internet connection valid check in 1/4 of the ups runtime
    else:
        # print('Ping Failure. Checking again in ' + str(UPSRuntime / 6) + ' seconds.')
        try:
            with open("UPS_Watchdog.log", "a") as log:
                log.write(
                    "Initial Connection loss detected at: " + str(time.ctime()) + ".\n"
                )
                log.write(
                    "     Checking again in " + str(UPSRuntime / 6) + " seconds.\n"
                )
                log.close()
        except:
            print("Error writing to log file.")

        time.sleep(UPSRuntime / 6)

        for i in range(0, 5):  # check 5 times for a valid connection
            if not ping(CheckIP):
                print("Failure")
                Shutdown(SudoPass)
                try:
                    with open("UPS_Watchdog.log", "a") as log:
                        log.write(
                            "Failed multiple check connection"
                            + str(time.ctime())
                            + ".\n"
                        )
                        log.write("Shutdown at " + str(time.ctime()) + ".\n")
                        log.close()
                except:
                    print("Error writing to log file.")
                exit()
            else:
                print("Success")
                try:
                    with open("UPS_Watchdog.log", "a") as log:
                        log.write(
                            "Successful multiple check connection"
                            + str(time.ctime())
                            + ".\n"
                        )
                        log.close()
                except:
                    print("Error writing to log file.")
                time.sleep(UPSRuntime / 6)

        try:
            with open("UPS_Watchdog.log", "a") as log:
                log.write("Connection Restored at " + str(time.ctime()) + ".\n")
                log.close()
        except:
            print("Error writing to log file.")
