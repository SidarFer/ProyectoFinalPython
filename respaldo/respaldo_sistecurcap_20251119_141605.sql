-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: sistecurcap
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `calificacionesunidad`
--

DROP TABLE IF EXISTS `calificacionesunidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `calificacionesunidad` (
  `idcalificacion` int(11) NOT NULL AUTO_INCREMENT,
  `idmatricula` int(11) DEFAULT NULL,
  `idunidad` int(11) DEFAULT NULL,
  `calificacion` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`idcalificacion`),
  KEY `idmatricula_idx` (`idmatricula`),
  KEY `idunidad_idx` (`idunidad`),
  CONSTRAINT `idmatricula` FOREIGN KEY (`idmatricula`) REFERENCES `matriculas` (`idmatricula`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idunidad` FOREIGN KEY (`idunidad`) REFERENCES `unidadescursos` (`idunidad`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calificacionesunidad`
--

LOCK TABLES `calificacionesunidad` WRITE;
/*!40000 ALTER TABLE `calificacionesunidad` DISABLE KEYS */;
INSERT INTO `calificacionesunidad` VALUES (1,4,1,90.00),(2,4,2,100.00),(3,4,3,80.00);
/*!40000 ALTER TABLE `calificacionesunidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cursos`
--

DROP TABLE IF EXISTS `cursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cursos` (
  `idcurso` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(10) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL COMMENT 'Nombre del Curso',
  `tipo` varchar(50) DEFAULT NULL COMMENT 'técnico, libre, etc',
  `horas` int(11) DEFAULT NULL COMMENT 'Cantidad de horas del curso',
  `fechainicio` date DEFAULT NULL COMMENT 'Fecha de inicio del curso',
  `fechafin` date DEFAULT NULL COMMENT 'Fecha de finalización del curso',
  PRIMARY KEY (`idcurso`),
  UNIQUE KEY `codigo_UNIQUE` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cursos`
--

LOCK TABLES `cursos` WRITE;
/*!40000 ALTER TABLE `cursos` DISABLE KEYS */;
INSERT INTO `cursos` VALUES (1,'C001','Excel Básico','Libre',50,'2025-11-01','2025-11-05'),(3,'C002','Excel Avanzado','Libre',100,'2025-11-17','2025-12-12'),(4,'C003','Chalupa','Complementación',40,'2025-12-01','2025-12-15'),(5,'C004','Creación de Piñatas','Discapacidad',10,'2025-11-19','0000-00-00');
/*!40000 ALTER TABLE `cursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estudiantes`
--

DROP TABLE IF EXISTS `estudiantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estudiantes` (
  `idestudiante` int(11) NOT NULL AUTO_INCREMENT,
  `ncarnet` varchar(20) DEFAULT NULL,
  `nombres` varchar(80) DEFAULT NULL,
  `apellidos` varchar(80) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `fechanacimiento` date DEFAULT NULL,
  `estado` enum('Activo','Inactivo') DEFAULT 'Activo',
  PRIMARY KEY (`idestudiante`),
  UNIQUE KEY `ncarnet_UNIQUE` (`ncarnet`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes`
--

LOCK TABLES `estudiantes` WRITE;
/*!40000 ALTER TABLE `estudiantes` DISABLE KEYS */;
INSERT INTO `estudiantes` VALUES (1,'E0001','Sidar Fernando','Rivas Berrios','Praderas','1977-02-12','Activo'),(2,'E0002','Fernando Gabriel','Rivas Robleto','Praderas Nunevo León','2021-04-21','Activo');
/*!40000 ALTER TABLE `estudiantes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graduaciones`
--

DROP TABLE IF EXISTS `graduaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `graduaciones` (
  `idgraduacion` int(11) NOT NULL AUTO_INCREMENT,
  `idmatricula` int(11) DEFAULT NULL,
  `fechagraduacion` date DEFAULT NULL,
  `resultado` enum('Aprobado','Reprobado') DEFAULT 'Aprobado',
  PRIMARY KEY (`idgraduacion`),
  KEY `idmatricula` (`idmatricula`),
  CONSTRAINT `graduaciones_ibfk_1` FOREIGN KEY (`idmatricula`) REFERENCES `matriculas` (`idmatricula`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graduaciones`
--

LOCK TABLES `graduaciones` WRITE;
/*!40000 ALTER TABLE `graduaciones` DISABLE KEYS */;
INSERT INTO `graduaciones` VALUES (1,1,'2025-12-15','Aprobado'),(2,2,'2025-12-15','Aprobado');
/*!40000 ALTER TABLE `graduaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matriculas`
--

DROP TABLE IF EXISTS `matriculas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `matriculas` (
  `idmatricula` int(11) NOT NULL AUTO_INCREMENT,
  `idestudiante` int(11) DEFAULT NULL,
  `idcurso` int(11) DEFAULT NULL,
  `fechamatricula` date DEFAULT NULL,
  `estado` enum('Cursando','Retirado','Finalizado') DEFAULT 'Cursando',
  PRIMARY KEY (`idmatricula`),
  KEY `idestudiante_idx` (`idestudiante`),
  KEY `idcurso_idx` (`idcurso`),
  CONSTRAINT `idcurso` FOREIGN KEY (`idcurso`) REFERENCES `cursos` (`idcurso`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idestudiante` FOREIGN KEY (`idestudiante`) REFERENCES `estudiantes` (`idestudiante`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matriculas`
--

LOCK TABLES `matriculas` WRITE;
/*!40000 ALTER TABLE `matriculas` DISABLE KEYS */;
INSERT INTO `matriculas` VALUES (1,1,4,'2025-11-18','Cursando'),(2,2,3,'2025-11-18','Cursando'),(3,1,1,'2025-11-19','Finalizado'),(4,1,3,'2025-11-01','Cursando');
/*!40000 ALTER TABLE `matriculas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrador'),(2,'Usuario');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidadescursos`
--

DROP TABLE IF EXISTS `unidadescursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidadescursos` (
  `idunidad` int(11) NOT NULL AUTO_INCREMENT,
  `idcurso` int(11) DEFAULT NULL,
  `nombreunidad` varchar(100) DEFAULT NULL,
  `numerounidad` int(11) DEFAULT NULL,
  PRIMARY KEY (`idunidad`),
  KEY `idcurso_idx` (`idcurso`),
  CONSTRAINT `idcursou` FOREIGN KEY (`idcurso`) REFERENCES `cursos` (`idcurso`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidadescursos`
--

LOCK TABLES `unidadescursos` WRITE;
/*!40000 ALTER TABLE `unidadescursos` DISABLE KEYS */;
INSERT INTO `unidadescursos` VALUES (1,3,'Conceptos Basicos',1),(2,3,'Funciones',2),(3,3,'Gráficos',3),(4,5,'Conceptos Básicos',1),(5,5,'Moldeado del Cartón',2);
/*!40000 ALTER TABLE `unidadescursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `rolid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `rolid` (`rolid`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rolid`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','1234',1),(2,'sifer','4567',2),(5,'gabriel','159',2);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-19 14:16:06
