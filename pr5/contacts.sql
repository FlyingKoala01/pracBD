PRAGMA foreign_keys=ON;

-- Create the table
CREATE TABLE contacts (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  filename TEXT
);

-- Insert sample data
INSERT INTO contacts (name, phone_number, filename) VALUES ('Alice', '938720000', 'upc.png');
INSERT INTO contacts (name, phone_number) VALUES ('Alice', '666666666');
INSERT INTO contacts (name, phone_number) VALUES ('Bob', '938720000');
INSERT INTO contacts (name, phone_number) VALUES ('Charlie', '938720001');
INSERT INTO contacts (name, phone_number) VALUES ('David', '938720002');
INSERT INTO contacts (name, phone_number) VALUES ('Emily', '938720003');
INSERT INTO contacts (name, phone_number) VALUES ('Frank', '938720004');
INSERT INTO contacts (name, phone_number) VALUES ('Grace', '938720005');
INSERT INTO contacts (name, phone_number) VALUES ('Harry', '938720006');
INSERT INTO contacts (name, phone_number) VALUES ('Isabelle', '938720007');
INSERT INTO contacts (name, phone_number) VALUES ('Jacob', '938720008');
