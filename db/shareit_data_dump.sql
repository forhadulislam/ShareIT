BEGIN TRANSACTION;

INSERT INTO `users` VALUES (1,'sadi','sadi@gmail.com',1488404307);
INSERT INTO `users` VALUES (2,'khaled','khaled@gmail.com',1488404307);
INSERT INTO `users` VALUES (3,'fatema','fatema@gmail.com',1488404777);
INSERT INTO `users` VALUES (4,'asare','asare@gmail.com',1488413278);
INSERT INTO `users` VALUES (5,'arash','arash@gmail.com',1488413278);
INSERT INTO `users_profile` VALUES (1,'Sadi Aliss','0469555307','http://99reviews.com','Yliopistokatu 24 C','shifat2sadi','M');
INSERT INTO `users_profile` VALUES (2,'Mohamed Khaled ','048998980','http://egyptian.com','Yliopistokatu 38','khaled.mohamed','M');
INSERT INTO `users_profile` VALUES (3,'Ummul Khayer Fatema','088494899','','Kalervontie 3 A','ukfttnd','F');
INSERT INTO `users_profile` VALUES (4,'Asare Kenedy','077897898','','Yliopistokatu 14','asare','M');
INSERT INTO `users_profile` VALUES (5,'Arash Sattari','988788899','','Kandentie 12','arash.sattari','M');
INSERT INTO `categories` VALUES ('Electronics','Electronic items',1488404307,1488493919,1);
INSERT INTO `categories` VALUES ('Book','Books and study materials',1488404307,1488404307,2);
INSERT INTO `categories` VALUES ('Furnitures','Furniture materials',1488404777,1488404777,3);
INSERT INTO `categories` VALUES ('Cars','Cars and other vehicles ',1488493919,1488493919,4);
INSERT INTO `categories` VALUES ('Costemics','Costemic items',1488493919,1488493919,5);
INSERT INTO `posts` VALUES (1,1,'New chair for sale','I want to sell my chair',2,'chair, sale',1488413278,1488413278);
INSERT INTO `posts` VALUES (2,1,'Ikea table','Table bought from ikea and is in a very good condition',3,'table, ikea',1488414807,1488413278);
INSERT INTO `posts` VALUES (3,2,'Brand new car','Brand new car just used for several days',4,'car',1488413278,1488413278);
INSERT INTO `posts` VALUES (4,3,'Some furnitures','In great condition. Hurry',3,'furniture',1488413278,1488413278);
INSERT INTO `posts` VALUES (5,1,'Some stuffs','Clearance sale . hurry',2,'sale',1488413278,1488413278);
INSERT INTO `reports` VALUES (1,1,2,'its spammy');
INSERT INTO `reports` VALUES (2,1,1,'Bad post');
INSERT INTO `reports` VALUES (3,2,1,'i dont like it');
INSERT INTO `reports` VALUES (4,2,3,'awful');
INSERT INTO `reports` VALUES (5,2,2,'worst post .. remove it');
INSERT INTO `messages` VALUES (1,'Hi sadi .. I am interested in this product',2,1,1488413278);
INSERT INTO `messages` VALUES (2,'khaled, I want this',1,2,1488413295);
INSERT INTO `messages` VALUES (3,'nothing important',1,2,1488507537);
INSERT INTO `messages` VALUES (4,'will contact you soon',1,3,1488413278);
INSERT INTO `messages` VALUES (5,'what is happening to you',2,3,1488413278);

COMMIT;