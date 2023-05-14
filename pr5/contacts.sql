PRAGMA foreign_keys=ON;

-- Create the table
CREATE TABLE contacts (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  filename TEXT
);

-- Insert sample data
INSERT INTO contacts (name, phone_number, filename) VALUES ('Alice', '938720000', 'alice.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Alice', '666666666', 'alice.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Bob', '938720000', 'bob.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Charlie', '938720001', 'charlie.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('David', '938720002', 'david.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Emily', '938720003', 'emily.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Frank', '938720004', 'frank.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Grace', '938720005', 'grace.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Harry', '938720006', 'harry.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Isabelle', '938720007', 'isabelle.png');
INSERT INTO contacts (name, phone_number, filename) VALUES ('Jacob', '938720008', 'jacob.png');
