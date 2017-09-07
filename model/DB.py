import mysql.connector as connector


class DB(object):

    def __init__(self):
        self.__dsn = {"host": "localhost", "user": "tripuser", "passwd": "W+f@8A6AFPyrUZ-N", "db": "tripmaster"}
        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    try:

        def insert_coordinates(self, lat, lon, date_time):
            self.__init__()
            query = "INSERT INTO gpsdata(latitude, longitude, date_time) VALUES ('{param1}', '{param2}', '{param3}');"
            sqlCommand = query.format(param1=lat, param2=lon, param3=date_time)
            self.__cursor.execute(sqlCommand)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def total_gpsdata_rows(self):
            self.__init__()
            query = "SELECT count(id) FROM tripmaster.gpsdata;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def start_time(self):
            self.__init__()
            query = "select date_time as 'trip_start_time' from tripmaster.gpsdata order by date_time asc limit 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def get_first_gpsdata_id(self, id):
            self.__init__()
            query = "SELECT id FROM tripmaster.gpsdata order by id ASC limit '{param1}', 2;"
            sqlCommand = query.format(param1=id)
            self.__cursor.execute(sqlCommand)
            result = self.__cursor.fetchall()
            # self.__cursor.close()
            return result

        def get_gpsdata_by_id(self, id):
            self.__init__()
            query = "SELECT latitude, longitude FROM tripmaster.gpsdata WHERE id = '{param1}';"
            sqlCommand = query.format(param1=id)
            self.__cursor.execute(sqlCommand)
            result = self.__cursor.fetchall()
            # self.__cursor.close()
            return result

        def get_pref_avg_speed(self):
            self.__init__()
            query = "SELECT avg_speed FROM tripmaster.settings LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def get_ideal_start_time(self):
            self.__init__()
            query = "SELECT ideal_start_time FROM tripmaster.settings LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def update_fix(self, fix):
            self.__init__()
            query = "UPDATE tripmaster.info SET gps_status = '{param1}' WHERE id = '1';"
            sqlCommand = query.format(param1=fix)
            self.__cursor.execute(sqlCommand)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def reset_toggle_trip(self, trip):
            self.__init__()
            if trip == "A":
                query1 = "UPDATE tripmaster.info SET toggle_trip_a_distance = '0' WHERE id = '1';"
                query2 = "DELETE FROM tripmaster.trips WHERE trip = 'A';"
            else:
                query1 = "UPDATE tripmaster.info SET toggle_trip_B_distance = '0' WHERE id = '1';"
                query2 = "DELETE FROM tripmaster.trips WHERE trip = 'B';"
            self.__cursor.execute(query1)
            self.__cursor.execute(query2)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def get_fix(self):
            self.__init__()
            query = "SELECT gps_status FROM tripmaster.info LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def update_cur_speed(self, speed):
            self.__init__()
            query = "UPDATE tripmaster.info SET cur_speed = '{param1}' WHERE id = '1';"
            sqlCommand = query.format(param1=speed)
            self.__cursor.execute(sqlCommand)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def get_cur_speed(self):
            self.__init__()
            query = "SELECT cur_speed FROM tripmaster.info LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def get_total_distance(self):
            self.__init__()
            query = "SELECT total_distance FROM tripmaster.info LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def get_trip_state(self):
            self.__init__()
            query = "SELECT trip_is_active FROM tripmaster.info LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def get_wrong_traject_state(self):
            self.__init__()
            query = "SELECT drove_wrong_current FROM tripmaster.info LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def get_screen_brightness(self):
            self.__init__()
            query = "SELECT screen_brightness FROM tripmaster.settings LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def get_total_distance_wrong(self):
            self.__init__()
            query = "SELECT total_distance_wrong FROM tripmaster.info LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def get_toggle_trip_distance(self, trip):
            self.__init__()
            if trip == "A":
                query = "SELECT toggle_trip_a_distance FROM tripmaster.info LIMIT 1;"
            else:
                query = "SELECT toggle_trip_b_distance FROM tripmaster.info LIMIT 1;"
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            # self.__cursor.close()
            return result[0]

        def update_trip_state(self, state):
            self.__init__()
            query = "UPDATE tripmaster.info SET trip_is_active = '{param1}' WHERE id = '1';"
            sqlCommand = query.format(param1=state)
            self.__cursor.execute(sqlCommand)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def update_wrong_traject_state(self, state):
            self.__init__()
            query = "UPDATE tripmaster.info SET drove_wrong_current = '{param1}' WHERE id = '1';"
            sqlCommand = query.format(param1=state)
            self.__cursor.execute(sqlCommand)
            query2 = "UPDATE tripmaster.info SET drove_wrong_count = drove_wrong_count + 1;" # Set the new count thing
            self.__cursor.execute(query2)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def update_pref_avg_speed(self, new_avg_speed):
            self.__init__()
            query = "UPDATE tripmaster.settings SET avg_speed = '{param1}' WHERE id = '1';"
            sqlCommand = query.format(param1=new_avg_speed)
            self.__cursor.execute(sqlCommand)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def update_ideal_start_time(self, new_start_time):
            self.__init__()
            query = "UPDATE tripmaster.settings SET ideal_start_time = '{param1}' WHERE id = '1';"
            sqlCommand = query.format(param1=new_start_time)
            self.__cursor.execute(sqlCommand)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def update_screen_brightness(self, new_screen_brightness):
            self.__init__()
            query = "UPDATE tripmaster.settings SET screen_brightness = '{param1}' WHERE id = '1';"
            sqlCommand = query.format(param1=new_screen_brightness)
            self.__cursor.execute(sqlCommand)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def reset_database(self):
            self.__init__()
            query1 = "SELECT tripmaster.reset_database();"
            self.__cursor.execute(query1)
            # Need to get a result, since the query won't work if it can't return a result.
            result = self.__cursor.fetchone()
            query2 = "UPDATE tripmaster.info SET total_distance = '0' WHERE id = '1';"
            self.__cursor.execute(query2)
            query3 = "ALTER TABLE tripmaster.gpsdata AUTO_INCREMENT = 1;"
            self.__cursor.execute(query3)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def toggle_trip_state(self, trip, state):
            self.__init__()
            if trip == "A":
                query = "UPDATE tripmaster.info SET toggle_trip_a_state = '{param1}' WHERE id = '1';"
            else:
                query = "UPDATE tripmaster.info SET toggle_trip_b_state = '{param1}' WHERE id = '1';"
            sqlCommand = query.format(param1=state)
            self.__cursor.execute(sqlCommand)
            # Data commit
            self.__connection.commit()
            # self.__cursor.close()

        def __del__(self):
            print("Connections are closed.")
            self.__cursor.close()
            self.__connection.close()
    except:
        raise Exception
