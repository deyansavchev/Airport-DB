-- =============================================
-- 03: Заявки
-- =============================================

-- 1. Търсене на полети според дистинацията
SELECT f.flight_id, f.flight_number, f.destination, 
       f.flight_date, f.flight_time, a.airline,
       a.model as aircraft_model, f.base_price
FROM flight f
JOIN aircraft a ON f.aircraft_id = a.aircraft_id
WHERE f.destination = 'London';

-- 2. Търсене на полети според дата
SELECT f.flight_id, f.flight_number, f.destination, 
       f.flight_date, f.flight_time, a.airline,
       a.model as aircraft_model, f.base_price
FROM flight f
JOIN aircraft a ON f.aircraft_id = a.aircraft_id
WHERE f.flight_date = '2024-03-15';

-- 3. Търсене на полети според авиокомпания
SELECT f.flight_id, f.flight_number, f.destination, 
       f.flight_date, f.flight_time, a.airline,
       a.model as aircraft_model, f.base_price
FROM flight f
JOIN aircraft a ON f.aircraft_id = a.aircraft_id
WHERE a.airline = 'Bulgaria Air';

-- 4. Търсене на пътник според конкретен полет
SELECT p.first_name, p.last_name, p.passport_number, p.nationality,
       t.seat_number, t.actual_price
FROM passenger p
JOIN ticket t ON p.passenger_id = t.passenger_id
WHERE t.flight_id = 1;  -- FB101 to London

-- 5. Изчисляване на запълнен капацитет на самолет
SELECT f.flight_number, f.destination, f.flight_date,
       a.model, a.capacity,
       COUNT(t.ticket_id) as tickets_sold,
       ROUND((COUNT(t.ticket_id)::DECIMAL / a.capacity) * 100, 2) as occupancy_percent
FROM flight f
JOIN aircraft a ON f.aircraft_id = a.aircraft_id
LEFT JOIN ticket t ON f.flight_id = t.flight_id
GROUP BY f.flight_id, f.flight_number, f.destination, f.flight_date, a.model, a.capacity
ORDER BY f.flight_date;

-- 6. Изчисляване на приходите от билети за определен период (март)
SELECT SUM(actual_price) as total_revenue,
       COUNT(ticket_id) as tickets_sold,
       ROUND(AVG(actual_price), 2) as average_ticket_price
FROM ticket
WHERE purchase_date BETWEEN '2024-03-01' AND '2024-03-31';

-- 7. Топ 5 най-печеливши дестинации
SELECT f.destination,
       COUNT(t.ticket_id) as tickets_sold,
       SUM(t.actual_price) as total_revenue,
       ROUND(AVG(t.actual_price), 2) as average_price
FROM flight f
JOIN ticket t ON f.flight_id = t.flight_id
GROUP BY f.destination
ORDER BY total_revenue DESC
LIMIT 5;

-- 8. Най-редовни пътници (3+ полета за последните 6 месеца)
SELECT p.first_name, p.last_name, p.passport_number,
       COUNT(t.ticket_id) as flights_taken,
       SUM(t.actual_price) as total_spent
FROM passenger p
JOIN ticket t ON p.passenger_id = t.passenger_id
JOIN flight f ON t.flight_id = f.flight_id
WHERE f.flight_date >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY p.passenger_id, p.first_name, p.last_name, p.passport_number
HAVING COUNT(t.ticket_id) >= 3
ORDER BY flights_taken DESC;

-- 9. Търсене на екипажа за конкретен полет (пр. FB101)
SELECT f.flight_number, f.destination, 
       e.first_name, e.last_name, 
       ca.role, e.position AS employee_position
FROM crew_assignment ca
JOIN employee e ON ca.employee_id = e.employee_id
JOIN flight f ON ca.flight_id = f.flight_id
WHERE f.flight_number = 'FB101'
ORDER BY ca.role DESC;

-- 10. Кой служител е зает на конкретен полет (пр. FB101)
SELECT f.flight_number, f.destination, 
       e.first_name, e.last_name, 
       ca.role, e.position AS employee_position
FROM crew_assignment ca
JOIN employee e ON ca.employee_id = e.employee_id
JOIN flight f ON ca.flight_id = f.flight_id
WHERE f.flight_number = 'FB101'
ORDER BY ca.role DESC;