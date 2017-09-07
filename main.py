import os
import serial
from datetime import datetime, timedelta
import time
from model.Formulas import Formulas
from model.Functions import Functions
from model.GPSParser import GPSParser
from model.DB import DB


#########################################
# This is the main code to setup the
# serial connection with the GPS module.
# it needs to be OR runt as root OR as
# pi with all the root rights.
#########################################
port = "/dev/serial0"
baudrate = 9600
timeout = 1
ser = serial.Serial(port, baudrate, timeout=timeout)


############################################################
# These are all the global variables to be used.
# All defined and set to zero or their standard
# 'Null' value.
############################################################
lat = 0.0
lon = 0.0
speed = 0.0
fix = "No fix"  # Gives no fix parsed.
timestamp = "010117 000000.000"


############################################################
# Timer functions
############################################################
# This conatains the variables for the timer,
# It will only start a script when there is a GPS fix and
# and it will execute the script once every 5 minutes.
############################################################
update_interval = timedelta(minutes=10)
last_update = datetime.min  # 1970-1-1 avoids having to check for None while still ensuring update @ first fix


data = None
db = DB()

while True:

    try:
        # Get the data from the serial monitor.
        data = ser.readline().decode().split(',')
        print(data)
        if data[0] == "$GPGGA" or data[0] == "$GPVTG" or data[0] == "$GPRMC":

            # Set the data to correct data to work with
            # Create a parse object to parse all the data easily
            parse = GPSParser(data)

            if Formulas.chksum_nmea(data[0]):

                # Start the data check
                done = False
                if data[0] == "$GPGGA":
                    lat = parse.lat
                    lon = parse.lon
                    fix = parse.fix
                elif data[0] == "$GPRMC":
                    timestamp = parse.timestamp
                elif data[0] == "$GPVTG":
                    speed = parse.speed
                    done = True

                if done is True:
                    print("All data is parsed")

                    ############################################################
                    # In here, we update the current time of the system.
                    # As the system does never have an internet connection in the
                    # fields, we need to set the time received from the GPS.
                    ###################################s#########################
                    if fix == "GPS fix":
                        # print("FIX!!!")
                        # Set the current timezone to europe/brussels
                        os.environ['TZ'] = 'Europe/Brussels'
                        time.tzset()
                        # Fix the timezone.
                        fixtime = datetime.now()
                        if timestamp != "":
                            if fixtime and fixtime > last_update + update_interval:
                                print("A time update was performed.")
                                stamp = datetime.strptime(timestamp, "%d%m%y %H%M%S.000").now().replace(microsecond=0)
                                print(stamp)
                                os.system("sudo timedatectl set-time \"" + str(stamp) + "\"")

                                # Set the current timezone to europe/brussels
                                os.environ['TZ'] = 'Europe/Brussels'
                                # Fix the timezone.
                                time.tzset()
                                # Give a new last_update for the time
                                last_update = datetime.now()

                    # Insert the fix into the database
                    db.update_fix(fix)

                    # Insert the current speed into the database
                    db.update_cur_speed(speed)

                    if db.get_trip_state() == 1:
                        if lat != "" and lon != "":
                            # The prints are for the debugging, they won't show up in the program itself.
                            # print("Tijd momenteel: {}\nLatitude: {}\nLongitude: {}\nSnelheid: {} km/u"
                            #       .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lat, lon, speed))
                            # print("##################################################")
                            # print("Voltage:%5.2fV" % Functions.read_ups_voltage())
                            # print("Battery:%5i%%" % Functions.read_ups_capacity())
                            # print("")

                            # Check whether the speed is high enough (+5km/h) and not way too high (+160 km/h)
                            if 5.0 < float(speed) < 160:
                                db.insert_coordinates(lat, lon, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                                ############################################################
                                # Check if the UPS battery is almost empty, if so,
                                # shutdown the system, to prevent damage on the SD card.
                                ############################################################
                                if Functions.read_ups_capacity() < 5:
                                    print("The power voltage of the battery is too low"
                                          "system is powering off to prevent software damage.")
                                    os.system('sudo shutdown now')

                    # ser.flushInput()
                    # ser.flushOutput()
                    done = False
                else:
                    print("Still parsing")
            else:
                print("Nmea was incorrect!")

    ############################################################
    # The error handling
    ############################################################
    except serial.serialutil.SerialException:
        # ser.flushInput()
        # ser.flushOutput()
        ser.close()
        ser = serial.Serial(port, baudrate, timeout=timeout)
        continue
    except BlockingIOError:
        # print("Blocking I/O error, continuing...")
        continue
    except TypeError:
        # print("Type error, continuing...")
        continue
    except IndexError:
        # print("I ran too far with the list :/")
        continue
    except ValueError:
        # print("Could not convert string to float...")
        continue
    except IOError:
        continue
    except KeyboardInterrupt:
        # Reset everything
        # ser.flushInput()
        # ser.flushOutput()
        ser.close()
        # ser = serial.Serial(port, baudrate, timeout=timeout)
        print("\nProgram stopped.")
        exit()
