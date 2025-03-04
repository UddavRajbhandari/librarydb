-- Create the database
CREATE DATABASE LibraryDB;
GO

USE LibraryDB;
GO

-- Create the Books table
CREATE TABLE Books (
    BookID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Author NVARCHAR(255) NOT NULL,
    Genre NVARCHAR(100) NOT NULL,   
    PublishedYear INT,
    Category NVARCHAR(100),
    Quantity INT CHECK (Quantity >= 0)
);

-- Create the Members table
CREATE TABLE Members (
    MemberID INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(255) NOT NULL,
    Email NVARCHAR(255) UNIQUE NOT NULL,
    Phone NVARCHAR(15),
    Address NVARCHAR(255),
    MembershipDate DATE DEFAULT GETDATE()
);

-- Create the Transactions table
CREATE TABLE Transactions (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    MemberID INT,
    BookID INT,
    IssueDate DATE DEFAULT GETDATE(),
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    Status NVARCHAR(50) DEFAULT 'Issued',
    CONSTRAINT FK_Transactions_Members FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    CONSTRAINT FK_Transactions_Books FOREIGN KEY (BookID) REFERENCES Books(BookID)
);

-- Create the Users table (for authentication in the UI)
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) UNIQUE NOT NULL,
    PasswordHash NVARCHAR(255) NOT NULL,
    Role NVARCHAR(50) CHECK (Role IN ('Admin', 'Librarian', 'Member'))
);
drop table Books
drop table Members
drop table Transactions
drop table Users

-- Insert 30 sample members into the Members table
INSERT INTO Members (FullName, Email, Phone, Address, MembershipDate) VALUES
('Alice Johnson', 'alice@example.com', '1234567890', '123 Main St', '2022-01-15'),
('Bob Smith', 'bob@example.com', '9876543210', '456 Elm St', '2021-12-10'),
('Charlie Brown', 'charlie@example.com', '1112223333', '789 Oak St', '2023-03-22'),
('David Lee', 'david@example.com', '5554443333', '101 Maple St', '2022-05-13'),
('Emily Davis', 'emily@example.com', '2223334444', '202 Birch St', '2022-11-01'),
('Frank White', 'frank@example.com', '3334445555', '303 Pine St', '2023-07-18'),
('Grace Clark', 'grace@example.com', '4445556666', '404 Cedar St', '2022-09-25'),
('Hannah Lewis', 'hannah@example.com', '5556667777', '505 Redwood St', '2021-08-30'),
('Isaac Walker', 'isaac@example.com', '6667778888', '606 Sequoia St', '2023-02-12'),
('Jack Scott', 'jack@example.com', '7778889999', '707 Birchwood St', '2021-10-07'),
('Kara Young', 'kara@example.com', '8889990000', '808 Chestnut St', '2023-05-16'),
('Liam King', 'liam@example.com', '9990001111', '909 Spruce St', '2023-09-03'),
('Mia Harris', 'mia@example.com', '0001112222', '1010 Willow St', '2022-12-19'),
('Noah Turner', 'noah@example.com', '1112223333', '1111 Ash St', '2021-07-04'),
('Olivia Martinez', 'olivia@example.com', '2223334444', '1212 Fir St', '2023-04-25'),
('Paul Rodriguez', 'paul@example.com', '3334445555', '1313 Maplewood St', '2022-02-28'),
('Quinn Lee', 'quinn@example.com', '4445556666', '1414 Sycamore St', '2023-08-21'),
('Rachel Green', 'rachel@example.com', '5556667777', '1515 Larch St', '2021-09-15'),
('Samuel Adams', 'samuel@example.com', '6667778888', '1616 Cedarwood St', '2022-06-11'),
('Tina Clark', 'tina@example.com', '7778889999', '1717 Elmwood St', '2023-01-09'),
('Ursula White', 'ursula@example.com', '8889990000', '1818 Chestnutwood St', '2022-04-06'),
('Victor Kim', 'victor@example.com', '9990001111', '1919 Oakwood St', '2021-11-17'),
('Wendy Johnson', 'wendy@example.com', '0001112222', '2020 Willowwood St', '2023-06-27'),
('Xander Wright', 'xander@example.com', '1112223333', '2121 Pinewood St', '2022-03-15'),
('Yasmine Bell', 'yasmine@example.com', '2223334444', '2222 Birchwood St', '2023-12-10'),
('Zane Parker', 'zane@example.com', '3334445555', '2323 Firwood St', '2021-05-20'),
('Aaron Brooks', 'aaron@example.com', '4445556666', '2424 Maplewood St', '2023-10-14'),
('Bella James', 'bella@example.com', '5556667777', '2525 Sequoiawood St', '2022-08-22'),
('Carlos Sanchez', 'carlos@example.com', '6667778888', '2626 Oakwood St', '2023-11-02'),
('Diana Foster', 'diana@example.com', '7778889999', '2727 Redwoodwood St', '2021-04-10'),
('Eva Peterson', 'eva@example.com', '8889990000', '2828 Cedarwood St', '2024-02-20'),
('Zara Woods', 'zara@example.com', '5556667777', '789 Pine St', '2024-02-20');



-- Insert 150 sample data into Books
INSERT INTO Books (Title, Author, Genre, PublishedYear, Category, Quantity) VALUES
('Tonight much.', 'Scott Smith', 'Fiction', 1981, 'Education', 4),
('Right parent.', 'Joshua Singleton', 'Non-Fiction', 1904, 'Fiction', 2),
('Never exactly study same.', 'Brenda Roberts', 'Biography', 1987, 'Education', 4),
('Meet check conference.', 'Janice Smith', 'Fiction', 1927, 'Fiction', 5),
('Politics sense.', 'Monica Potts', 'Politics', 2017, 'Fiction', 8),
('City size.', 'Jasmine Kent', 'Technology', 1950, 'Technology', 10),
('Maybe kind.', 'Laura Russell', 'History', 2008, 'History', 4),
('Artist company newspaper company.', 'Nathaniel Harris', 'Business', 1994, 'Technology', 8),
('Realize design administration.', 'Jody Gregory', 'Management', 2013, 'History', 9),
('Will figure.', 'Kimberly Molina', 'Self-Help', 1968, 'Education', 10),
('Staff decide share.', 'Gregory Schneider', 'Fiction', 1980, 'Fiction', 2),
('Find never participant.', 'Angelica Henderson', 'Science', 1973, 'Science', 10),
('Avoid paper.', 'Alexander Ellis', 'Technology', 2007, 'Technology', 7),
('Service.', 'Casey Rosario', 'Health', 2015, 'History', 3),
('Common specific him.', 'Daniel Miller', 'History', 1946, 'History', 8),
('Trouble live for.', 'Seth Myers', 'Comedy', 1992, 'Education', 1),
('Cell loss ten.', 'Mr. Ryan Smith', 'Fiction', 1978, 'Fiction', 7),
('Election least surface.', 'Kristy Lopez', 'Political Science', 1989, 'Technology', 5),
('Throw serve.', 'Kayla Hill', 'Sports', 2010, 'History', 10),
('Operation reality.', 'Thomas Carey', 'History', 1959, 'History', 7),
('Character conference hotel.', 'Amanda Smith', 'Science', 1940, 'Science', 2),
('Catch answer security.', 'Kevin Arnold', 'Law', 1914, 'History', 6),
('Through method next.', 'Micheal Castaneda', 'Technology', 1926, 'Science', 4),
('Turn.', 'Cathy Guzman', 'Fiction', 1952, 'Technology', 6),
('Billion miss gun.', 'Travis Small', 'Technology', 1976, 'Technology', 3),
('Ball cover.', 'Molly Scott', 'History', 1959, 'History', 4),
('Television mouth decide.', 'Vicki Crane', 'Drama', 1964, 'Fiction', 9),
('Available while.', 'Abigail Higgins', 'Fiction', 1935, 'Fiction', 3),
('Meet short.', 'Jeffery Nelson', 'Fiction', 1941, 'Education', 7),
('Because career seem.', 'Kelly Jones', 'Self-Help', 1954, 'Education', 10),
('Low eye bar.', 'Matthew Burton', 'History', 2001, 'Education', 10),
('And real.', 'Thomas Patrick', 'Fiction', 1947, 'Education', 8),
('Bring kid.', 'Heidi Brown', 'Biography', 1901, 'History', 9),
('Language.', 'Jason Johns', 'Education', 1940, 'Technology', 8),
('Government art.', 'Gregory Smith', 'Government', 1990, 'History', 1),
('Chair military else.', 'Amy Gomez', 'Politics', 1953, 'Technology', 4),
('Bank field.', 'Hector Lee', 'Economics', 1987, 'History', 2),
('Expert exist.', 'Jody Hernandez', 'Technology', 2019, 'Technology', 7),
('Leg evening.', 'William Marshall', 'Science', 2020, 'Science', 2),
('Perform others.', 'Devin Murillo', 'Education', 1968, 'Education', 4),
('Would thousand.', 'Carlos Garza', 'Science', 1929, 'Science', 10),
('Next store.', 'Matthew Miller', 'Business', 1975, 'Education', 3),
('Time air.', 'John Hall', 'Science', 2010, 'Science', 6),
('Like memory.', 'Mrs. Melissa Williams', 'Fiction', 1936, 'Education', 5),
('Personal challenge shake.', 'Katherine Taylor', 'Health', 1985, 'Technology', 2),
('Beautiful station.', 'Samuel Hall', 'Fiction', 1968, 'History', 1),
('Perform claim house.', 'Ruth Miller', 'Health', 1978, 'Science', 7),
('Pay yeah seven.', 'Laura Hodge', 'Technology', 1923, 'Technology', 4),
('Recently various.', 'Miss Danielle Morgan MD', 'Health', 1917, 'History', 5),
('Fund education.', 'Diane Cole', 'Education', 1909, 'Technology', 4),
('Myself dark.', 'Steven Thompson', 'Fiction', 1900, 'History', 3),
('Tend management.', 'Sandra Walter', 'Management', 1911, 'History', 3),
('Attack occur security.', 'Stephanie Cox', 'Security', 1967, 'Technology', 8),
('Easy scene eye.', 'Richard Henry', 'Fiction', 1917, 'Technology', 5),
('Smile prove.', 'Richard Noble', 'Science', 1918, 'Science', 6),
('For manage.', 'Shane Thomas', 'Fiction', 1930, 'Fiction', 5),
('Fact industry.', 'Jill Byrd', 'Economics', 2017, 'Education', 2),
('Dark however skill less.', 'Aaron Ramirez', 'Technology', 1964, 'Education', 1),
('Around policy stop note.', 'Stacey Estrada', 'Fiction', 1958, 'Fiction', 10),
('Scientist enjoy success.', 'Jessica Norris', 'Science', 1969, 'Science', 1),
('Space current.', 'Thomas Rogers', 'Fiction', 1951, 'Fiction', 2),
('Instead must partner.', 'Jenny Gomez', 'History', 1931, 'History', 3),
('Politics white.', 'Lydia Anderson', 'Politics', 1960, 'Education', 5),
('Though trip radio.', 'Kimberly Kelly', 'Fiction', 2002, 'History', 4),
('Matter camera environmental.', 'Michelle Dunn', 'Environment', 2020, 'History', 10),
('Near act.', 'Christian Craig', 'Fiction', 1958, 'Education', 10),
('Interesting job.', 'Lisa Forbes', 'Business', 1991, 'Education', 7),
('Which write others.', 'Kristen Ramirez', 'Fiction', 1943, 'Fiction', 1),
('Wall fact claim remain.', 'Nathan Allen', 'Politics', 1910, 'Technology', 6),
('Couple by.', 'Kelly Horn', 'Fiction', 1904, 'Education', 9),
('Fire natural go.', 'Christopher Shea', 'Science', 2021, 'Fiction', 5),
('Twist close.', 'Sam Walters', 'Fiction', 1999, 'History', 5),
('Digital paper.', 'Lola Richards', 'Technology', 2006, 'Fiction', 9),
('Turn section.', 'Patricia Matthews', 'Fiction', 1992, 'Business', 4),
('Tough set.', 'Steven Alexander', 'Fiction', 1988, 'Education', 6),
('Final movement.', 'Harry Jackson', 'Non-Fiction', 1995, 'Science', 7),
('Winter notes.', 'Benjamin Fisher', 'Fiction', 2012, 'Technology', 3),
('Information chart.', 'Megan Clark', 'History', 1994, 'Science', 6),
('Principle study.', 'Edward Rogers', 'Fiction', 2003, 'Business', 7),
('Test questions.', 'Sally Peters', 'Management', 2018, 'Education', 8),
('Pressure current.', 'Laura Green', 'Self-Help', 2001, 'Technology', 4),
('Office meeting.', 'Brian Collins', 'Fiction', 2005, 'Fiction', 7),
('Change information.', 'Jenna Powell', 'Fiction', 1998, 'Technology', 8),
('Wind speed.', 'Nancy Harris', 'Technology', 1990, 'Science', 5),
('Tidy tools.', 'David Jenkins', 'Science', 1993, 'Fiction', 4),
('Energy rush.', 'Debra Long', 'Fiction', 2007, 'Science', 10),
('Believe project.', 'Barbara Moore', 'Fiction', 2015, 'Education', 8),
('Pass skill.', 'Catherine Hill', 'Non-Fiction', 1989, 'History', 5),
('Lead touch.', 'Erica Rivera', 'Fiction', 1996, 'Science', 3),
('Result labor.', 'Douglas Wells', 'Fiction', 2010, 'Technology', 4),
('Outdoor action.', 'Diane Fields', 'Sports', 1998, 'Sports', 6),
('Recall energy.', 'Mary Phillips', 'Technology', 2005, 'Science', 2),
('Find command.', 'Emma Bell', 'Fiction', 1990, 'Technology', 8),
('Remote break.', 'Luke Robinson', 'Fiction', 2014, 'History', 1),
('Define country.', 'Hannah Daniels', 'History', 1987, 'Education', 5),
('Store memory.', 'Cynthia Adams', 'Technology', 2003, 'Technology', 4),
('Clear ground.', 'Oliver White', 'Business', 2019, 'Business', 9),
('Revolution state.', 'Kevin King', 'Political Science', 1991, 'Politics', 2),
('Location find.', 'Debbie Fox', 'Fiction', 2006, 'Fiction', 7),
('Speed line.', 'Fred Armstrong', 'Science', 2000, 'Fiction', 5),
('Simple divide.', 'Cheryl Harris', 'Fiction', 2011, 'History', 9),
('Increase week.', 'Daniel Hughes', 'Technology', 2004, 'Fiction', 8),
('Hold success.', 'Beatrice Daniels', 'History', 1986, 'Science', 6),
('Flat interesting.', 'Joan Patterson', 'Fiction', 2009, 'Education', 3),
('Alternative chance.', 'Pamela Cooper', 'Fiction', 1999, 'Fiction', 8),
('Prevent challenge.', 'Gloria Martinez', 'Self-Help', 1994, 'Education', 7),
('Pathing stage.', 'Cindy Sanchez', 'Fiction', 2003, 'Business', 7),
('Line context.', 'Ashley Scott', 'Fiction', 2018, 'Business', 9),
('Award idea.', 'Benjamin Morris', 'Fiction', 1982, 'Science', 8),
('After exam.', 'Paula Russell', 'History', 2000, 'Science', 6),
('Plant strategy.', 'Mary Fisher', 'Fiction', 2008, 'History', 5),
('Time action.', 'Evelyn Jenkins', 'Technology', 1997, 'Fiction', 6),
('Factor test.', 'Peter Reed', 'Fiction', 2007, 'Education', 4),
('Total piece.', 'William Bell', 'Technology', 1993, 'Fiction', 3),
('Larger country.', 'Nancy Brooks', 'Fiction', 2001, 'Business', 7),
('Economics analyze.', 'Sophia Robinson', 'Economics', 2012, 'Technology', 8);


-- Insert 30 sample transactions into the Transactions table
INSERT INTO Transactions (MemberID, BookID, IssueDate, DueDate, ReturnDate, Status) VALUES
(1, 1, '2025-02-25', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(2, 2, '2025-02-26', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(3, 3, '2025-02-27', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(4, 4, '2025-02-28', DATEADD(DAY, 14, GETDATE()), '2025-03-10', 'Returned'),
(5, 5, '2025-02-20', DATEADD(DAY, 14, GETDATE()), '2025-03-05', 'Returned'),
(6, 6, '2025-02-21', DATEADD(DAY, 14, GETDATE()), NULL, 'Overdue'),
(7, 7, '2025-02-22', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(8, 8, '2025-02-23', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(9, 9, '2025-02-24', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(10, 10, '2025-02-19', DATEADD(DAY, 14, GETDATE()), '2025-03-03', 'Returned'),
(11, 11, '2025-02-20', DATEADD(DAY, 14, GETDATE()), NULL, 'Overdue'),
(12, 12, '2025-02-21', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(13, 13, '2025-02-22', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(14, 14, '2025-02-23', DATEADD(DAY, 14, GETDATE()), '2025-03-08', 'Returned'),
(15, 15, '2025-02-24', DATEADD(DAY, 14, GETDATE()), '2025-03-09', 'Returned'),
(16, 16, '2025-02-19', DATEADD(DAY, 14, GETDATE()), NULL, 'Overdue'),
(17, 17, '2025-02-20', DATEADD(DAY, 14, GETDATE()), '2025-03-04', 'Returned'),
(18, 18, '2025-02-21', DATEADD(DAY, 14, GETDATE()), '2025-03-06', 'Returned'),
(19, 19, '2025-02-22', DATEADD(DAY, 14, GETDATE()), '2025-03-07', 'Returned'),
(20, 20, '2025-02-23', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(21, 21, '2025-02-24', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(22, 22, '2025-02-19', DATEADD(DAY, 14, GETDATE()), NULL, 'Overdue'),
(23, 23, '2025-02-20', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(24, 24, '2025-02-21', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(25, 25, '2025-02-22', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(26, 26, '2025-02-23', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(27, 27, '2025-02-24', DATEADD(DAY, 14, GETDATE()), NULL, 'Issued'),
(28, 28, '2025-02-19', DATEADD(DAY, 14, GETDATE()), '2025-03-04', 'Returned'),
(29, 29, '2025-02-20', DATEADD(DAY, 14, GETDATE()), NULL, 'Reserved'),
(30, 30, '2025-02-21', DATEADD(DAY, 14, GETDATE()), '2025-03-06', 'Returned');




-- Insert 20 sample users into the Users table
INSERT INTO Users (Username, PasswordHash, Role) VALUES
('Alice Johnson', 'password1', 'Member'),
('Bob Smith', 'password2', 'Member'),
('Charlie Brown', 'password3', 'Member'),
('David Lee', 'password4', 'Member'),
('Eva Martinez', 'password5', 'Member'),
('Frank White', 'password6', 'Member'),
('Grace Green', 'password7', 'Member'),
('Hannah Clark', 'password8', 'Member'),
('Ian Wilson', 'password9', 'Member'),
('Jack Turner', 'password10', 'Member'),
('Karen Adams', 'password11', 'Member'),
('Liam Scott', 'password12', 'Member'),
('Mia Cooper', 'password13', 'Member'),
('Nathan Brooks', 'password14', 'Member'),
('Olivia Allen', 'password15', 'Member'),
('Paul Harris', 'password16', 'Member'),
('Quinn Evans', 'password17', 'Member'),
('Rita Young', 'password18', 'Member'),
('Sarah King', 'password19', 'Member'),
('admin1', 'adminpass', 'Admin');

select * from books;
select * from members;
select * from users;

-- Query to check all transactions
SELECT * FROM Transactions;