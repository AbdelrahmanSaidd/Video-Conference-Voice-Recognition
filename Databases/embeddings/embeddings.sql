CREATE TABLE `embeddings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `voice` varchar(100),
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `embeddings` WRITE;

INSERT INTO `embeddings` VALUES (1,'Reem', 'Said','ReemSaid.gmm'),(2,'Omar','Fayed',NULL),(3,'Renad','AlKady','RenadAlKady.gmm'),(4,'Abdelrahman' ,'Said','AbdelrahmanSaid.gmm'),(5,'Youssef', 'Abouelenin','YoussefAbouelenin.gmm'),(6,'Sherif', 'Sakran',NULL);

UNLOCK TABLES;
