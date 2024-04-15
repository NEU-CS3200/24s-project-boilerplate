CREATE DATABASE Scheduling;

USE Scheduling;


CREATE TABLE Users (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(50),
    hourlyRate FLOAT(2), # In dollars
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    sharesOwned INTEGER DEFAULT 0, # Ownership percentage
    active BOOLEAN DEFAULT TRUE # If they're still employed
);

CREATE TABLE UserManagers (
    employee INTEGER,
    manager INTEGER,
    PRIMARY KEY (employee, manager),
    CONSTRAINT employeeKey FOREIGN KEY (employee)
        REFERENCES Users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT managerKey FOREIGN KEY (manager)
        REFERENCES Users (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Locations (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    address1 VARCHAR(100) NOT NULL, # Line 1
    address2 VARCHAR(100), # Line 2 (optional)
    city  VARCHAR(50),
    state CHAR(2), # State abbreviation
    zip CHAR(5), # Should be numeric
    owner INTEGER,
    CONSTRAINT ownedBy FOREIGN KEY (owner)
        REFERENCES Users (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Schedules ( # Why does this table exist?
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    location INTEGER NOT NULL,
    CONSTRAINT locatedAt FOREIGN KEY (location)
        REFERENCES Locations (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE TimeOffRequests (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    reason TEXT,
    paid BOOLEAN DEFAULT FALSE,
    submitDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    createdBy INTEGER,
    approved BOOLEAN,
    viewedBy INTEGER,
    schedule INTEGER,
    CONSTRAINT creator FOREIGN KEY (createdBy)
        REFERENCES Users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT viewer FOREIGN KEY (viewedBy)
        REFERENCES Users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT scheduleKey FOREIGN KEY (schedule)
        REFERENCES Schedules (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

# Multivalued attribute Times of TimeOffRequests
CREATE TABLE Times (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    startDate DATETIME NOT NULL,
    endDate DATETIME NOT NULL, # Should be after startDate
    request INTEGER,
    CONSTRAINT requestKey FOREIGN KEY (request)
        REFERENCES TimeOffRequests (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Shifts (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    duty VARCHAR(50),
    dayOfWeek INTEGER, # 0 = Monday, 6 = Sunday
    startTime TIME,
    endTime TIME, # Should be after startTime
    overtime BOOLEAN DEFAULT FALSE,
    employee INTEGER,
    schedule INTEGER,
    CONSTRAINT workedBy FOREIGN KEY (employee)
        REFERENCES Users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT scheduledAt FOREIGN KEY (schedule)
        REFERENCES Schedules (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Tasks (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    assignedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    dueDate DATETIME,
    type VARCHAR(100),
    description TEXT,
    submitted BOOLEAN DEFAULT FALSE,
    user INTEGER NOT NULL,
    CONSTRAINT student FOREIGN KEY (user)
        REFERENCES Users (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);