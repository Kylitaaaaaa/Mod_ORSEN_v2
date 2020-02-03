-- MySQL dump 10.13  Distrib 8.0.17, for macos10.14 (x86_64)
--
-- Host: localhost    Database: orsen_kb
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `extraction_templates`
--

DROP TABLE IF EXISTS `extraction_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `extraction_templates` (
  `idextraction` int(11) NOT NULL AUTO_INCREMENT,
  `relation` varchar(45) NOT NULL,
  `first` varchar(45) NOT NULL,
  `keywords` varchar(45) DEFAULT NULL,
  `second` varchar(45) NOT NULL,
  `third` varchar(45) NOT NULL,
  `keyword_type` int(11) NOT NULL,
  `is_flipped` varchar(45) NOT NULL,
  PRIMARY KEY (`idextraction`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `extraction_templates`
--

LOCK TABLES `extraction_templates` WRITE;
/*!40000 ALTER TABLE `extraction_templates` DISABLE KEYS */;
INSERT INTO `extraction_templates` VALUES (1,'IsA','nsubj','be','attr','',1,'n'),(2,'HasA','nsubj','have','dobj','',1,'n'),(3,'CapableOf','nsubj','aux','ROOT','advmod',0,'n'),(4,'CapableOf','nsubj','','ROOT','advmod',1,'n'),(5,'CapableOf','ROOT','agent','pobj','',0,'y'),(6,'ReceivesAction','nsubjpass','auxpass','ROOT','',0,'n'),(7,'ReceivesAction','ROOT','det','dobj','',0,'y'),(8,'AtLocation','nsubj','go','advmod','',1,'n'),(9,'AtLocation','nsubj','at','pobj','',1,'n'),(10,'AtLocation','nsubj','in','pobj','',1,'n'),(11,'HasProperty','amod','','nsubj','',1,'y'),(12,'HasProperty','nsubj','ROOT','acomp','',0,'n'),(13,'Desires','nsubj','ask','dobj','',1,'n'),(14,'Desires','nsubj','hope','dobj','',1,'n'),(15,'Desires','nsubj','like','dobj','',1,'n'),(16,'Desires','nsubj','want','dobj','',1,'n'),(17,'Desires','nsubj','wish','dobj','',1,'n'),(18,'Desires','nsubj','ask','xcomp','',1,'n'),(19,'Desires','nsubj','hope','xcomp','',1,'n'),(20,'Desires','nsubj','like','xcomp','',1,'n'),(21,'Desires','nsubj','want','xcomp','',1,'n'),(22,'Desires','nsubj','wish','xcomp','',1,'n'),(23,'UsedFor','dobj','to','xcomp','',1,'n'),(24,'UsedFor','dobj','for','pcomp','',1,'n'),(25,'UsedFor','nsubjpass','to','xcomp','',1,'n'),(26,'UsedFor','nsubjpass','for','pcomp','',1,'n'),(27,'CreatedBy','dobj','by','pcomp','dobj',1,'y'),(28,'CreatedBy','dobj','through','pcomp','dobj',1,'y'),(29,'ReceivesAction','ROOT','','dobj','',1,'y'),(30,'HasProperty','amod','','dobj','',1,'y'),(31,'HasProperty','amod','','pobj','',1,'y'),(32,'UsedFor','nsubjpass','use','pobj','',1,'n'),(33,'HasProperty','amod','','attr','',1,'y'),(34,'HasA','pobj','have','dobj','',1,'n'),(35,'CapableOf','nsubj','aux','advcl','',0,'n'),(36,'Desires','nsubj','desire','dobj','',1,'n'),(37,'Desires','nsubj','desire','xcomp','',1,'n');
/*!40000 ALTER TABLE `extraction_templates` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-22  0:22:30
