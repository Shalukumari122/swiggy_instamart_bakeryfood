/*
SQLyog Professional v13.1.1 (64 bit)
MySQL - 8.0.33 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `pincodes` (
	`city` text ,
	`pincode` bigint (20),
	`storeid` varchar (75),
	`address` text ,
	`lat` double ,
	`long` double 
); 
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Delhi','110017','1382291','New Delhi, Delhi 110017, India','28.5279118','77.2088986999999');
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Delhi','110048',NULL,NULL,NULL,NULL);
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Kolkata','700075',NULL,NULL,NULL,NULL);
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Mumbai','400050','969383','Mumbai, Maharashtra 400050, India','19.0551695','72.8299518');
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Mumbai','400053',NULL,NULL,NULL,NULL);
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Mumbai','400057',NULL,NULL,NULL,NULL);
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Pune','411014','1389691','Pune, Maharashtra 411014, India','18.5574028','73.9283004999999');
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Pune','411057',NULL,NULL,NULL,NULL);
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Pune','412202',NULL,NULL,NULL,NULL);
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Hyderabad','500014','1388312','Nizamabad - Hyderabad Rd, Sai Nagar, Kompally, Hyderabad, Telangana, India','17.5487065','78.4930217');
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Hyderabad','500084','1386094','Hyderabad, Telangana 500084, India','17.4707751','78.3587426');
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Hyderabad','501501',NULL,NULL,NULL,NULL);
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Bangalore','560066','762610','Bengaluru, Karnataka 560066, India','12.9698066','77.7499632');
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Bangalore','560078','1237709','Bengaluru, Karnataka 560078, India','12.898773','77.5764094');
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Bangalore','560102','1231052','4th Cross Rd, Sector 5, HSR Layout, Bengaluru, Karnataka 560102, India','12.911862','77.6445923');
insert into `pincodes` (`city`, `pincode`, `storeid`, `address`, `lat`, `long`) values('Kolkata','700027',NULL,NULL,NULL,NULL);
