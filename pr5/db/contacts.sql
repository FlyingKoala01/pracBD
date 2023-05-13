PRAGMA foreign_keys=ON;

-- Create the table
CREATE TABLE contacts (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  phone_number TEXT NOT NULL
);

-- Insert sample data
INSERT INTO contacts (name, phone_number) VALUES ('Alice', '555-1234');
INSERT INTO contacts (name, phone_number) VALUES ('Bob', '555-5678');
INSERT INTO contacts (name, phone_number) VALUES ('Charlie', '555-9012');
INSERT INTO contacts (name, phone_number) VALUES ('David', '555-3456');
INSERT INTO contacts (name, phone_number) VALUES ('Emily', '555-7890');
INSERT INTO contacts (name, phone_number) VALUES ('Frank', '555-2345');
INSERT INTO contacts (name, phone_number) VALUES ('Grace', '555-6789');
INSERT INTO contacts (name, phone_number) VALUES ('Harry', '555-0123');
INSERT INTO contacts (name, phone_number) VALUES ('Isabelle', '555-4567');
INSERT INTO contacts (name, phone_number) VALUES ('Jacob', '555-8901');
