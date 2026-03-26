-- Изтриване в обратен ред на релациите
DROP TABLE IF EXISTS crew_assignment CASCADE;
DROP TABLE IF EXISTS ticket CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS passenger CASCADE;
DROP TABLE IF EXISTS flight CASCADE;
DROP TABLE IF EXISTS aircraft CASCADE;

-- 1. СЛУЖИТЕЛИ
CREATE TABLE employee (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    phone VARCHAR(20)
);

-- 2. САМОЛЕТИ
CREATE TABLE aircraft (
    aircraft_id SERIAL PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL,
    airline VARCHAR(50) NOT NULL 
);

-- 3. ПОЛЕТИ
CREATE TABLE flight (
    flight_id SERIAL PRIMARY KEY,
    flight_number VARCHAR(10) UNIQUE NOT NULL,
    destination VARCHAR(50) NOT NULL,
    flight_date DATE NOT NULL,
    flight_time TIME NOT NULL,
    aircraft_id INTEGER REFERENCES aircraft(aircraft_id),
    base_price DECIMAL(10,2) NOT NULL
);
CREATE INDEX idx_destination ON flight(destination); -- Индекс за бързо търсене

-- 4. ПЪТНИЦИ
CREATE TABLE passenger (
    passenger_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    passport_number VARCHAR(20) UNIQUE NOT NULL,
    nationality VARCHAR(50) NOT NULL
);

-- 5. БИЛЕТИ
CREATE TABLE ticket (
    ticket_id SERIAL PRIMARY KEY,
    passenger_id INTEGER REFERENCES passenger(passenger_id), 
    flight_id INTEGER REFERENCES flight(flight_id),
    seat_number VARCHAR(5) NOT NULL,
    actual_price DECIMAL(10,2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. ЕКИПАЖ
CREATE TABLE crew_assignment (
    crew_assignment_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employee(employee_id) NOT NULL,
    flight_id INTEGER REFERENCES flight(flight_id) NOT NULL,
    role VARCHAR(50) NOT NULL, 
    UNIQUE (employee_id, flight_id)
);
