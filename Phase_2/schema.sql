SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS cs6400_fa19_team060 DEFAULT CHARACTER SET utf8mb4  DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_fa19_team060;

--Tables

CREATE TABLE Sell(
    FK_vin_vehicle varchar(20) not null,
	FK_customer_id_customer int(16) unsigned not null,
	sales_price double not null,
	sales_date Date not null,
	vehicle_condition varchar(20),
	PRIMARY KEY (FK_vin_vehicle, FK_customer_id_customer)
);
 
CREATE TABLE Loan (
    FK_vin_loan varchar(20) not null,
	FK_username_priveledged_user varchar(20) not null,
	loanID int(5) not null AUTO_INCREMENT,
	loanterm int(5) not null,
	interest_rate double,
	down_payment double,
	month_payment double,
	start_month Date,
	PRIMARY KEY(loanID)
);
 
CREATE TABLE  PriviledgedUser(
    username varchar(20) not null,
	pass_word varchar(20)not null,
	priviledge_user_type varchar(20) not null,
	first_name varchar(20) not null,
	last_name varchar(20) not null,
	PRIMARY KEY(username)
);

CREATE TABLE Customer (
    customerID int(16) unsigned NOT NULL AUTO_INCREMENT,
    email_address varchar(250) NOT NULL,
    phone_number bigint(10) unsigned NOT NULL,
    street varchar(250) NOT NULL,
    postal_code int(6) unsigned NOT NULL,
    city varchar(15) NOT NULL,
    state varchar(20) NOT NULL,
    PRIMARY KEY (CustomerID),
    UNIQUE KEY  email_address  (email_address)
);

CREATE TABLE Individual (
    FK_individual_customer_id int(16) unsigned not null,
    driverLicenseNumber int(20) unsigned NOT NULL,
    first_name varchar(25) NOT NULL,
    last_name varchar(25) NOT NULL,
    PRIMARY KEY (driverLicenseNumber)
);

CREATE TABLE Business(
    FK_business_customer_id int(16) unsigned not null,
    taxIDNumber int(20) unsigned NOT NULL,
    business_name varchar(25) NOT NULL,
    name varchar(25) NOT NULL,
    contact int(10) unsigned NOT NULL,
    PRIMARY KEY (taxIDNumber)
);




CREATE TABLE  Vehicle(
	vin varchar(20) not null,
	vehicle_type varchar(20) not null,
	cost double not null,
	model_name varchar(20) not null,
	model_year int(4) not null,
	Fk_manufacturer_manufacturerid int(5) NOT NULL,
	mileage int(3) not null,
	description varchar(100),
	PRIMARY KEY(vin)
);


CREATE TABLE VehicleColor ( 
	FK_vin_vehicle varchar(16) not null, 
	color varchar(15) 
);


CREATE TABLE Manufacturer(
    manufacturer_id int(5) not null,
    Manufacturer_name varchar(20) NOT NULL,
    PRIMARY KEY(manufacturer_id)
);


CREATE TABLE Vendor(
    vendorName varchar(20) not null,
    street varchar (20),
    city varchar(20),
    state varchar(20),
    postal_code int not null,
    phone_number bigint(12) not null,
    PRIMARY KEY(vendorName)
);

CREATE TABLE Contains(
    Fk_contains_ordernumber varchar(20), 
    Fk_contains_partnumber varchar(20) NOT NULL,
    PartStatus varchar(20) NOT NULL
);


CREATE TABLE  Part(
    partNumber varchar(20) not null,
    cost double not null,
    description varchar(100),
    PRIMARY KEY (partNumber)
);

CREATE TABLE PartOrder(
    FK_vin_part_order varchar(20)not null,
    FK_vendor_name_part_order varchar(20) not null,
    FK_user_name_part_order varchar(20) not null,
    orderNumber varchar(20),
    PRIMARY  KEY(orderNumber)
);


CREATE TABLE Buy(
    FK_vin_vehicle varchar(20) not null,
    FK_customer_id_customer int(16) unsigned not null,
    purchase_price double not null,
    purchase_date Date not null,
    PRIMARY KEY (FK_vin_vehicle, FK_customer_id_customer)
);


--Constraints

ALTER TABLE Individual
ADD CONSTRAINT FK_individual_customer_id FOREIGN KEY (FK_individual_customer_id)
REFERENCES
Customer (CustomerID);

ALTER TABLE Business
ADD CONSTRAINT FK_business_customer_id FOREIGN KEY (FK_business_customer_id)
REFERENCES
Customer (CustomerID);

ALTER TABLE Loan
Add CONSTRAINT FK_username_priveledged_user FOREIGN KEY(FK_username_priveledged_user)
REFERENCES 
PriviledgedUser(username);
 
 
ALTER TABLE Sell
Add CONSTRAINT FK_vin_vehicle_sell FOREIGN KEY(FK_vin_vehicle)
REFERENCES 
Vehicle(vin);
 
ALTER TABLE Sell
Add CONSTRAINT FK_customer_id_customer_sell FOREIGN KEY(FK_customer_id_customer)
REFERENCES 
Customer(customerID);

ALTER TABLE  VehicleColor
Add CONSTRAINT FK_vin_vehicle_color FOREIGN KEY(FK_vin_vehicle)
REFERENCES 
Vehicle(vin);

ALTER TABLE  Vehicle
Add CONSTRAINT FK_vin_vehicle_color FOREIGN KEY(FK_vin_vehicle)
REFERENCES 
Vehicle(vin);

ALTER TABLE Manufacturer
ADD CONSTRAINT Fk_manufacturer_manufacturerid FOREIGN KEY(Fk_manufacturer_manufacturerid)
REFERENCES Vehicle(manufacturer_id);

ALTER TABLE Contains
ADD CONSTRAINT Fk_contains_ordernumber FOREIGN KEY(Fk_contains_ordernumber)
REFERENCES 
PartOrder(orderNumber);

ALTER TABLE Contains
ADD CONSTRAINT Fk_contains_partnumber FOREIGN KEY(Fk_contains_partnumber)
REFERENCES 
Part(partNumber);

ALTER TABLE Buy
Add CONSTRAINT FK_vin_vehicle_buy FOREIGN KEY(FK_vin_vehicle)
REFERENCES Vehicle(vin);

ALTER TABLE Buy
Add CONSTRAINT FK_customer_id_customer_buy FOREIGN KEY(FK_customer_id_customer)
REFERENCES Customer(customerID);

ALTER TABLE PartOrder
Add CONSTRAINT FK_vin_part_order FOREIGN KEY(FK_vin_part_order)
REFERENCES Vehicle(vin);

ALTER TABLE PartOrder
Add CONSTRAINT FK_vendor_name_part_order FOREIGN KEY(FK_vendor_name_part_order)
REFERENCES Vendor(vendorName);


