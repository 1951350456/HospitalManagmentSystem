-- MySQL dump 10.13  Distrib 8.0.35, for Win64 (x86_64)
--
-- Host: localhost    Database: HospitalManagement
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
REPLACE INTO `users` VALUES (3,'zyf','5fd8ecec630074686df4be84705fc8c1f3f97b9ad35ab0db9dbe8656b7be5f0a');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `入库记录`
--

DROP TABLE IF EXISTS `入库记录`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `入库记录` (
  `入库ID` int NOT NULL AUTO_INCREMENT,
  `药品ID` int NOT NULL,
  `数量` int NOT NULL,
  `入库时间` datetime DEFAULT CURRENT_TIMESTAMP,
  `操作员` varchar(50) DEFAULT NULL,
  `供应商` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`入库ID`),
  KEY `药品ID` (`药品ID`),
  CONSTRAINT `入库记录_ibfk_1` FOREIGN KEY (`药品ID`) REFERENCES `药品信息` (`药品ID`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `入库记录`
--

LOCK TABLES `入库记录` WRITE;
/*!40000 ALTER TABLE `入库记录` DISABLE KEYS */;
REPLACE INTO `入库记录` VALUES (8,10,100,'2025-04-01 10:00:00','库管员A','华北制药'),(9,11,150,'2025-04-05 14:30:00','库管员B','上海信谊'),(10,12,50,'2025-04-10 09:15:00','库管员A','阿斯利康'),(11,13,30,'2025-04-15 11:20:00','库管员C','强生制药'),(12,14,80,'2025-04-20 16:45:00','库管员B','养生堂'),(13,10,50,'2025-05-25 13:10:00','库管员A','广州白云山');
/*!40000 ALTER TABLE `入库记录` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `出库_科室`
--

DROP TABLE IF EXISTS `出库_科室`;
/*!50001 DROP VIEW IF EXISTS `出库_科室`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `出库_科室` AS SELECT 
 1 AS `科室ID`,
 1 AS `科室名称`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `出库记录`
--

DROP TABLE IF EXISTS `出库记录`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `出库记录` (
  `出库ID` int NOT NULL AUTO_INCREMENT,
  `药品ID` int NOT NULL,
  `数量` int NOT NULL,
  `出库时间` datetime DEFAULT CURRENT_TIMESTAMP,
  `操作员` varchar(50) DEFAULT NULL,
  `领用科室` int DEFAULT NULL,
  PRIMARY KEY (`出库ID`),
  KEY `药品ID` (`药品ID`),
  KEY `fk_领用科室` (`领用科室`),
  CONSTRAINT `fk_领用科室` FOREIGN KEY (`领用科室`) REFERENCES `科室` (`科室ID`),
  CONSTRAINT `出库记录_ibfk_1` FOREIGN KEY (`药品ID`) REFERENCES `药品信息` (`药品ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `出库记录`
--

LOCK TABLES `出库记录` WRITE;
/*!40000 ALTER TABLE `出库记录` DISABLE KEYS */;
REPLACE INTO `出库记录` VALUES (1,10,20,'2025-05-05 10:30:00','库管员B',2),(2,11,30,'2025-05-08 14:00:00','库管员A',3),(3,12,15,'2025-05-12 09:45:00','库管员C',4),(4,13,25,'2025-05-18 11:20:00','库管员B',5),(5,14,10,'2025-05-22 16:10:00','库管员A',6),(6,13,30,'2025-06-06 00:00:00','zyf',5);
/*!40000 ALTER TABLE `出库记录` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `医生`
--

DROP TABLE IF EXISTS `医生`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `医生` (
  `医生ID` int NOT NULL AUTO_INCREMENT,
  `姓名` varchar(50) NOT NULL,
  `性别` char(1) DEFAULT NULL,
  `职称` varchar(50) DEFAULT NULL,
  `所属科室ID` int DEFAULT NULL,
  `联系电话` varchar(20) DEFAULT NULL,
  `入职日期` date DEFAULT NULL,
  PRIMARY KEY (`医生ID`),
  KEY `所属科室ID` (`所属科室ID`),
  CONSTRAINT `医生_ibfk_1` FOREIGN KEY (`所属科室ID`) REFERENCES `科室` (`科室ID`),
  CONSTRAINT `CK_医生性别` CHECK ((`性别` in (_utf8mb4'男',_utf8mb4'女',_utf8mb4'未知')))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `医生`
--

LOCK TABLES `医生` WRITE;
/*!40000 ALTER TABLE `医生` DISABLE KEYS */;
REPLACE INTO `医生` VALUES (2,'张明远','男','主任医师',2,'13800138001','2010-05-20'),(3,'李思雨','女','副主任医师',3,'13900139002','2015-08-15'),(4,'王建国','男','主治医师',4,'13700137003','2018-03-10'),(5,'赵晓雯','女','主任医师',5,'13600136004','2008-11-30'),(6,'刘振华','男','副主任医师',6,'13500135005','2016-07-22');
/*!40000 ALTER TABLE `医生` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `处方`
--

DROP TABLE IF EXISTS `处方`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `处方` (
  `处方ID` int NOT NULL AUTO_INCREMENT,
  `病人ID` int NOT NULL,
  `医生ID` int NOT NULL,
  `开具时间` datetime DEFAULT CURRENT_TIMESTAMP,
  `诊断结果` text,
  PRIMARY KEY (`处方ID`),
  KEY `病人ID` (`病人ID`),
  KEY `医生ID` (`医生ID`),
  CONSTRAINT `处方_ibfk_1` FOREIGN KEY (`病人ID`) REFERENCES `病人` (`病人ID`),
  CONSTRAINT `处方_ibfk_2` FOREIGN KEY (`医生ID`) REFERENCES `医生` (`医生ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `处方`
--

LOCK TABLES `处方` WRITE;
/*!40000 ALTER TABLE `处方` DISABLE KEYS */;
REPLACE INTO `处方` VALUES (2,2,2,'2025-05-10 09:30:00','高血压二级'),(3,3,3,'2025-05-12 14:15:00','慢性胃炎'),(4,4,4,'2025-05-15 11:20:00','急性肠胃炎'),(5,5,5,'2025-05-20 10:00:00','儿童上呼吸道感染'),(6,2,2,'2025-06-01 08:45:00','高血压复诊'),(7,6,6,'2025-06-03 16:30:00','腰椎间盘突出');
/*!40000 ALTER TABLE `处方` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `处方_医生`
--

DROP TABLE IF EXISTS `处方_医生`;
/*!50001 DROP VIEW IF EXISTS `处方_医生`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `处方_医生` AS SELECT 
 1 AS `医生ID`,
 1 AS `姓名`,
 1 AS `科室名称`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `处方_病人`
--

DROP TABLE IF EXISTS `处方_病人`;
/*!50001 DROP VIEW IF EXISTS `处方_病人`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `处方_病人` AS SELECT 
 1 AS `病人ID`,
 1 AS `姓名`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `处方明细`
--

DROP TABLE IF EXISTS `处方明细`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `处方明细` (
  `明细ID` int NOT NULL AUTO_INCREMENT,
  `处方ID` int NOT NULL,
  `药品ID` int NOT NULL,
  `数量` int NOT NULL,
  `用法用量` text,
  PRIMARY KEY (`明细ID`),
  KEY `处方ID` (`处方ID`),
  KEY `药品ID` (`药品ID`),
  CONSTRAINT `处方明细_ibfk_1` FOREIGN KEY (`处方ID`) REFERENCES `处方` (`处方ID`),
  CONSTRAINT `处方明细_ibfk_2` FOREIGN KEY (`药品ID`) REFERENCES `药品信息` (`药品ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `处方明细`
--

LOCK TABLES `处方明细` WRITE;
/*!40000 ALTER TABLE `处方明细` DISABLE KEYS */;
REPLACE INTO `处方明细` VALUES (1,2,11,2,'每日一次，每次1片'),(2,3,12,1,'每日一次，每次1粒'),(3,4,10,1,'每日三次，每次2粒'),(4,4,13,1,'疼痛时服用，每次1片'),(5,5,14,1,'每日一次，每次1片'),(6,5,10,1,'每日三次，每次1粒'),(7,6,11,3,'每日一次，每次1片'),(8,7,13,2,'每日两次，每次1片'),(9,7,10,1,'每日两次，每次1片'),(10,7,13,1,'每日两次，每次1片');
/*!40000 ALTER TABLE `处方明细` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `处方详情视图`
--

DROP TABLE IF EXISTS `处方详情视图`;
/*!50001 DROP VIEW IF EXISTS `处方详情视图`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `处方详情视图` AS SELECT 
 1 AS `处方ID`,
 1 AS `病人姓名`,
 1 AS `病人电话`,
 1 AS `医生姓名`,
 1 AS `就诊科室`,
 1 AS `诊断结果`,
 1 AS `开具时间`,
 1 AS `收费金额`,
 1 AS `收费时间`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `库存预警`
--

DROP TABLE IF EXISTS `库存预警`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `库存预警` (
  `预警ID` int NOT NULL AUTO_INCREMENT,
  `药品ID` int NOT NULL,
  `预警信息` text,
  `预警时间` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`预警ID`),
  KEY `药品ID` (`药品ID`),
  CONSTRAINT `库存预警_ibfk_1` FOREIGN KEY (`药品ID`) REFERENCES `药品信息` (`药品ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `库存预警`
--

LOCK TABLES `库存预警` WRITE;
/*!40000 ALTER TABLE `库存预警` DISABLE KEYS */;
REPLACE INTO `库存预警` VALUES (2,13,'药品库存低于安全水平: 布洛芬','2025-06-06 16:13:59');
/*!40000 ALTER TABLE `库存预警` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `收费记录`
--

DROP TABLE IF EXISTS `收费记录`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `收费记录` (
  `收费ID` int NOT NULL AUTO_INCREMENT,
  `处方ID` int NOT NULL,
  `收费金额` decimal(10,2) NOT NULL,
  `收费时间` datetime DEFAULT CURRENT_TIMESTAMP,
  `收费员` varchar(50) DEFAULT NULL,
  `支付方式` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`收费ID`),
  KEY `处方ID` (`处方ID`),
  CONSTRAINT `收费记录_ibfk_1` FOREIGN KEY (`处方ID`) REFERENCES `处方` (`处方ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `收费记录`
--

LOCK TABLES `收费记录` WRITE;
/*!40000 ALTER TABLE `收费记录` DISABLE KEYS */;
REPLACE INTO `收费记录` VALUES (2,2,30.40,'2025-05-10 10:05:00','张财务','支付宝'),(3,3,68.00,'2025-05-12 14:40:00','李出纳','微信支付'),(4,4,43.30,'2025-05-15 12:00:00','张财务','医保卡'),(5,5,61.80,'2025-05-20 10:30:00','王收银','现金'),(6,6,45.60,'2025-06-01 09:20:00','李出纳','微信支付'),(7,7,25.00,'2025-06-03 17:00:00','张财务','医保卡'),(8,7,25.80,'2025-06-06 20:38:00','zyf','现金');
/*!40000 ALTER TABLE `收费记录` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `收费记录_处方`
--

DROP TABLE IF EXISTS `收费记录_处方`;
/*!50001 DROP VIEW IF EXISTS `收费记录_处方`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `收费记录_处方` AS SELECT 
 1 AS `处方ID`,
 1 AS `病人姓名`,
 1 AS `医生姓名`,
 1 AS `开具时间`,
 1 AS `诊断结果`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `收费记录_收费`
--

DROP TABLE IF EXISTS `收费记录_收费`;
/*!50001 DROP VIEW IF EXISTS `收费记录_收费`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `收费记录_收费` AS SELECT 
 1 AS `收费ID`,
 1 AS `处方ID`,
 1 AS `收费金额`,
 1 AS `收费时间`,
 1 AS `收费员`,
 1 AS `支付方式`,
 1 AS `病人姓名`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `未缴费处方`
--

DROP TABLE IF EXISTS `未缴费处方`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `未缴费处方` (
  `处方ID` int NOT NULL,
  `病人姓名` varchar(50) DEFAULT NULL,
  `医生姓名` varchar(50) DEFAULT NULL,
  `开具时间` datetime DEFAULT NULL,
  `诊断结果` text,
  `待缴费金额` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`处方ID`),
  CONSTRAINT `未缴费处方_ibfk_1` FOREIGN KEY (`处方ID`) REFERENCES `处方` (`处方ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `未缴费处方`
--

LOCK TABLES `未缴费处方` WRITE;
/*!40000 ALTER TABLE `未缴费处方` DISABLE KEYS */;
REPLACE INTO `未缴费处方` VALUES (7,'刘伟强','刘振华','2025-06-03 16:30:00','腰椎间盘突出',12.50);
/*!40000 ALTER TABLE `未缴费处方` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `未缴费处方视图`
--

DROP TABLE IF EXISTS `未缴费处方视图`;
/*!50001 DROP VIEW IF EXISTS `未缴费处方视图`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `未缴费处方视图` AS SELECT 
 1 AS `处方ID`,
 1 AS `病人姓名`,
 1 AS `医生姓名`,
 1 AS `开具时间`,
 1 AS `诊断结果`,
 1 AS `待缴费金额`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `病人`
--

DROP TABLE IF EXISTS `病人`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `病人` (
  `病人ID` int NOT NULL AUTO_INCREMENT,
  `姓名` varchar(50) NOT NULL,
  `性别` char(1) DEFAULT NULL,
  `出生日期` date DEFAULT NULL,
  `联系电话` varchar(20) DEFAULT NULL,
  `住址` text,
  `医保卡号` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`病人ID`),
  UNIQUE KEY `UQ_医保卡号` (`医保卡号`),
  CONSTRAINT `CK_病人性别` CHECK ((`性别` in (_utf8mb4'男',_utf8mb4'女',_utf8mb4'未知')))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `病人`
--

LOCK TABLES `病人` WRITE;
/*!40000 ALTER TABLE `病人` DISABLE KEYS */;
REPLACE INTO `病人` VALUES (2,'陈晓东','男','1985-07-12','18611112222','北京市朝阳区建国路88号','YB110225198507123456'),(3,'李静怡','女','1992-03-25','18733334444','上海市浦东新区张江路56号','YB310115199203255678'),(4,'王思聪','男','1978-11-08','18855556666','广州市天河区体育西路120号','YB440106197811084321'),(5,'赵欣然','女','2005-09-17','18977778888','深圳市南山区科技园南路18号','YB440305200509170987'),(6,'刘伟强','男','1965-02-28','18299990000','成都市武侯区人民南路四段88号','YB510107196502281234');
/*!40000 ALTER TABLE `病人` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `科室`
--

DROP TABLE IF EXISTS `科室`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `科室` (
  `科室ID` int NOT NULL AUTO_INCREMENT,
  `科室名称` varchar(50) NOT NULL,
  `负责人` varchar(50) DEFAULT NULL,
  `描述` text,
  PRIMARY KEY (`科室ID`),
  UNIQUE KEY `UQ_科室名称` (`科室名称`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `科室`
--

LOCK TABLES `科室` WRITE;
/*!40000 ALTER TABLE `科室` DISABLE KEYS */;
REPLACE INTO `科室` VALUES (2,'心血管内科','张明远','心脏及血管疾病诊疗'),(3,'消化内科','李思雨','胃肠道疾病诊疗'),(4,'急诊科','王建国','24小时急诊服务'),(5,'儿科','赵晓雯','儿童疾病诊疗'),(6,'骨科','刘振华','骨骼系统疾病诊疗');
/*!40000 ALTER TABLE `科室` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `药品信息`
--

DROP TABLE IF EXISTS `药品信息`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `药品信息` (
  `药品ID` int NOT NULL AUTO_INCREMENT,
  `药品名称` varchar(100) NOT NULL,
  `类型ID` int NOT NULL,
  `规格` varchar(50) DEFAULT NULL,
  `单位` varchar(20) DEFAULT NULL,
  `生产厂家` varchar(100) DEFAULT NULL,
  `价格` decimal(10,2) NOT NULL,
  `库存量` int DEFAULT '0',
  PRIMARY KEY (`药品ID`),
  KEY `类型ID` (`类型ID`),
  CONSTRAINT `药品信息_ibfk_1` FOREIGN KEY (`类型ID`) REFERENCES `药品类型` (`类型ID`),
  CONSTRAINT `CK_价格` CHECK ((`价格` > 0)),
  CONSTRAINT `CK_库存量` CHECK ((`库存量` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `药品信息`
--

LOCK TABLES `药品信息` WRITE;
/*!40000 ALTER TABLE `药品信息` DISABLE KEYS */;
REPLACE INTO `药品信息` VALUES (10,'阿莫西林',9,'0.5g*24粒','盒','华北制药',25.80,180),(11,'硝苯地平',10,'10mg*30片','瓶','上海信谊',15.20,220),(12,'奥美拉唑',11,'20mg*14粒','盒','阿斯利康',68.00,65),(13,'布洛芬',12,'0.3g*20片','盒','强生制药',12.50,5),(14,'维生素C',13,'100mg*60片','瓶','养生堂',26.00,110),(15,'头孢克肟',9,'0.1g*12片','盒','广州白云山',35.00,15);
/*!40000 ALTER TABLE `药品信息` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `药品库存视图`
--

DROP TABLE IF EXISTS `药品库存视图`;
/*!50001 DROP VIEW IF EXISTS `药品库存视图`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `药品库存视图` AS SELECT 
 1 AS `药品ID`,
 1 AS `药品名称`,
 1 AS `类型名称`,
 1 AS `规格`,
 1 AS `单位`,
 1 AS `库存量`,
 1 AS `价格`,
 1 AS `库存状态`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `药品类型`
--

DROP TABLE IF EXISTS `药品类型`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `药品类型` (
  `类型ID` int NOT NULL AUTO_INCREMENT,
  `类型名称` varchar(50) NOT NULL,
  `描述` text,
  PRIMARY KEY (`类型ID`),
  UNIQUE KEY `UQ_药品类型名称` (`类型名称`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `药品类型`
--

LOCK TABLES `药品类型` WRITE;
/*!40000 ALTER TABLE `药品类型` DISABLE KEYS */;
REPLACE INTO `药品类型` VALUES (9,'抗生素','用于治疗细菌感染的药物'),(10,'心血管','治疗心脏和血管疾病的药物'),(11,'消化系统','治疗胃肠道疾病的药物'),(12,'止痛药','缓解疼痛的药物'),(13,'维生素','补充人体所需维生素');
/*!40000 ALTER TABLE `药品类型` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `出库_科室`
--

/*!50001 DROP VIEW IF EXISTS `出库_科室`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `出库_科室` AS select `科室`.`科室ID` AS `科室ID`,`科室`.`科室名称` AS `科室名称` from `科室` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `处方_医生`
--

/*!50001 DROP VIEW IF EXISTS `处方_医生`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `处方_医生` AS select `医生`.`医生ID` AS `医生ID`,`医生`.`姓名` AS `姓名`,`科室`.`科室名称` AS `科室名称` from (`医生` join `科室` on((`医生`.`所属科室ID` = `科室`.`科室ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `处方_病人`
--

/*!50001 DROP VIEW IF EXISTS `处方_病人`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `处方_病人` AS select `病人`.`病人ID` AS `病人ID`,`病人`.`姓名` AS `姓名` from `病人` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `处方详情视图`
--

/*!50001 DROP VIEW IF EXISTS `处方详情视图`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `处方详情视图` AS select `cf`.`处方ID` AS `处方ID`,`b`.`姓名` AS `病人姓名`,`b`.`联系电话` AS `病人电话`,`y`.`姓名` AS `医生姓名`,`k`.`科室名称` AS `就诊科室`,`cf`.`诊断结果` AS `诊断结果`,`cf`.`开具时间` AS `开具时间`,`c`.`收费金额` AS `收费金额`,`c`.`收费时间` AS `收费时间` from ((((`处方` `cf` join `病人` `b` on((`cf`.`病人ID` = `b`.`病人ID`))) join `医生` `y` on((`cf`.`医生ID` = `y`.`医生ID`))) join `科室` `k` on((`y`.`所属科室ID` = `k`.`科室ID`))) left join `收费记录` `c` on((`cf`.`处方ID` = `c`.`处方ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `收费记录_处方`
--

/*!50001 DROP VIEW IF EXISTS `收费记录_处方`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `收费记录_处方` AS select `p`.`处方ID` AS `处方ID`,`t`.`姓名` AS `病人姓名`,`d`.`姓名` AS `医生姓名`,`p`.`开具时间` AS `开具时间`,`p`.`诊断结果` AS `诊断结果` from ((`处方` `p` join `病人` `t` on((`p`.`病人ID` = `t`.`病人ID`))) join `医生` `d` on((`p`.`医生ID` = `d`.`医生ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `收费记录_收费`
--

/*!50001 DROP VIEW IF EXISTS `收费记录_收费`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `收费记录_收费` AS select `b`.`收费ID` AS `收费ID`,`p`.`处方ID` AS `处方ID`,`b`.`收费金额` AS `收费金额`,`b`.`收费时间` AS `收费时间`,`b`.`收费员` AS `收费员`,`b`.`支付方式` AS `支付方式`,`t`.`姓名` AS `病人姓名` from ((`收费记录` `b` join `处方` `p` on((`b`.`处方ID` = `p`.`处方ID`))) join `病人` `t` on((`p`.`病人ID` = `t`.`病人ID`))) order by `b`.`收费时间` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `未缴费处方视图`
--

/*!50001 DROP VIEW IF EXISTS `未缴费处方视图`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `未缴费处方视图` AS select `cf`.`处方ID` AS `处方ID`,`b`.`姓名` AS `病人姓名`,`y`.`姓名` AS `医生姓名`,`cf`.`开具时间` AS `开具时间`,`cf`.`诊断结果` AS `诊断结果`,(ifnull(`cost`.`药品总费用`,0) - ifnull(`c`.`已缴费金额`,0)) AS `待缴费金额` from ((((`处方` `cf` join `病人` `b` on((`cf`.`病人ID` = `b`.`病人ID`))) join `医生` `y` on((`cf`.`医生ID` = `y`.`医生ID`))) left join (select `收费记录`.`处方ID` AS `处方ID`,sum(`收费记录`.`收费金额`) AS `已缴费金额` from `收费记录` group by `收费记录`.`处方ID`) `c` on((`cf`.`处方ID` = `c`.`处方ID`))) left join (select `m`.`处方ID` AS `处方ID`,sum((`m`.`数量` * `y`.`价格`)) AS `药品总费用` from (`处方明细` `m` join `药品信息` `y` on((`m`.`药品ID` = `y`.`药品ID`))) group by `m`.`处方ID`) `cost` on((`cf`.`处方ID` = `cost`.`处方ID`))) where (ifnull(`cost`.`药品总费用`,0) > ifnull(`c`.`已缴费金额`,0)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `药品库存视图`
--

/*!50001 DROP VIEW IF EXISTS `药品库存视图`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `药品库存视图` AS select `y`.`药品ID` AS `药品ID`,`y`.`药品名称` AS `药品名称`,`l`.`类型名称` AS `类型名称`,`y`.`规格` AS `规格`,`y`.`单位` AS `单位`,`y`.`库存量` AS `库存量`,`y`.`价格` AS `价格`,(case when (`y`.`库存量` < 10) then '低库存' when (`y`.`库存量` < 50) then '正常' else '充足' end) AS `库存状态` from (`药品信息` `y` join `药品类型` `l` on((`y`.`类型ID` = `l`.`类型ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 14:45:24
