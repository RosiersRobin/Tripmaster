import math
import datetime
import re

from model.DB import DB


class Formulas:

    # 3959  # radius of the great circle in miles...some algorithms use 3956
    # 6371  # radius in kilometers...some algorithms use 6367
    # 3959 * 5280  # radius in feet
    # 6371 * 1000  # radius in meters
    @staticmethod
    def calculate_distance(origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d

    @staticmethod
    def avg_speed():
        # Speed = Distance ÷ Time
        cur_time = datetime.datetime.now().replace(microsecond=0)
        db_time_record = datetime.datetime.strptime(DB().start_time(), "%Y-%m-%d %H:%M:%S")
        elapsed = cur_time - db_time_record
        seconds = elapsed.total_seconds()
        # print(str(time_diff).split(":"))
        total_distance = DB().get_total_distance()
        result = (total_distance / seconds)
        return round(result, 2)

    @staticmethod
    def chksum_nmea(sentence):

        # This is a string, will need to convert it to hex for
        # proper comparsion below
        cksum = sentence[len(sentence) - 2:]

        # String slicing: Grabs all the characters
        # between '$' and '*' and nukes any lingering
        # newline or CRLF
        chksumdata = re.sub("(\n|\r\n)", "", sentence[sentence.find("$") + 1:sentence.find("*")])

        # Initializing our first XOR value
        csum = 0

        # For each char in chksumdata, XOR against the previous
        # XOR'd char.  The final XOR of the last char will be our
        # checksum to verify against the checksum we sliced off
        # the NMEA sentence

        for c in chksumdata:
            # XOR'ing value of csum against the next char in line
            # and storing the new XOR value in csum
            csum ^= ord(c)

        # Do we have a validated sentence?
        if hex(csum) == hex(int(cksum, 16)):
            return True

        return False
