PRAGMA foreign_keys=ON;

CREATE TABLE employee (
    id_employee INT PRIMARY KEY,
    street TEXT,
    city TEXT NOT NULL
    );

CREATE TABLE job (
    id_employee INT PRIMARY KEY,
    id_company INT NOT NULL,
    salary FLOAT NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employee,
    FOREIGN KEY (id_company) REFERENCES company
    );

CREATE TABLE company (
    id_company INT PRIMARY KEY,
    city TEXT NOT NULL
    );

CREATE TABLE manager (
    id_employee INT PRIMARY KEY,
    id_employee_coordinator INT NOT NULL,
    FOREIGN KEY (id_employee) REFERENCES employee,
    FOREIGN KEY (id_employee_coordinator) REFERENCES employee
    );