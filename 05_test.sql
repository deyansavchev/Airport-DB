-- 1. Проверка на билетите за полет 1
SELECT COUNT(*) as total_tickets, 
       COALESCE(SUM(actual_price), 0) as total_revenue
FROM ticket 
WHERE flight_id = 1;

-- 2. Проверка на капацитета за полет 1
SELECT a.capacity, COUNT(t.ticket_id) as sold_tickets
FROM flight f
JOIN aircraft a ON f.aircraft_id = a.aircraft_id
LEFT JOIN ticket t ON f.flight_id = t.flight_id
WHERE f.flight_id = 1
GROUP BY a.capacity;

-- 3. Проверка на датите на полетите
SELECT flight_id, flight_number, flight_date 
FROM flight 
ORDER BY flight_date;