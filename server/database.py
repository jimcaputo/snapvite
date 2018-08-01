import MySQLdb


USER = 'snapvite'
PASSWORD = 'snapvite_password'
DATABASE = 'snapvite'


def insert_update_delete(sql):
	db = MySQLdb.connect('localhost', USER, PASSWORD, DATABASE)
	cursor = db.cursor()

	response = ''
	try:
		cursor.execute(sql)
		db.commit()
		response = 'Success'
	except Exception as err:
		db.rollback()
		response = 'database.py:insert_update_delete - ' + str(err)
		print(response)
		
	db.close()
	return response


def read(sql):
	db = MySQLdb.connect('localhost', USER, PASSWORD, DATABASE)
	cursor = db.cursor()

	rows = ()
	response = ''
	try:
		cursor.execute(sql)
		rows = cursor.fetchall()
		response = 'Success'
	except Exception as err:
		response = 'database.py:read - ' + str(err)
		print(response)
	
	db.close()
	return rows, response


'''

CREATE USER 'snapvite'@'localhost' IDENTIFIED BY 'snapvite_password';
GRANT ALL PRIVILEGES ON *.* TO 'snapvite'@'localhost' WITH GRANT OPTION;
CREATE DATABASE snapvite;


DELIMITER $$
CREATE PROCEDURE create_user(p_phone_number VARCHAR(20), p_validation_code VARCHAR(10))
BEGIN
INSERT INTO users (phone_number) VALUES (p_phone_number) ON DUPLICATE KEY UPDATE phone_number=p_phone_number;
INSERT INTO validation_codes (phone_number, validation_code, expire_time) VALUES (p_phone_number, p_validation_code, DATE_ADD(NOW(), INTERVAL 1 HOUR));
END $$
DELIMITER ; $$


CREATE TABLE users
(
phone_number VARCHAR(20) NOT NULL,
user_name VARCHAR(20),
create_date DATETIME DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(phone_number)
);

CREATE TABLE validation_codes
(
phone_number VARCHAR(20) NOT NULL,
validation_code VARCHAR(5) NOT NULL,
expire_time DATETIME NOT NULL,
PRIMARY KEY(phone_number, validation_code)
);


TODO - housekeeping work to do:
- job that deletes past date reservations
- job that deletes old validation codes

'''