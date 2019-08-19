/*
INTRODUCTION TO SQLITE3 for the Political Science Python Summer Short Course
By: Ryden Butler

The following .sql script is intended to interactively demonstrate some simple operations in SQL.
Though all of the code here is run in SQLite3 (the most widely used SQL, as well as the language immediately accessible on Macs),
  numerous other SQL variants exist. Each has its own idiosyncracies in terms of table structure and functionality, but the language, 
  logic, and operations remain fairly consistent across variant (as far as I can tell).

For more information on getting started in SQL see the following links (ranked in order of usefulness):

http://www.sqlitetutorial.net/   ~ This resource has extensive explanations and examples of SQLite code, including tutorials on the SQLite Python API
http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html    ~ This resource offers more in-depth explanations for working in SQLite via Python
https://www.codecademy.com/learn/learn-sql     ~ Code Academy offers some simple introductory lessons to SQL if you find the following .sql script too brief

P.S. This slash-star combination allows you to comment over multiple lines. Begin the comment with a star-slash and end it with a slash-star
*/

-- Create a basic table to store data.
-- Note that this format is a BAD way to store our data. It is, however, useful for illustrating some operations... 
CREATE TABLE IF NOT EXISTS PresidentVotes ( -- This creates a table, with the given name, providing one does not already exist. This is a safer way to create tables
Candidate TEXT, -- Name each column of your table and specify the type of data it contains
Homestate TEXT,
NominationParty TEXT,
SelfParty TEXT,
Gender NOT NULL, -- You can be lazy and specify any type (except for NULL) with NOT NULL. However the more structure you add upfront, the more stability you get in the long-run
PreviousGovExp NOT NULL,
Year NOT NULL,
Votes INTEGER, -- Types also include integers
NHPrimary BOOLEAN -- and boolean values, which are stored as special cases of integers\
-- For more on SQL data types, see http://www.cs.toronto.edu/~nn/csc309/guide/pointbase/docs/html/htmlfiles/dev_datatypesandconversionsFIN.html
);

-- Check our current table with the following
.tables
-- This is called a "command" (not to be confused with a "function"). 
-- It can operate on tables and/or the database as a whole without explicily accessing data

-- We can see the schema of our table with
.schema 'PresidentVotes'
-- Or to see all of our tables' schemas
.fullschema
-- As we will see, commands are also useful for opening/saving data as well as quitting SQLite

-- We can also use a PRAGMA statement. These are unique to SQLite, and are convenience functions similar to commands
PRAGMA table_info(PresidentVotes);
-- For a full list of PRAGMA statements, see https://sqlite.org/pragma.html

-- Now insert some data into the table
INSERT OR IGNORE INTO PresidentVotes (Candidate, Homestate, NominationParty, SelfParty, Gender, PreviousGovExp, Year, Votes, NHPrimary)
VALUES ('Donald Trump', 'NY', 'R', '?', 'M', 0, 2016, 12345, 'TRUE');
-- Note a few features of this statement:
-- 1) Operations with the SQL statement are capitalized, but only by convention. SQLite is actually insensitive to case. 
-- This case-insensitivty applies to operations, tables, and columns
-- 2) We need not specify the column names, however this is much safer for data input, since adding values will put them in order of column creation by default
-- 3) We use the safer INSERT OR IGNORE in order to avoid problems of uniqueness. These only work when we have uniqueness constraints in place (see below)

-- Use a SELECT statement to inspect the table
SELECT * FROM PresidentVotes;

-- Without a uniqueness constraint, INSERT OR IGNORE is equivalent to INSERT. Try this. We'll delete it in a second
INSERT INTO PresidentVotes (Candidate, Homestate, NominationParty, SelfParty, Gender, PreviousGovExp, Year, Votes, NHPrimary)
VALUES ('Donald Trump', 'NY', 'R', '?', 'M', 0, 2016, 12345, 'TRUE');

-- Notice the repeat
SELECT * FROM PresidentVotes;

-- We can also insert multiple rows with a single insert statement
INSERT OR IGNORE INTO PresidentVotes (Candidate, Homestate, NominationParty, SelfParty, Gender, PreviousGovExp, Year, Votes, NHPrimary)
VALUES ('Donald Trump', 'NY', 'R', '?', 'M', 0, 2020, 7654, 'TRUE'),
('Donald Trump', 'NY', 'R', '?', 'M', 0, 2024, 321, 'FALSE'),
('Hillary Clinton', 'DC', 'D', 'D', 'F', 'Senate', 2016, 23456, 'FALSE'),
('Hillary Clinton', 'DC', 'D', 'D', 'F', 'SecState', 2016, 23456, 'FALSE'),
('Hillary Clinton', 'DC', 'D', 'D', 'F', 'FistLady', 2016, 23456, 'FALSE'),
('Hillary Clinton', 'DC', 'D', 'D', 'F', 'Senate', 2020, 34567, 'FALSE'),
('Hillary Clinton', 'DC', 'D', 'D', 'F', 'SecState', 2020, 34567, 'FALSE'),
('Hillary Clinton', 'DC', 'D', 'D', 'F', 'FirstLady', 20202020, 34567, 'FALSE'),
('Bernie Sanders', 'VT', 'D', 'I', 'M', 'HouseRep', 2024, 98765, 'TRUE'),
('Bernie Sanders', 'VT', 'D', 'I', 'M', 'Senate', 2024, 98765, 'TRUE'),
('Bernie Sanders', 'VT', 'D', 'I', 'M', 'Mayor', 2024, 98765, 'TRUE');

-- Notice the new rows
-- Also notice that we've made a mistake on one of the election years
SELECT * FROM PresidentVotes;

-- To fix the error, we can update the value of election year by referencing the errant year
UPDATE PresidentVotes
SET Year = 123456
WHERE Year = 20202020;

-- We've now changed the errant year to 123456
SELECT * FROM PresidentVotes;

-- We can also update values based on specific criteria
UPDATE PresidentVotes
SET Year = 2020
WHERE (Candidate, Year) = ('Hillary Clinton', 123456);

-- Or we can update based on row value
-- We get the column "rowid" for free in every table we create, so long as we don't specify a column called rowid, in which case it will be overwritten
UPDATE PresidentVotes
SET Year = 2028
WHERE rowid = 1;

-- We can see that Trump takes up the first few rows
SELECT rowid FROM PresidentVotes 
WHERE Candidate = 'Donald Trump';

-- We can also delete the first row, which is a duplicate
DELETE FROM PresidentVotes
WHERE rowid = 1;

-- Take a look at the table one last time to see all of the changes that have taken effect
-- Also note one important point: This resembles the kinds of R dataframes we typically work with.
-- We would store this as a 12 x 9 matrix (108 cells of data) in other contexts
SELECT * FROM PresidentVotes;




-- Now let's build a proper "relational" database to cut down on some redundancy 

-- First create a table to store only candidate information
CREATE TABLE IF NOT EXISTS Candidates (
Name UNIQUE, -- Note that we are constraining candidate name to be unique. Only 1 row is allowed per candidate
Homestate NOT NULL,
SelfParty NOT NULL,
Gender NOT NULL);

-- Next we create a table to store only election information
CREATE TABLE IF NOT EXISTS Elections (
Year UNIQUE, -- Here, year is unique. This is not the PRIMARY KEY, though we could specify it as such
WinnerName TEXT REFERENCES Candidates, -- The REFERENCES statement tells the table how it relates to others in the database
WinnerPartyNom TEXT,
WinnerVotes INT,
LoserName TEXT REFERENCES Candidates,
LoserPartyNom TEXT,
LoserVotes INT);

-- Finally create a table to store past government positions for each of the candidates
CREATE TABLE IF NOT EXISTS PastGovExp (
Name TEXT,
Position TEXT,
CONSTRAINT Name_Position UNIQUE (Name, Position), -- Here we constrain the table to only accept unique combination of candidate and position
FOREIGN KEY (Name) REFERENCES Candidates (Name)); -- We can also reference other tables after all columns are specified

-- Quickly insert all of our data into our re-structured tables
-- We've covered the INSERT OR IGNORE statement before, but if you're feeling particularly adventurous, try running these again.
-- Did anything change?
INSERT OR IGNORE INTO Elections (Year, WinnerName, WinnerPartyNom, WinnerVotes, LoserName, LoserPartyNom, LoserVotes)
VALUES (2016, 'Donald Trump', 'R', 12345, 'Hillary Clinton', 'D', 23456),
(2020, 'Donald Trump', 'R', 7654, 'Hillary Clinton', 'D', 34567),
(2024, 'Bernie Sanders', 'D', 98765, 'Donald Trump', 'R', 321);

INSERT OR IGNORE INTO Candidates (Name, Homestate, SelfParty, Gender)
VALUES ('Donald Trump', 'NY', '?', 'M'),
('Hillary Clinton', 'DC', 'D', 'F'),
('Bernie Sanders', 'VT', 'I', 'M');

INSERT OR IGNORE INTO PastGovExp (Name, Position)
VALUES ('Hillary Clinton', 'First Lady'),
('Hillary Clinton', 'Senator'),
('Hillary Clinton', 'Secretary of State'),
('Bernie Sanders', 'Mayor'),
('Bernie Sanders', 'House Member'),
('Bernie Sanders', 'Senator');

-- Take a look at your tables now
.tables

SELECT * FROM Candidates;
SELECT * FROM Elections;
SELECT * FROM PastGovExp;
-- We've reduced the amount of stored information from 108 stored values to (3x7 + 3x4 + 6x2) only 45 cells.
-- Which is only useful if we can get all that data back to run regression...

-- Meet the join statement:
SELECT * FROM Candidates
LEFT JOIN PastGovExp ON Candidates.Name = PastGovExp.Name;
-- The LEFT JOIN contains all of the information in the left table (after the FROM) and any overlapping content in the right tables(s)

-- We can also ORDER the returned data BY some value
SELECT Candidates.Name, Homestate, SelfParty, Gender, Position FROM Candidates -- This lets us specify which columns to return, whereas * returns all
LEFT JOIN PastGovExp ON Candidates.Name = PastGovExp.Name
ORDER BY Candidates.Name;

-- Or we can SELECT and JOIN tables WHERE data takes on a specific value of our choice
SELECT Candidates.Name, Homestate, SelfParty, Gender, Position FROM Candidates
LEFT JOIN PastGovExp ON Candidates.Name = PastGovExp.Name
WHERE Candidates.Name = 'Bernie Sanders';

-- We can also JOIN multiple tables
SELECT Candidates.Name, Homestate, SelfParty, Gender, Year, Position,
CASE -- CASE is like an if-then statement
WHEN Candidates.Name = Elections.WinnerName THEN Elections.WinnerVotes -- Specify the conditional THEN the return values
WHEN Candidates.Name = Elections.LoserName THEN Elections.LoserVotes
END,
CASE -- To return multiple values for a CASE, you must specify multiple CASE statements, that is, you cannot have multiple returns for a single conditional
WHEN Candidates.Name = Elections.WinnerName THEN Elections.WinnerPartyNom
ELSE Elections.LoserPartyNom -- You can also use ELSE. Here it's analogous to the WHEN ... THEN ... in the above CASE
END -- According to a StackOverflow user, SQL is smart enough to run these CASEs simultaneously even though they are coded sequentially
FROM Candidates
LEFT JOIN Elections ON Candidates.Name = Elections.WinnerName
OR Candidates.Name = Elections.LoserName -- AND & OR may also be used in SELECTs and JOINs to widen/narrow the returned values
LEFT JOIN PastGovExp ON Candidates.Name = PastGovExp.Name -- Finally we can simultaneously JOIN our third table
ORDER BY Year; -- And optionally order the data by election year

-- We can also do some easy SELECTs (and JOINs) by regular expressions
-- The % are wild cards for multiple characters
-- The _ is a wild card for a single character, though you can use multiple
SELECT * FROM Candidates WHERE Name LIKE 'Don%';
SELECT * FROM Candidates WHERE Name Like '%on%';
SELECT * FROM Candidates WHERE Name Like 'Donald %';
SELECT * FROM Candidates WHERE Name Like 'Donald _____'; -- 5 underscores

/*
There are many more statements that can be useful including:

SELECT DISTINCT
HAVING
IN
UNION
INNER / CROSS / SELF JOINS
REPLACE

You can also ALTER and DROP tables that need modification or deletion 
*/

-- Before we save and quit, let's test a few SQL functions
-- Do you know what these are doing?
SELECT COUNT(Position) FROM PastGovExp
WHERE Name = 'Hillary Clinton';

SELECT 
SUM(CASE 
WHEN WinnerName = 'Donald Trump' THEN WinnerVotes
WHEN LoserName = 'Donald Trump' THEN LoserVotes
END)
FROM Elections;

SELECT MIN(Year), MAX(Year) FROM Elections;
-- Also try AVG() and others
-- Note that SQL is generally limited in its functions, so it's important that ease of data processing should be baked into the table schemas



-- Finally let's save the data
-- Use the following commands to specify how sqlite3 should save the data
.headers on
.mode csv
.output data.csv

SELECT Candidates.Name, Homestate, SelfParty, Gender, Year, Position,
CASE 
WHEN Candidates.Name = Elections.WinnerName THEN Elections.WinnerVotes
WHEN Candidates.Name = Elections.LoserName THEN Elections.LoserVotes
END AS Votes, -- The AS statement allows us to name the result of the CASE
CASE
WHEN Candidates.Name = Elections.WinnerName THEN Elections.WinnerPartyNom
WHEN Candidates.Name = Elections.LoserName THEN Elections.LoserPartyNom
END AS PartyNomination
FROM Candidates
LEFT JOIN Elections ON Candidates.Name = Elections.WinnerName
OR Candidates.Name = Elections.LoserName
LEFT JOIN PastGovExp ON Candidates.Name = PastGovExp.Name
ORDER BY Year;

-- Finally we can quit sqlite3 with this command
.quit

