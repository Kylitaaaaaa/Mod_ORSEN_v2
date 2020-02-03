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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `iduser` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `code` varchar(45) NOT NULL,
  PRIMARY KEY (`iduser`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'celina','dog'),(2,'admin','admin'),(3,'jilyan','munch'),(4,'casey','hateyou'),(5,'rein','665'),(6,'hendrix','noodle'),(7,'renz','cool'),(8,'kaylee','loving'),(9,'daed','1905'),(11,'alijah','alijah333'),(12,'gffghguktuo0','potatogirl'),(13,'charmaine','lovelypotato'),(14,'hannahthekittycat','kittynani1233'),(15,'julia','blue'),(16,'diego','phoenix810'),(17,'andrea','picnic'),(18,'ryan','evans'),(19,'sydney','mermaid'),(20,'audrey','password'),(21,'enrich','sehn'),(22,'hi','heterogeneous'),(23,'yannie','bangtan'),(24,'tin','berj'),(25,'pepepr','harry'),(26,'pepper','harry'),(27,'pepper','cookie'),(28,'wisner','xd'),(29,'wisner','xd'),(30,'wisner','xd'),(31,'wisner','xd'),(32,'wisner','xd'),(33,'wisner','shhh'),(34,'Kyle','pepper'),(35,'pepperoni','1'),(36,'kyle','pepper'),(37,'kyle','pepper'),(38,'pepper','pepper'),(39,'pepper','pepper'),(40,'pepper','pepper'),(41,'kyle','pepper'),(42,'Sticko101','strawberry'),(43,'Sticko101','strawberry'),(44,'Sticko101','strawberry'),(45,'Sticko101','strawberry'),(46,'Sticko101','strawberry'),(47,'Sticko101','strawberry'),(48,'jamescerbito30','09236163739'),(49,'jim david','09shadabeng'),(50,'abeng','09192918195'),(51,'abeng2','1234'),(52,'enteng','6874457889268'),(53,'harvy','682455456');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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
