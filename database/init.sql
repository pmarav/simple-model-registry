-- Create the database (already set in POSTGRES_DB, but just in case)
-- CREATE DATABASE modelmetadata;

-- Connect to the database
\c modelmetadata;

-- Create the table
CREATE TABLE models (
    name VARCHAR(255) PRIMARY KEY,
    version VARCHAR(50) NOT NULL,
    accuracy DECIMAL(7,5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the user
CREATE USER psqluser WITH ENCRYPTED PASSWORD 'psqluser123!';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE modelmetadata TO psqluser;
GRANT ALL PRIVILEGES ON TABLE models TO psqluser;
GRANT ALL ON SCHEMA public TO psqluser;
