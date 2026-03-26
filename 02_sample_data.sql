-- Изтриване на данни в правилния ред (за да избегнем грешки с foreign key)
DELETE FROM crew_assignment;
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

-- London
('FB101A', 'London', '2026-04-20', '08:00:00', 1, 250.00),
('FB101B', 'London', '2026-05-05', '09:15:00', 1, 270.00),
('FB101C', 'London', '2026-05-22', '10:30:00', 1, 290.00),
('FB101D', 'London', '2026-06-10', '11:45:00', 1, 310.00),
('FB101E', 'London', '2026-07-01', '13:00:00', 1, 330.00),

('BA401A', 'London', '2026-04-25', '09:20:00', 5, 280.00),
('BA401B', 'London', '2026-05-12', '10:40:00', 5, 300.00),
('BA401C', 'London', '2026-05-28', '12:00:00', 5, 320.00),
('BA401D', 'London', '2026-06-15', '13:20:00', 5, 340.00),
('BA401E', 'London', '2026-07-05', '14:40:00', 5, 360.00),

-- Paris
('FB102A', 'Paris', '2026-04-21', '10:30:00', 1, 200.00),
('FB102B', 'Paris', '2026-05-06', '11:45:00', 1, 215.00),
('FB102C', 'Paris', '2026-05-23', '13:00:00', 1, 230.00),
('FB102D', 'Paris', '2026-06-11', '14:15:00', 1, 245.00),
('FB102E', 'Paris', '2026-07-02', '15:30:00', 1, 260.00),

-- Berlin
('WZ201A', 'Berlin', '2026-04-22', '14:15:00', 2, 150.00),
('WZ201B', 'Berlin', '2026-05-08', '15:30:00', 2, 165.00),
('WZ201C', 'Berlin', '2026-05-25', '16:45:00', 2, 180.00),
('WZ201D', 'Berlin', '2026-06-12', '18:00:00', 2, 195.00),
('WZ201E', 'Berlin', '2026-07-03', '19:15:00', 2, 210.00),

-- Frankfurt
('LH301A', 'Frankfurt', '2026-04-23', '16:45:00', 3, 300.00),
('LH301B', 'Frankfurt', '2026-05-09', '18:00:00', 3, 320.00),
('LH301C', 'Frankfurt', '2026-05-26', '19:15:00', 3, 340.00),
('LH301D', 'Frankfurt', '2026-06-13', '20:30:00', 3, 360.00),
('LH301E', 'Frankfurt', '2026-07-04', '21:45:00', 3, 380.00),

-- Rome
('FB103A', 'Rome', '2026-04-24', '11:45:00', 1, 220.00),
('FB103B', 'Rome', '2026-05-10', '13:00:00', 1, 235.00),
('FB103C', 'Rome', '2026-05-27', '14:15:00', 1, 250.00),
('FB103D', 'Rome', '2026-06-14', '15:30:00', 1, 265.00),
('FB103E', 'Rome', '2026-07-06', '16:45:00', 1, 280.00),

-- Beijing
('FB105A', 'Beijing', '2026-04-26', '11:51:00', 1, 500.00),
('FB105B', 'Beijing', '2026-05-13', '13:10:00', 1, 530.00),
('FB105C', 'Beijing', '2026-05-29', '14:30:00', 1, 560.00),
('FB105D', 'Beijing', '2026-06-16', '15:50:00', 1, 590.00),
('FB105E', 'Beijing', '2026-07-07', '17:10:00', 1, 620.00),

-- Bangkok
('FB106A', 'Bangkok', '2026-04-27', '11:52:00', 1, 480.00),
('FB106B', 'Bangkok', '2026-05-14', '13:05:00', 1, 510.00),
('FB106C', 'Bangkok', '2026-05-30', '14:20:00', 1, 540.00),
('FB106D', 'Bangkok', '2026-06-18', '15:35:00', 1, 570.00),
('FB106E', 'Bangkok', '2026-07-08', '16:50:00', 1, 600.00),

-- Varna
('FB109A', 'Varna', '2026-04-21', '11:58:00', 1, 90.00),
('FB109B', 'Varna', '2026-05-06', '13:05:00', 1, 100.00),
('FB109C', 'Varna', '2026-05-23', '14:15:00', 1, 110.00),
('FB109D', 'Varna', '2026-06-11', '15:25:00', 1, 120.00),
('FB109E', 'Varna', '2026-07-02', '16:35:00', 1, 130.00),

-- Mumbai
('FB120A', 'Mumbai', '2026-04-22', '11:49:00', 1, 450.00),
('FB120B', 'Mumbai', '2026-05-08', '13:00:00', 1, 480.00),
('FB120C', 'Mumbai', '2026-05-25', '14:10:00', 1, 510.00),
('FB120D', 'Mumbai', '2026-06-12', '15:20:00', 1, 540.00),
('FB120E', 'Mumbai', '2026-07-03', '16:30:00', 1, 570.00),

-- Cairo
('FB130A', 'Cairo', '2026-04-23', '11:46:00', 1, 300.00),
('FB130B', 'Cairo', '2026-05-09', '12:55:00', 1, 320.00),
('FB130C', 'Cairo', '2026-05-26', '14:05:00', 1, 340.00),
('FB130D', 'Cairo', '2026-06-13', '15:15:00', 1, 360.00),
('FB130E', 'Cairo', '2026-07-04', '16:25:00', 1, 380.00);

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
