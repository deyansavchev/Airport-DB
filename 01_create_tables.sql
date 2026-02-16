-- =============================================
-- 01: Създаване на таблици
-- =============================================

-- Таблица самолет
CREATE TABLE IF NOT EXISTS aircraft (
    aircraft_id SERIAL PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL,
    airline VARCHAR(50) NOT NULL
);

-- Таблица полет  
CREATE TABLE IF NOT EXISTS flight (
    flight_id SERIAL PRIMARY KEY,
    flight_number VARCHAR(10) UNIQUE NOT NULL,
    destination VARCHAR(50) NOT NULL,
    flight_date DATE NOT NULL,
    flight_time TIME NOT NULL,
    aircraft_id INTEGER REFERENCES aircraft(aircraft_id),
    base_price DECIMAL(10,2) NOT NULL
);

-- Таблица пътник
CREATE TABLE IF NOT EXISTS passenger (
    passenger_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    passport_number VARCHAR(20) UNIQUE NOT NULL,
    nationality VARCHAR(50) NOT NULL
);

-- Таблица служител
CREATE TABLE IF NOT EXISTS employee (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    phone VARCHAR(20)
);

-- Таблица билети
CREATE TABLE IF NOT EXISTS ticket (
    ticket_id SERIAL PRIMARY KEY,
    passenger_id INTEGER REFERENCES passenger(passenger_id),
    flight_id INTEGER REFERENCES flight(flight_id),
    seat_number VARCHAR(5) NOT NULL,
    actual_price DECIMAL(10,2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица за назначение на екипаж
CREATE TABLE IF NOT EXISTS crew_assignment (
    crew_assignment_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employee(employee_id) NOT NULL,
    flight_id INTEGER REFERENCES flight(flight_id) NOT NULL,
    role VARCHAR(50) NOT NULL, 
    UNIQUE (employee_id, flight_id)
);

COMMENT ON TABLE crew_assignment IS 'Свързва служители (екипаж) с конкретен полет.';

COMMENT ON COLUMN crew_assignment.role IS 'Ролята на служителя в този полет (напр. Pilot, Flight Attendant).';
