-- MySQL dump 10.13  Distrib 5.6.36, for Linux (x86_64)
--
-- Host: localhost    Database: ops_deploy
-- ------------------------------------------------------
-- Server version	5.6.36

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
-- Table structure for table `project_config`
--

DROP TABLE IF EXISTS `project_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_config` (
  `project_name` varchar(64) NOT NULL,
  `config1` text,
  `config2` text,
  `config3` text,
  `config4` text,
  `config5` text,
  `config6` text,
  `config7` text,
  `config8` text,
  `config9` text,
  `config10` text,
  PRIMARY KEY (`project_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projectinfo`
--

DROP TABLE IF EXISTS `projectinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projectinfo` (
  `project_name` varchar(64) CHARACTER SET latin1 NOT NULL,
  `project` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `environment` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `branch` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `type` varchar(10) CHARACTER SET latin1 DEFAULT NULL,
  `git` varchar(1024) CHARACTER SET latin1 DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `make` text CHARACTER SET latin1,
  `istag` varchar(10) CHARACTER SET latin1 DEFAULT NULL,
  `isnginx` varchar(10) CHARACTER SET latin1 DEFAULT NULL,
  `business` varchar(40) DEFAULT NULL,
  `ischeck` varchar(10) CHARACTER SET latin1 DEFAULT NULL,
  `checkurl` varchar(300) CHARACTER SET latin1 DEFAULT NULL,
  `statuscode` varchar(8) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`project_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `serverinfo`
--

DROP TABLE IF EXISTS `serverinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serverinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `hostname` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `ip` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable1` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable2` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable3` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable4` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable5` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable6` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable7` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable8` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `variable9` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_serverinfo_project_name` (`project_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2177 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `updatelog`
--

DROP TABLE IF EXISTS `updatelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `updatelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskid` varchar(64) DEFAULT NULL,
  `project_name` varchar(64) DEFAULT NULL,
  `host` varchar(2000) DEFAULT NULL,
  `tag` varchar(64) DEFAULT NULL,
  `rtime` varchar(32) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `loginfo` mediumtext,
  PRIMARY KEY (`id`),
  KEY `ix_updatelog_taskid` (`taskid`)
) ENGINE=InnoDB AUTO_INCREMENT=98158 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `updateoperation`
--

DROP TABLE IF EXISTS `updateoperation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `updateoperation` (
  `taskid` varchar(64) CHARACTER SET latin1 NOT NULL,
  `project_name` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `hostlist` varchar(2000) CHARACTER SET latin1 DEFAULT NULL,
  `tag` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `rtime` varchar(32) CHARACTER SET latin1 DEFAULT NULL,
  `operation` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `loginfo` varchar(6400) CHARACTER SET latin1 DEFAULT NULL,
  `user` varchar(50) NOT NULL,
  PRIMARY KEY (`taskid`),
  KEY `ix_updateoperation_taskid` (`taskid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `username` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `_password` varchar(128) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `ix_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userservicegroup`
--

DROP TABLE IF EXISTS `userservicegroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userservicegroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `servicegroup` varchar(64) CHARACTER SET latin1 DEFAULT NULL,
  `permissions` varchar(64) NOT NULL DEFAULT 'online',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=431 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workorder`
--

DROP TABLE IF EXISTS `workorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group` varchar(64) DEFAULT NULL,
  `project` varchar(64) DEFAULT NULL,
  `applicant` varchar(64) DEFAULT NULL,
  `applicationtime` varchar(64) DEFAULT NULL,
  `status` varchar(64) DEFAULT NULL,
  `executor` varchar(64) DEFAULT NULL,
  `completiontime` varchar(64) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2156 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-06 16:24:11
