CREATE DATABASE  IF NOT EXISTS `tripmaster` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `tripmaster`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: tripmaster
-- ------------------------------------------------------
-- Server version	5.5.55-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `draw_points`
--

DROP TABLE IF EXISTS `draw_points`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `draw_points` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gpsdata_id` int(11) DEFAULT NULL,
  `is_important_point` bit(1) DEFAULT b'0',
  `is_letter_point` bit(1) DEFAULT b'0',
  `is_number_point` bit(1) DEFAULT b'0',
  `is_street_point` bit(1) DEFAULT b'0',
  `is_tc_point` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`),
  KEY `fk_draw_points_gpsdata_idx` (`gpsdata_id`),
  CONSTRAINT `fk_draw_points_gpsdata` FOREIGN KEY (`gpsdata_id`) REFERENCES `gpsdata` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `drove_wrong`
--

DROP TABLE IF EXISTS `drove_wrong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drove_wrong` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gpsdata_id` int(11) DEFAULT NULL,
  `drove_wrong_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_droveWrong_gpsdata1_idx` (`gpsdata_id`),
  CONSTRAINT `fk_droveWrong_gpsdata1` FOREIGN KEY (`gpsdata_id`) REFERENCES `gpsdata` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=787 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gpsdata`
--

DROP TABLE IF EXISTS `gpsdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gpsdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `latitude` float(10,6) NOT NULL,
  `longitude` float(10,6) NOT NULL,
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1289 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tripmaster`.`gpsdata_AFTER_INSERT` AFTER INSERT ON `gpsdata` FOR EACH ROW
BEGIN

declare lat1 float;
declare long1 float;
declare lat2 float;
declare long2 float;

declare lat1_wrong float;
declare long1_wrong float;
declare lat2_wrong float;
declare long2_wrong float;

declare lat1_trip_a float;
declare long1_trip_a float;
declare lat2_trip_a float;
declare long2_trip_a float;

declare lat1_trip_b float;
declare long1_trip_b float;
declare lat2_trip_b float;
declare long2_trip_b float;

declare calc_dist float;
declare id_exists Boolean;

-- Check if the table with the total distance isn't empty
SELECT 1 INTO @id_exists FROM tripmaster.info;

-- find the last inserted ID of the tripmaster to start counting from there
SELECT latitude, longitude FROM tripmaster.gpsdata ORDER BY id DESC LIMIT 1, 1 INTO lat1, long1;

-- Get the new values that are recently inserted.
SELECT latitude, longitude FROM tripmaster.gpsdata where id = NEW.id ORDER BY id DESC LIMIT 1 INTO lat2, long2;


SELECT tripmaster.calculate_distance_between_points(lat1, long1, lat2, long2) INTO calc_dist;

if(SELECT drove_wrong_current FROM tripmaster.info WHERE info.id = 1) = 1
then
	IF (SELECT count(*) FROM drove_wrong) >= 2 THEN
    
		SET lat1_wrong = (SELECT latitude FROM gpsdata ORDER BY id DESC limit 0,1);
		SET long1_wrong = (SELECT longitude FROM gpsdata ORDER BY id DESC limit 0,1);
		SET lat2_wrong = (SELECT latitude FROM gpsdata ORDER BY id DESC Limit 1,1);
        SET long2_wrong = (SELECT longitude FROM gpsdata ORDER BY id DESC limit 1,1);
        
        UPDATE tripmaster.info SET total_distance_wrong = total_distance_wrong + (SELECT tripmaster.calculate_distance_between_points(lat1_wrong, long1_wrong, lat2_wrong, long2_wrong)*2) WHERE info.id = 1;
        
    END IF;
    
	INSERT INTO drove_wrong (gpsdata_id, drove_wrong_count) VALUES (NEW.id,  (SELECT drove_wrong_count FROM tripmaster.info) + 1);

end if;


if(SELECT toggle_trip_a_state FROM tripmaster.info where info.id = 1) = 1
then

	IF (SELECT count(*) FROM trips where trip = "A") >= 2 THEN
		
        SET lat1_trip_a = (SELECT latitude FROM gpsdata ORDER BY id DESC limit 0,1);
		SET long1_trip_a = (SELECT longitude FROM gpsdata ORDER BY id DESC limit 0,1);
		SET lat2_trip_a = (SELECT latitude FROM gpsdata ORDER BY id DESC Limit 1,1);
		SET long2_trip_a = (SELECT longitude FROM gpsdata ORDER BY id DESC limit 1,1);
        
        UPDATE tripmaster.info SET toggle_trip_a_distance = toggle_trip_a_distance + (SELECT tripmaster.calculate_distance_between_points(lat1_trip_a, long1_trip_a, lat2_trip_a, long2_trip_a)) WHERE info.id = 1;
        
    end if;
    
    INSERT INTO trips(trip, gpsdata_id) VALUES ("A", NEW.id);

end if;


if(SELECT toggle_trip_b_state FROM tripmaster.info where info.id = 1) = 1
then

	IF (SELECT count(*) FROM trips where trip = "B") >= 2 THEN
		
        SET lat1_trip_b = (SELECT latitude FROM gpsdata ORDER BY id DESC limit 0,1);
		SET long1_trip_b = (SELECT longitude FROM gpsdata ORDER BY id DESC limit 0,1);
		SET lat2_trip_b = (SELECT latitude FROM gpsdata ORDER BY id DESC Limit 1,1);
		SET long2_trip_b = (SELECT longitude FROM gpsdata ORDER BY id DESC limit 1,1);
        
        UPDATE tripmaster.info SET toggle_trip_b_distance = toggle_trip_b_distance + (SELECT tripmaster.calculate_distance_between_points(lat1_trip_b, long1_trip_b, lat2_trip_b, long2_trip_b)) WHERE info.id = 1;
        
    end if;
    
    INSERT INTO trips(trip, gpsdata_id) VALUES ("B", NEW.id);

end if;


if @id_exists
then
	if calc_dist IS NOT NULL
    then
		update tripmaster.info set total_distance = total_distance + calc_dist where info.id = 1;
	end if;
else
	insert into tripmaster.info (id, settings_id, total_distance) values (1, 1, calc_dist);
end if;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `icons`
--

DROP TABLE IF EXISTS `icons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `icons` (
  `id` int(11) NOT NULL,
  `icon_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `info`
--

DROP TABLE IF EXISTS `info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `settings_id` int(11) DEFAULT NULL,
  `cur_speed` float(100,3) DEFAULT '0.000',
  `total_distance` float(100,6) DEFAULT '0.000000',
  `gps_status` varchar(45) DEFAULT 'No fix',
  `trip_is_active` tinyint(4) DEFAULT '0',
  `total_distance_wrong` float(100,6) DEFAULT '0.000000',
  `drove_wrong_current` tinyint(4) DEFAULT '0',
  `drove_wrong_count` int(11) DEFAULT '0',
  `toggle_trip_a_distance` float(100,6) DEFAULT '0.000000',
  `toggle_trip_a_state` tinyint(4) DEFAULT '0',
  `toggle_trip_b_distance` float(10,6) DEFAULT '0.000000',
  `toggle_trip_b_state` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_distance_settings1_idx` (`settings_id`),
  CONSTRAINT `fk_distance_settings1` FOREIGN KEY (`settings_id`) REFERENCES `settings` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `avg_speed` int(11) DEFAULT NULL,
  `ideal_start_time` time DEFAULT NULL,
  `screen_brightness` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trip` enum('A','B') DEFAULT NULL,
  `gpsdata_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tripA_gpsdata1_idx` (`gpsdata_id`),
  CONSTRAINT `fk_trips_gpsdata1` FOREIGN KEY (`gpsdata_id`) REFERENCES `gpsdata` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'tripmaster'
--

--
-- Dumping routines for database 'tripmaster'
--
/*!50003 DROP FUNCTION IF EXISTS `calculate_distance_between_points` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `calculate_distance_between_points`(
lat1 float,
lon1 float,
lat2 float,
lon2 float
) RETURNS float
BEGIN

-- Earth radius
DECLARE radius INT;
DECLARE dlat FLOAT;
DECLARE dlon FLOAT;
DECLARE a FLOAT;
DECLARE c FLOAT;
DECLARE d FLOAT;


SET radius = 6371; -- km
SET dlat = RADIANS(lat2 - lat1);
SET dlon = RADIANS(lon2 - lon1);
SET a = SIN(dlat / 2) * SIN(dlat / 2) + COS(RADIANS(lat1)) * COS(RADIANS(lat2)) * SIN(dlon / 2) * SIN(dlon / 2);
SET c = 2 * ATAN2(SQRT(a), SQRT(1 - a));
SET d = radius * c;

-- In meter
RETURN d;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `reset_database` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `reset_database`() RETURNS int(11)
BEGIN

-- Delete all the trips
DELETE FROM tripmaster.trips;

-- Now, to start with, purge the drove_wrong table
DELETE FROM tripmaster.drove_wrong;

-- First we remove all the GPS data.
DELETE FROM tripmaster.gpsdata;

-- Make all the info back to zero
UPDATE `tripmaster`.`info` SET `cur_speed`='0', `total_distance`='0', `gps_status`='No fix', `total_distance_wrong`='0', `drove_wrong_current`='0', `drove_wrong_count`='0', `trip_is_active`='0' WHERE `id`='1';

-- Put the settings back to zero
UPDATE `tripmaster`.`settings` SET `ideal_start_time`='00:00:00', `screen_brightness`='100' WHERE `id`='1';

RETURN 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-19 21:26:12
