-- Prac2ex1

PRAGMA foreign_keys=ON;

-- Tables
CREATE TABLE IF NOT EXISTS parking_spot (
    spot_number INT PRIMARY KEY,
    car_license_plate VARCHAR(10),
    FOREIGN KEY (car_license_plate) REFERENCES car(license_plate)
);

CREATE TABLE IF NOT EXISTS car (
    license_plate VARCHAR(10) PRIMARY KEY,
    color VARCHAR(20),
    brand VARCHAR(20),
    arrival_time DATETIME
);

-- Test data
INSERT INTO car VALUES 
('ABC123', 'Red', 'Toyota', datetime('now', '-1 hours')),
('DEF456', 'Blue', 'Ford', datetime('now', '-2 hours')),
('GHI789', 'Black', 'Honda', datetime('now', '-3 hours'));

INSERT INTO parking_spot VALUES 
(1, 'ABC123'),
(2, 'DEF456'),
(3, NULL),
(4, NULL),
(5, 'GHI789');


-- Uncomment to check that foreign keys work (because of PRAGMA in line 1)
-- INSERT INTO parking_spot VALUES (6, 'XYZ987');

-- Uncomment to check that primary keys must be unique
-- INSERT INTO car VALUES ('ABC123', 'Green', 'Honda', DATETIME('now'));

-- Inserting a car just now
INSERT INTO car VALUES ('JKL012', 'Yellow', 'Tesla', DATETIME('now'));
UPDATE parking_spot SET car_license_plate = 'JKL012' WHERE spot_number = 4;

-- To calculate the amount of money a car needs to pay (supose 0.02€/minute)
SELECT 
    license_plate, arrival_time,
    strftime('%s', 'now') - strftime('%s', arrival_time) AS duration_seconds,
    (strftime('%s', 'now') - strftime('%s', arrival_time)) / 60.0 AS duration_minutes,
    (strftime('%s', 'now') - strftime('%s', arrival_time)) / 60.0 * 0.02 AS price
FROM car;

-- Empty spaces
SELECT spot_number
FROM parking_spot
WHERE car_license_plate IS NULL;

-- Full spaces (with license plate)
SELECT spot_number, car_license_plate
FROM parking_spot
WHERE car_license_plate IS NOT NULL;
