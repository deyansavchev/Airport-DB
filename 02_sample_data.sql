-- =============================================
-- 02: Въвеждане на данни
-- =============================================

-- Изтриване на данни в правилния ред (за да избегнем грешки с foreign key)
DELETE FROM crew_assignment; -- Трябва да е първо заради FK
DELETE FROM ticket;
DELETE FROM passenger;
DELETE FROM flight;
DELETE FROM aircraft;
DELETE FROM employee;

-- Нулиране на последователности 
ALTER SEQUENCE aircraft_aircraft_id_seq RESTART WITH 1; --Рестартира брояча от начало. Това го правим, защото искаме пак всички броячи да започнат от 1, като преди това сме изтрили предварително данните с delete командата по-горе.
ALTER SEQUENCE flight_flight_id_seq RESTART WITH 1;
ALTER SEQUENCE passenger_passenger_id_seq RESTART WITH 1;
ALTER SEQUENCE employee_employee_id_seq RESTART WITH 1;
ALTER SEQUENCE ticket_ticket_id_seq RESTART WITH 1;
ALTER SEQUENCE crew_assignment_crew_assignment_id_seq RESTART WITH 1;

-- Самолети
INSERT INTO aircraft (model, capacity, airline) VALUES
('Boeing 737', 180, 'Bulgaria Air'),
('Airbus A320', 150, 'Wizz Air'),
('Boeing 787', 250, 'Lufthansa'),
('Embraer E195', 120, 'Ryanair'),
('Airbus A321', 200, 'British Airways');

-- Полети
INSERT INTO flight (flight_number, destination, flight_date, flight_time, aircraft_id, base_price) VALUES
('FB101', 'London', '2024-03-15', '08:00:00', 1, 250.00),
('FB102', 'Paris', '2024-03-15', '10:30:00', 1, 200.00),
('WZ201', 'Berlin', '2024-03-16', '14:15:00', 2, 150.00),
('LH301', 'Frankfurt', '2024-03-17', '16:45:00', 3, 300.00),
('BA401', 'London', '2024-03-18', '09:20:00', 5, 280.00),
('FB103', 'Rome', '2024-03-19', '11:45:00', 1, 220.00);

-- Пътници
INSERT INTO passenger (first_name, last_name, passport_number, nationality) VALUES
('Ivan', 'Petrov', 'BG123456', 'Bulgarian'),
('Maria', 'Ivanova', 'BG654321', 'Bulgarian'),
('John', 'Smith', 'US789012', 'American'),
('Anna', 'Müller', 'DE345678', 'German'),
('Georgi', 'Dimitrov', 'BG111222', 'Bulgarian'),
('Elena', 'Popova', 'BG333444', 'Bulgarian'),
('Michael', 'Brown', 'US555666', 'American');

-- Служители
INSERT INTO employee (first_name, last_name, position, phone) VALUES
('Petar', 'Georgiev', 'Pilot', '+359881234567'),
('Svetla', 'Nikolova', 'Flight Attendant', '+359885554444'),
('Dimitar', 'Iliev', 'Ground Staff', '+359886667777'),
('Krasimira', 'Stoyanova', 'Check-in Agent', '+359888889999');

-- Билети
INSERT INTO ticket (passenger_id, flight_id, seat_number, actual_price) VALUES
(1, 1, '15A', 250.00),  -- Ivan Petrov - FB101 London
(2, 1, '15B', 250.00),  -- Maria Ivanova - FB101 London
(3, 1, '16A', 260.00),  -- John Smith - FB101 London
(1, 6, '22A', 220.00),  -- Ivan Petrov - FB103 Rome
(1, 4, '23B', 300.00),  -- Ivan Petrov - LH301 Frankfurt
(4, 2, '08C', 200.00),  -- Anna Müller - FB102 Paris
(1, 2, '08D', 190.00),  -- Ivan Petrov - FB102 Paris
(5, 3, '12A', 150.00),  -- Georgi Dimitrov - WZ201 Berlin
(6, 3, '12B', 150.00),  -- Elena Popova - WZ201 Berlin
(7, 4, '05B', 300.00),  -- Michael Brown - LH301 Frankfurt
(1, 5, '10C', 280.00),  -- Ivan Petrov - BA401 London
(2, 5, '10D', 280.00),  -- Maria Ivanova - BA401 London
(3, 6, '07A', 220.00);  -- John Smith - FB103 Rome

-- Назначения на Екипаж
INSERT INTO crew_assignment (employee_id, flight_id, role) VALUES
(1, 1, 'Pilot'),             -- Petar Georgiev е пилот на FB101 (Лондон)
(2, 1, 'Flight Attendant'),  -- Svetla Nikolova е стюардеса на FB101
(1, 2, 'Pilot'),             -- Petar Georgiev е пилот на FB102 (Париж)
(2, 6, 'Flight Attendant'),  -- Svetla Nikolova е стюардеса на FB103 (Рим)
(3, 4, 'Technician');        -- Dimitar Iliev (Ground Staff) е техник на LH301 (Франкфурт)
