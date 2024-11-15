create database if not exists store;
use store;

CREATE TABLE if not exists  product (
	upc VARCHAR(255) PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	type VARCHAR(30) NOT NULL,
	category VARCHAR(50),
	description text,
	stock INT UNSIGNED default 0  NOT NULL,
	price FLOAT  NOT NULL check (price >= 0),
	tax FLOAT NOT NULL DEFAULT 0 check(tax >= 0),
	rating FLOAT NOT NULL DEFAULT 5.0 check(rating >= 0 and rating <=5.0),
	reviews int UNSIGNED DEFAULT 0 not null
);

create table if not exists image(
imgID int UNSIGNED primary key auto_increment,
upc varchar(255) not null,
file longBLOB NOT NULL,
alt varchar(255),
Foreign Key (upc) REFERENCES product(upc)
);

create table if not exists user(
	uid int UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	first_name VARCHAR(32) NOT NULL,
	last_name VARCHAR(32) NOT NULL,
	email VARCHAR(50) UNIQUE not null,
	dob date not null ,
	password varchar(50),
	city varchar(50) not null,
	country varchar(50) not null
);
