/*
Create Table Statements

 */
CREATE TABLE IF NOT EXISTS Users(UID SERIAL PRIMARY KEY, FName VARCHAR(50), LName VARCHAR(50), password TEXT, PNumber INTEGER, Email VARCHAR(100) UNIQUE, Confirmation BOOLEAN, LogAttempt INTEGER, Blocked TIMESTAMP);
CREATE TABLE IF NOT EXISTS Client(CID SERIAL PRIMARY KEY , UID INTEGER REFERENCES Users(UID) CHECK(NOT NULL), DebtorFlag BOOLEAN);
CREATE TABLE IF NOT EXISTS Worker(WID SERIAL PRIMARY KEY, UID INTEGER REFERENCES Users(UID) CHECK(NOT NULL), Status VARCHAR(15));
CREATE TABLE IF NOT EXISTS Admin(AID SERIAL PRIMARY KEY, UID INTEGER REFERENCES Users(UID) CHECK(NOT NULL));
CREATE TABLE IF NOT EXISTS Bike(BID Serial PRIMARY KEY, LP VARCHAR(15), RFID VARCHAR(50) UNIQUE, Status varchar(15), brand TEXT, model TEXT);
CREATE TABLE IF NOT EXISTS Rental(RID serial PRIMARY KEY, STime TIMESTAMP, ETime TIMESTAMP, Client INTEGER REFERENCES Client (CID), BID INTEGER REFERENCES Bike(BID), DispatchedBy INTEGER REFERENCES Worker(WID), ReceivedBy  INTEGER REFERENCES Worker(WID), dueDate TIMESTAMP);
CREATE TABLE IF NOT EXISTS Transactions(TID SERIAL PRIMARY KEY, stamp timestamp, Token varchar(50), CID INTEGER REFERENCES Client(CID) CHECK(NOT NULL), Status VARCHAR(15), Cost REAL, SMID INTEGER REFERENCES ServiceMaintenance(SMID));
CREATE TABLE IF NOT EXISTS RentLink(RID INTEGER REFERENCES Rental(RID), TID INTEGER REFERENCES Transactions(TID), PRIMARY KEY(TID, RID));
CREATE TABLE IF NOT EXISTS Maintenance(MID SERIAL PRIMARY KEY, StartTime TIMESTAMP, EndTime TIMESTAMP, Status varchar(15), Notes VARCHAR(180), BID INTEGER REFERENCES Bike(BID), RequestedBy INTEGER REFERENCES Users(UID), ServicedBy INTEGER REFERENCES Worker(WID), Service text);
CREATE TABLE IF NOT EXISTS DecommissionReq( DQID SERIAL PRIMARY KEY , RequestedBy INTEGER REFERENCES Users(UID) CHECK(NOT NULL), AnsweredBy INTEGER REFERENCES Admin(AID), Status VARCHAR(15),  BID INTEGER REFERENCES Bike(BID) CHECK(NOT NULL));
CREATE TABLE IF NOT EXISTS ServiceMaintenance(SMID SERIAL PRIMARY KEY, FName varchar(50), LName varchar(50), Bike varchar(50), Service varchar(100), WorkedBy INTEGER REFERENCES Worker(WID), WorkStatus varchar(15), Notes VARCHAR(180), STime TIMESTAMP, ETime TIMESTAMP, TID INTEGER REFERENCES Transactions(TID));
CREATE TABLE IF NOT EXISTS PunchCard(PCID serial primary key, stampType varchar(5), stamp timestamp, WID INTEGER REFERENCES Worker(WID));
CREATE TABLE IF NOT EXISTS Plans(PID INTEGER primary key, name varchar(15), amount integer);

/*
Create User
 */
INSERT INTO USERS( FName, LName, password, PNumber, Email, Confirmation) VALUES ('I', 'Couver', crypt('password', gen_salt('bf')), '5555555555', 'i@ece.com', true) RETURNING uid;
SELECT * FROM USERS WHERE Email= 'e@r.com';
/*
Create Admin, Create Worker, Client
 */
INSERT INTO Admin (UID )VALUES ((Select  UID FROM Users where Email = 'e@mail.com') );
Select  UID FROM Users where Email = 'e@f.com';
INSERT INTO Client (UID )VALUES ((Select  UID FROM Users where Email = 'fgfgf') ) RETURNING CID;
SELECT * FROM Client NATURAL INNER JOIN Users WHERE Email = 'e@r.com';
INSERT INTO Worker (UID )VALUES ((Select  UID FROM Users where Email = 'e@mail.com') );

/*
Logins:
 */

SELECT UID from Users where email = 'e@r.com'  AND password = crypt('passw', password) ;

/*
Add Bike to system
 */

INSERT INTO Bike(lp, rfid, bikestatus, brand, model) VALUES ('1236', '123456', 'Available', 'OFO', 'HISTANDARD');

/*
Available Bikes

Statuses Include Available, Rented, Reserved, Awaiting Decomission, Decomissioned, Maintainance

 */
SELECT * FROM bike where status = 'Available';

/*
Rent Bike in Mobile App
 */

/*
    Reserve Bike, Revert If Transaction Fails
 */
UPDATE bike SET bikestatus = 'RESERVED' WHERE BID in (SELECT bid from bike where bikestatus = 'Available' limit 1) returning bid;

/*
    Save Successful Transaction and create rental object
 */
INSERT INTO transactions(stamp, token, cid, status, Cost) VALUES (now(), 'token', 11, 'Completed', (SELECT amount from plans WHERE PID = 1)) returning TID;
INSERT INTO rental(stime, client, dueDate) VALUES (now(), 11,current_date +8 ) RETURNING RID;
INSERT INTO RentLink(RID, TID) VALUES (3, 11);

/*
   Update Rental Upon Dispatch
 */


  /*
  Find Rental to be Updated
   */
  UPDATE Rental set DispatchedBy = 1 where RID = 3;

/*
Find bike scanned
 */
SELECT BID, Bikestatus FROM bike WHERE RFID =  '1111111' or LP = '1236';

/*
If Status = 'Available' reserve bike and release 1 reserved bike
 */
UPDATE bike set Status = 'Rented' where BID = 'bidGiven';
UPDATE Bike set Status = 'Available' where bid = (SELECT BID from bike where Status= 'Reserved' LIMIT 1);
 /*
 If Status = Reserved update to rented
  */
 UPDATE Bike SET Status = 'Rented' where BID = 3;


/*
Update Rental by inserting final bike dispatched
 */
UPDATE rental SET BID = 3 where RID = 3;


/*
   Update Upon Rental Return
 */

 UPDATE Rental set ETime = now(), ReceivedBy = 1 where RID = (SELECT rid from bike inner join Rental ON Bike.BID = Rental.BID AND RFID = '111111111' and rental.ReceivedBy isnull );
 UPDATE BIKE SET bikestatus = 'AVAILABLE' WHERE bID = (SELECT BID FROM Bike WHERE RFID = '111111111');

/*
Create ServiceMaintenance
 */

 INSERT INTO ServiceMaintenance(fname, lname, bike, service, workstatus, notes, stime ) VALUES ('fNAme', 'lName', 'bike', 'service', 'StandBy', 'notes', now());

/*
Checkout ServiceMaintenance
 */

 UPDATE ServiceMaintenance set WorkedBy = 1, WorkStatus='Done', ETime = now() where SMID = 1;

/*
Decomission Request
 */

insert into DecommissionReq( RequestedBy, Status, BID) values ('WorkerRequesting', 'Pending', 'bidRequested');

/*
Update Request
 */

 update DecommissionReq set AnsweredBy = 'AdminAnswering', Status = 'Approved/Denied' where DQID = 'dqidGiven';

/*
Create new Maintainance Request
 */

 INSERT INTO Maintenance(starttime, status, bid, requestedby) VALUES (now(), 'Pending',  'bidGiven', 'requestor');

/*
Update MaintenanceRequest
 */

 update Maintenance set servicedby = 'Server', EndTime= now(), Service = 'Services Done', Notes = 'Additional Details' , Status = 'Finished' where MID = 'midGiven' and Status ='Pending' ;

/*
PunchCard
 */

 insert into PunchCard(stampType, STAMP, WID) VALUES ('In / Out ', now(), 'Worker_ID');

/*
Financial Report
 */

/*
Get Rentals in the Last 7 Days
 */
 select count(*) from Rental where current_date - STime::date < 7;

/*
Get Revenue for the last 7 days
 */
 select sum(cost) from Transactions where Status !='Failed' and current_date - stamp :: date <7;

/*
Cash Late Fee
 */

 SELECT  ceil((DATE_PART('day', current_date - (SELECT dueDate from Rental where RID = 2))/7) )* (SELECT amount from plans WHERE PID = 2);

SELECT  current_date - (SELECT dueDate from Rental where RID = 2)

select * from Maintenance

select * from Plans