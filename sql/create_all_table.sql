CREATE DATABASE IF NOT EXISTS seat_reservation;

USE seat_reservation;

CREATE TABLE Student (
	id INT PRIMARY KEY AUTO_INCREMENT,
	openid VARCHAR(50) NOT NULL,
	student_id VARCHAR(11) NOT NULL,
	name VARCHAR(50) NOT NULL,
	password VARCHAR(255) NOT NULL,
	wechat_number VARCHAR(50),
	school VARCHAR(50),
	breach_count INT DEFAULT 0
);

CREATE TABLE Administer (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	password VARCHAR(255) NOT NULL,
	wechat_number VARCHAR(50)
);


CREATE TABLE Building (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	campus VARCHAR(20) NOT NULL,
	open_time TIME NOT NULL,
	close_time TIME NOT NULL,
	deprecated BOOLEAN DEFAULT False NOT NULL
);

CREATE TABLE Room (
	id INT PRIMARY KEY AUTO_INCREMENT,
	building_id INT NOT NULL,
	school VARCHAR(50),
	name VARCHAR(100) NOT NULL,
	open_time TIME NOT NULL,
	close_time TIME NOT NULL,
	deprecated BOOLEAN DEFAULT False NOT NULL
);

CREATE TABLE Seat (
	id INT PRIMARY KEY AUTO_INCREMENT,
	room_id INT NOT NULL,
	near_fixed_socket BOOLEAN,
	near_movable_socket BOOLEAN,
	near_window BOOLEAN,
	deprecated BOOLEAN DEFAULT False NOT NULL
);


CREATE TABLE Reservation (
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT,
	room_id INT,
	seat_id INT,
	create_time DATETIME NOT NULL,
	start_time DATETIME NOT NULL,
	end_time DATETIME NOT NULL,
	status INT DEFAULT 0 NOT NULL
);

CREATE TABLE AdminConfig (
	id INT PRIMARY KEY AUTO_INCREMENT,
	config_key VARCHAR(100) NOT NULL,
	config_value VARCHAR(255) NOT NULL
);