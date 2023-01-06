#!/usr/bin/env python3
import os, time

checkip = '10.0.0.1' #ip to check for valid connection against. router is the best option.
UPS_runtime = 7*60 #runtime of UPS in seconds.
sudopass = 'password' #sudo password for shutdown command.
logpath = '/home/pi/UPS_Watchdog.log' #path to log file.

def ping(ip):
    result = os.system('ping -c 1 ' + str(ip))
    if result == 0:
        return True
    else:
        return False

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
        for i in range(0,5):
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


