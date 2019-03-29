/*
Create Table Statements

 */
CREATE TABLE Users(UID SERIAL PRIMARY KEY, FName VARCHAR(50), LName VARCHAR(50), password TEXT, PNumber smallint, Email VARCHAR(100) UNIQUE);
CREATE TABLE Client(CID SERIAL PRIMARY KEY , UID INTEGER REFERENCES Users(UID));
CREATE TABLE Worker(WID SERIAL PRIMARY KEY, UID INTEGER REFERENCES Users(UID), Status VARCHAR(15));
CREATE TABLE Admin(AID SERIAL PRIMARY KEY, UID INTEGER REFERENCES Users(UID));

CREATE TABLE Bike(BID Serial PRIMARY KEY, LP VARCHAR(15), RFID VARCHAR(50), Status varchar(15), brand TEXT, model TEXT);

CREATE TABLE Rental(RID serial PRIMARY KEY, STime TIMESTAMP, ETime TIMESTAMP, Client INTEGER REFERENCES Client (CID), BID INTEGER REFERENCES Bike(BID), DispatchedBy INTEGER REFERENCES Worker(WID), RecivedBy INTEGER REFERENCES Worker(WID), TID INTEGER REFERENCES Transactions(TID));
CREATE TABLE Transactions(TID SERIAL PRIMARY KEY, stamp timestamp, Token varchar(50), CID INTEGER REFERENCES Client(CID), BID INTEGER REFERENCES Bike(BID), Status VARCHAR(15));
CREATE TABLE TransLink (TID INTEGER REFERENCES Transactions(TID), BID INTEGER REFERENCES Bike(BID), PRIMARY KEY(TID, BID));
CREATE TABLE Maintenance(MID SERIAL PRIMARY KEY, StartTime TIMESTAMP, EndTime TIMESTAMP, Status varchar(15), Notes VARCHAR(180), BID INTEGER REFERENCES Bike(BID), RequestedBy INTEGER REFERENCES Worker(WID), ServicedBy INTEGER REFERENCES Worker(WID));

CREATE TABLE DecommissionReq( DQID SERIAL PRIMARY KEY , RequestedBy INTEGER REFERENCES Users(UID), AnsweredBy INTEGER REFERENCES Admin(AID), Status VARCHAR(15),  BID INTEGER REFERENCES Bike(BID));
CREATE TABLE ServiceMaintenance(SMID SERIAL PRIMARY KEY, FName varchar(50), LName varchar(50), Bike varchar(50), Service varchar(100), Price REAL, WorkedBy INTEGER REFERENCES Worker(WID), WorkStatus varchar(15), Notes VARCHAR(180), STime TIMESTAMP, ETime TIMESTAMP);



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
    Save Successful Transaction
 */
INSERT INTO transactions(stamp, token, cid, status, bid) VALUES (now(), 'token', 1, 'Completed', 1) returning TID;

/*
    Create Rental Upon Successful Transaction
 */
 INSERT INTO rental(stime, client, bid, tid) VALUES (now(), CID,WID, BID, tid) RETURNING RID;

/*
   Update Rental Upon Dispatch
 */

UPDATE rental SET dispatchedby = 'WorkerDispatching' where (SELECT BID FROM bike natural inner join Rental where rfid = 'RFIDScanned' and Rental.RID = RID);
UPDATE Bike SET Status = 'Rented' where rfid = 'RFIDScanned';