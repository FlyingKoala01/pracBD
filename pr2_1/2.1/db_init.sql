PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS parking_spot (
    spot_number INT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS car (
    license_plate VARCHAR(10) PRIMARY KEY,
    color VARCHAR(20),
    brand VARCHAR(20),
    arrival_time DATETIME
);

CREATE TABLE IF NOT EXISTS parking_history (
    license_plate VARCHAR(10) PRIMARY KEY,
    space_number INT,
    arrival_time DATETIME,
    departure_time DATETIME,
    duration_minutes INT,
    FOREIGN KEY (space_number) REFERENCES parking_spot(space_number),
    FOREIGN KEY (license_plate) REFERENCES car(license_plate)
);

UPDATE parking
