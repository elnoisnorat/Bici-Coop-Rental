/*
Create Table Statements

 */
CREATE TABLE Users(UID SERIAL PRIMARY KEY, FName VARCHAR(50), LName VARCHAR(50), password TEXT, PNumber smallint, Email VARCHAR(100) UNIQUE);
CREATE TABLE Client(CID SERIAL PRIMARY KEY , UID INTEGER REFERENCES Users(UID));
CREATE TABLE Worker(WID SERIAL PRIMARY KEY, UID INTEGER REFERENCES Users(UID), Status VARCHAR(15));
CREATE TABLE Admin(AID SERIAL PRIMARY KEY, UID INTEGER REFERENCES Users(UID));

CREATE TABLE Bike(BID Serial PRIMARY KEY, LP VARCHAR(15), RFID VARCHAR(50), Status varchar(15), brand TEXT, model TEXT);
CREATE TABLE RentLink(RID INTEGER REFERENCES Rental(RID), TID INTEGER REFERENCES Transactions(TID), PRIMARY KEY(TID, RID));
CREATE TABLE Rental(RID serial PRIMARY KEY, STime TIMESTAMP, ETime TIMESTAMP, Client INTEGER REFERENCES Client (CID), BID INTEGER REFERENCES Bike(BID), DispatchedBy INTEGER REFERENCES Worker(WID), RecivedBy INTEGER REFERENCES Worker(WID), dueDate TIMESTAMP);
CREATE TABLE Transactions(TID SERIAL PRIMARY KEY, stamp timestamp, Token varchar(50), CID INTEGER REFERENCES Client(CID), Status VARCHAR(15));
CREATE TABLE Maintenance(MID SERIAL PRIMARY KEY, StartTime TIMESTAMP, EndTime TIMESTAMP, Status varchar(15), Notes VARCHAR(180), BID INTEGER REFERENCES Bike(BID), RequestedBy INTEGER REFERENCES Worker(WID), ServicedBy INTEGER REFERENCES Worker(WID));

CREATE TABLE DecommissionReq( DQID SERIAL PRIMARY KEY , RequestedBy INTEGER REFERENCES Users(UID), AnsweredBy INTEGER REFERENCES Admin(AID), Status VARCHAR(15),  BID INTEGER REFERENCES Bike(BID));
CREATE TABLE ServiceMaintenance(SMID SERIAL PRIMARY KEY, FName varchar(50), LName varchar(50), Bike varchar(50), Service varchar(100), Price REAL, WorkedBy INTEGER REFERENCES Worker(WID), WorkStatus varchar(15), Notes VARCHAR(180), STime TIMESTAMP, ETime TIMESTAMP);

ALTER TABLE Transactions DROP COLUMN BID;
ALTER TABLE Rental ADD COLUMN dueDate TIMESTAMP;
ALTER TABLE Rental DROP COLUMN TID;
/*
Create User
 */
INSERT INTO USERS( FName, LName, password, PNumber, Email) VALUES ('F', 'L', crypt('password', gen_salt('bf')), '5555555555', 'e@email.com') RETURNING uid;

/*
Create Admin, Create Worker, Client
 */
INSERT INTO Admin (UID )VALUES ((Select  UID FROM Users where Email = 'email@ree.com') );
INSERT INTO Client (UID )VALUES ((Select  UID FROM Users where Email = 'email@ree.com') );
INSERT INTO Worker (UID )VALUES ((Select  UID FROM Users where Email = 'email@ree.com') );

/*
Logins:
 */

SELECT email = 'email@ree.com'  AND password = crypt('UsersPassword', password) from Users;

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
UPDATE bike SET status = 'Reserved' WHERE BID in (SELECT bid from bike where status = 'Available' limit 1) returning bid;

/*
    Save Successful Transaction and create rental object
 */
INSERT INTO transactions(stamp, token, cid, status) VALUES (now(), 'token', 1, 'Completed') returning TID;
INSERT INTO rental(stime, client, dueDate) VALUES (now(), CID,now() +8 ) RETURNING RID;
INSERT INTO RentLink(RID, TID) VALUES (RID, TID);

/*
   Update Rental Upon Dispatch
 */


  /*
  Find Rental to be Updated
   */
  UPDATE Rental set DispatchedBy = 'WorkerOnTurn' where RID = 'ridGiven';

/*
Find bike scanned
 */
SELECT BID, Status FROM bike WHERE RFID =  'RFIDScanned' or LP = 'LPGiven';

/*
If Status = 'Available' reserve bike and release 1 reserved bike
 */
UPDATE bike set Status = 'Rented' where BID = 'bidGiven';
UPDATE Bike set Status = 'Available' where bid = (SELECT BID from bike where Status= 'Reserved' LIMIT 1);
 /*
 If Status = Reserved update to rented
  */
 UPDATE Bike SET Status = 'Rented' where BID = 'bidGiven';

/*
Update Rental by inserting final bike dispatched
 */
UPDATE rental SET BID = 'bidGiven' where RID = 'ridGiven';


/*
   Update Upon Rental Return
 */

 UPDATE Rental set ETime = now(), RecivedBy = 'WorkerOnStation' where RID = (SELECT rid from bike inner join Rental ON Bike.BID = Rental.BID AND RFID = 'rfidScanned' and RecivedBy isnull );

/*
Create ServiceMaintenance
 */

 INSERT INTO ServiceMaintenance(fname, lname, bike, service, price, workstatus, notes, stime ) VALUES ('fNAme', 'lName', 'bike', 'service', 5, 'StandBy', 'notes', now());

/*
Checkout ServiceMaintenance
 */

 UPDATE ServiceMaintenance set WorkedBy = 'Worker on turn', WorkStatus='Done', ETime = now() where SMID ='smidGiven'; 

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

 INSERT INTO Maintenance(starttime, status, notes, bid, requestedby) VALUES (now(), 'Pending', 'Notes', 'bidGiven', 'requestor');

/*
Update MaintenanceRequest
 */

 update Maintenance set servicedby = 'Server', EndTime= now() where MID = 'midGiven';