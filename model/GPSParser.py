class GPSParser:
    def __init__(self, data):
        self.__data = data

    @property
    def lat(self):
        lat = self.__data[(self.__data.index("$GPGGA") + 2)]
        # lat = self.__data[2]
        return lat

    @property
    def lon(self):
        lon = self.__data[(self.__data.index("$GPGGA") + 4)]
        # lon = self.__data[4]
        return lon

    @property
    def speed(self):
        try:
            cur_speed = self.__data[(self.__data.index("$GPVTG") + 7)]
            # cur_speed = self.__data[113]
            return cur_speed
        except:
            return ""

    @property
    def sats(self):
        sats = self.__data[(self.__data.index("$GPGGA") + 7)]
        # sats = self.__data[7]
        return sats

    @property
    def fix(self):
        fix = self.__data[(self.__data.index("$GPGGA") + 6)]
        # fix = self.__data[6]
        return {
            '0': "No fix",
            '1': "GPS fix",
            '2': "Dif. GPS fix"
        }.get(fix, "No fix")

    @property
    def timestamp(self):
        try:
            cur_time = self.__data[(self.__data.index("$GPRMC") + 1)]
            cur_date = self.__data[(self.__data.index("$GPRMC") + 9)]
            timestamp = cur_date + " " + cur_time
            # sats = self.__data[7]
            return timestamp
        except:
            return ""
