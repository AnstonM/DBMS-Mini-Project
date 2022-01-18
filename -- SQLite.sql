-- SQLite
create table if not exists route(
     route_id integer primary key autoincrement,
     source varchar2(20),
    destination varchar2(20),
   fare number(10,2) NOT NULL,
   distance varchar2(10),
   time varchar2(10));

INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Bangalore','Mysore',3993.90,'143.8km','3hr 27min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Bangalore','Mangalore',7441.59,'351.8km','7hr 58min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Bangalore','Chennai',5499.00,'345.7km','6hr 32min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Bangalore','Telangana',14990.00,'715.5km','11hr 32min');

INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Mangalore','Mumbai',14350.90,'893.3km','16hr 32min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Mangalore','Bangalore',7441.59,'351.8km','7hr 58min');
INSERT INTO route (source, destination,fare,distance,time)
VALUES ('Mangalore','Chennai',20499.00,'705.0km','14hr 13min');


drop TABLE driver

DELETE  from driver where driver_id=101

create TABLE driver(
driver_id integer PRIMARY KEY,
Dname varchar2(20) NOT NULL,
DL_no number(10) UNIQUE NOT NULL,
dph_no number(10) NOT NULL,
Age number(2));

INSERT into driver VALUES(101,'Arman Malik','A4329LF4J49042J',
9440487109,23);
INSERT into driver VALUES(102,'Rohan Sharma','JF30FO381JD914F',
89319037495,44);
INSERT into driver
VALUES(103,'Rahul K','DKW029099EK2KD2',
9903199103,32);
INSERT into driver
VALUES(104,'Rajesh Sharma','12J9EO10DL33J4F',
89109893813,45);
INSERT into driver
VALUES(105,'Ronit R','A92K2801OE350C3',
9201113031,45);
INSERT into driver
VALUES(106,'Raj Kapoor','29DEO10EPC14EKD',
7718304194,32);
INSERT into driver
VALUES(107,'Aryan Khan','381LE01EAD9238F',
9120314451,35);
INSERT into driver
VALUES(108,'Rohan Joshi','1JD919DN4501PCV',
9998110384,29);

create table cab(
type varchar2(15) NOT NULL,
Driver_id REFERENCES driver(driver_id),
reg_no varchar2(15) NOT NULL,
Avail varchar2(3) NOT NULL,
CHECK(Avail in('Yes','No')),
PRIMARY KEY(Driver_id,reg_no)); 

INSERT INTO cab VALUES('SUV',101,'KA19P1234','Yes');
INSERT INTO cab VALUES('Sedan',102,'KA19MH1230','Yes');
INSERT INTO cab VALUES('Minivan',103,'KA03P0089','Yes');
INSERT INTO cab VALUES('Hatchback',104,'KA01P1345','Yes');
INSERT INTO cab VALUES('SUV',105,'MH93P1491','Yes');
INSERT INTO cab VALUES('Sedan',106,'KA29PG314','Yes');
INSERT INTO cab VALUES('SUV',107,'KA38N2910','Yes');

create table Booking(
booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
route_id REFERENCES route(route_id),
reg_no REFERENCES Cab(reg_no),
driver_id REFERENCES CAB(driver_id),
total_fare number(10,2) not null);


INSERT INTO Booking (route_id,reg_no,driver_id,total_fare) VALUES(2,'KA38N2910',107,7441.59);

DELETE FROM Booking where booking_id = 55

DELETE FROM booking where 1<2