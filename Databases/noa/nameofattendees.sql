CREATE TABLE `nameofattendees` (
  `attendeeid` int NOT NULL AUTO_INCREMENT,
  `attendeename` varchar(100) NOT NULL,
  `attendeeemail` varchar(100) NOT NULL,
  PRIMARY KEY (`attendeeid`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `nameofattendees` WRITE;

INSERT INTO `nameofattendees` VALUES (1,'Reem Said','reemahmed@auceygpt.edu'),(2,'Omar Fayed','ofayed@aucegypt.edu'),(3,'Renad AlKady','renadelkady@aucegypt.edu'),(4,'Abdelrahman Said','arefaat@aucegypt.edu'),(5,'Youssef Abouelenin','yamr5611@aucegypt.edu'),(6,'Sherif Sakran','sherifsakran@aucegypt.edu'),(7,'Abdallah Sabah','asabah@aucegypt.edu');

UNLOCK TABLES;