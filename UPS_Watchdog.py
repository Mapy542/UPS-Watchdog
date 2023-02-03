#!/usr/bin/env python3
import os, time

checkip = '10.0.0.1' #ip to check for valid connection against. A router is the best option, but another server could work.
UPS_runtime = 7*60 #runtime of UPS in seconds.
sudopass = 'password' #sudo password for shutdown command. Better yet, make shutdown a non-sudo command.
logpath = '/home/pi/UPS_Watchdog.log' #path to log file.

def ping(ip):
    result = os.system('ping -c 1 ' + str(ip)) #ping the ip
    if result == 0: #if ping is successful
        return True
    else:
        return False #if ping fails error result returns something like 256, so this will catch that.

while(True):
    if ping(checkip):
        time.sleep(UPS_runtime/4) #internet connection valid check in 1/4 of the ups runtime
    else:
        print('Ping Failure. Checking again in ' + str(UPS_runtime / 6) + ' seconds.')
        try:
            with open('UPS_Watchdog.log', 'a') as log:
                log.write('Connection loss detected at: ' + str(time.ctime()) + '.\n')
                log.close()
        except:
            print('Error writing to log file.')
        time.sleep(UPS_runtime / 6)
        multickeck = False
        for i in range(0,5): #check 5 times for a valid connection
            if not ping(checkip):
                print('Failure')
                multicheck = False
                break
            else:
                print('Sucess')
                multicheck = True
            time.sleep(15)
        if multicheck == False:
            os.system('echo '+ str(sudopass) + ' | sudo -S shutdown')
            try:
                with open('UPS_Watchdog.log', 'a') as log:
                    log.write('Shutdown at ' + str(time.ctime()) + '.\n')
                    log.close()
            except:
                print('Error writing to log file.')
            exit()


