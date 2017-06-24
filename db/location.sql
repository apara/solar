# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: tiny (MySQL 5.5.5-10.0.30-MariaDB-0+deb8u2)
# Database: solar
# Generation Time: 2017-06-24 20:50:59 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table location
# ------------------------------------------------------------

DROP TABLE IF EXISTS `location`;

CREATE TABLE `location` (
  `serial` varchar(64) NOT NULL DEFAULT '',
  `direction` enum('EAST','WEST','SOUTH','NORTH') DEFAULT NULL,
  `room` enum('MASTER BDRM','3RD BDRM','FAMILY','KITCHEN') DEFAULT NULL,
  PRIMARY KEY (`serial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;

INSERT INTO `location` (`serial`, `direction`, `room`)
VALUES
	('414051706011633','EAST','MASTER BDRM'),
	('414051707011020','WEST','MASTER BDRM'),
	('414051707013664','EAST','MASTER BDRM'),
	('414051707014662','EAST','3RD BDRM'),
	('414051707014786','SOUTH','FAMILY'),
	('414051707014925','SOUTH','FAMILY'),
	('414051707015014','EAST','3RD BDRM'),
	('414051707015028','SOUTH','FAMILY'),
	('414051707015080','EAST','MASTER BDRM'),
	('414051707015082','EAST','KITCHEN'),
	('414051707015253','SOUTH','FAMILY'),
	('414051707015260','EAST','MASTER BDRM'),
	('414051708000304','WEST','MASTER BDRM'),
	('414051708000326','WEST','MASTER BDRM'),
	('414051708000342','WEST','MASTER BDRM'),
	('414051708000343','WEST','MASTER BDRM'),
	('414051708000625','EAST','KITCHEN'),
	('414051708000639','EAST','MASTER BDRM'),
	('414051708005176','EAST','KITCHEN'),
	('414051708005888','WEST','MASTER BDRM');

/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
