-- =============================================
-- 04: ЗАПАЗЕНИ ПРОЦЕДУРИ И ФУНКЦИИ
-- =============================================

-- Изтриване на стари тригери и функции (ако съществуват)
DROP TRIGGER IF EXISTS validate_seat_trigger ON ticket;
DROP TRIGGER IF EXISTS log_ticket_purchase ON ticket;
DROP FUNCTION IF EXISTS validate_seat_number() CASCADE;
DROP FUNCTION IF EXISTS update_flight_stats() CASCADE;
DROP FUNCTION IF EXISTS get_flight_revenue(INTEGER) CASCADE;
DROP FUNCTION IF EXISTS get_available_seats(INTEGER) CASCADE;
DROP FUNCTION IF EXISTS find_frequent_travelers(INTEGER, INTEGER) CASCADE;
DROP PROCEDURE IF EXISTS book_ticket(INTEGER, INTEGER, VARCHAR, DECIMAL);

-- 1. ФУНКЦИЯ: Изчисляване на общите приходи за полет
CREATE OR REPLACE FUNCTION get_flight_revenue(flight_id_param INTEGER)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    total DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(actual_price), 0) 
    INTO total
    FROM ticket 
    WHERE flight_id = flight_id_param;
    
    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- 2. ФУНКЦИЯ: Получаване на свободни места в полет
CREATE OR REPLACE FUNCTION get_available_seats(flight_id_param INTEGER)
RETURNS INTEGER AS $$
DECLARE
    capacity INTEGER;
    sold INTEGER;
BEGIN
    -- Вземане на капацитета на самолета
    SELECT a.capacity INTO capacity
    FROM flight f
    JOIN aircraft a ON f.aircraft_id = a.aircraft_id
    WHERE f.flight_id = flight_id_param;
    
    -- Броене на продадените билети
    SELECT COUNT(*) INTO sold
    FROM ticket
    WHERE flight_id = flight_id_param;
    
    RETURN capacity - sold;
END;
$$ LANGUAGE plpgsql;

-- 3. ФУНКЦИЯ: Намиране на чести пътници
CREATE OR REPLACE FUNCTION find_frequent_travelers(
    months_back INTEGER DEFAULT 6,
    min_flights INTEGER DEFAULT 3
)
RETURNS TABLE (
    passenger_name VARCHAR(100),
    passport_number VARCHAR(20),
    flights_count BIGINT,
    total_spent DECIMAL(10,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (p.first_name || ' ' || p.last_name)::VARCHAR(100) as passenger_name,
        p.passport_number,
        COUNT(t.ticket_id) as flights_count,
        SUM(t.actual_price) as total_spent
    FROM passenger p
    JOIN ticket t ON p.passenger_id = t.passenger_id
    JOIN flight f ON t.flight_id = f.flight_id
    WHERE f.flight_date >= CURRENT_DATE - (months_back || ' months')::INTERVAL
    GROUP BY p.passenger_id, p.first_name, p.last_name, p.passport_number
    HAVING COUNT(t.ticket_id) >= min_flights
    ORDER BY flights_count DESC;
END;
$$ LANGUAGE plpgsql;

-- 4. ПРОЦЕДУРА: Резервиране на билет с валидация
CREATE OR REPLACE PROCEDURE book_ticket(
    passenger_id_param INTEGER,
    flight_id_param INTEGER,
    seat_number_param VARCHAR(5),
    ticket_price DECIMAL(10,2)
)
AS $$
DECLARE
    available_seats INTEGER;
    existing_booking INTEGER;
BEGIN
    -- Проверка на свободните места
    available_seats := get_available_seats(flight_id_param);
    
    IF available_seats <= 0 THEN
        RAISE EXCEPTION 'Няма свободни места в този полет';
    END IF;
    
    -- Проверка дали пътникът вече е резервирал този полет
    SELECT COUNT(*) INTO existing_booking
    FROM ticket
    WHERE passenger_id = passenger_id_param 
    AND flight_id = flight_id_param;
    
    IF existing_booking > 0 THEN
        RAISE EXCEPTION 'Пътникът вече има билет за този полет';
    END IF;
    
    -- Вмъкване на билета
    INSERT INTO ticket (passenger_id, flight_id, seat_number, actual_price)
    VALUES (passenger_id_param, flight_id_param, seat_number_param, ticket_price);
    
    RAISE NOTICE 'Билетът е резервиран успешно за място %', seat_number_param;
END;
$$ LANGUAGE plpgsql;

-- 5. ФУНКЦИЯ ЗА ТРИГЕР: Валидиране на формата на номера на място
CREATE OR REPLACE FUNCTION validate_seat_number()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверка дали номерът на място съответства на шаблон като 15A, 8C и т.н.
    IF NEW.seat_number !~ '^[0-9]{1,2}[A-Z]$' THEN
        RAISE EXCEPTION 'Невалиден формат на номер на място. Използвайте формат като 15A, 8C и т.н.';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 6. ТРИГЕР: Добавяне на валидацията на номера на място
CREATE TRIGGER validate_seat_trigger
    BEFORE INSERT OR UPDATE ON ticket
    FOR EACH ROW
    EXECUTE FUNCTION validate_seat_number();

-- 7. ФУНКЦИЯ ЗА ТРИГЕР: Актуализиране на статистиките за полети
CREATE OR REPLACE FUNCTION update_flight_stats()
RETURNS TRIGGER AS $$
BEGIN
    RAISE NOTICE 'Нов закупен билет: Полет %, Място %, Цена %', 
                 NEW.flight_id, NEW.seat_number, NEW.actual_price;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 8. ТРИГЕР: Логване на закупени билети
CREATE TRIGGER log_ticket_purchase
    AFTER INSERT ON ticket
    FOR EACH ROW
    EXECUTE FUNCTION update_flight_stats();
	
-- Функция с курсор за отчет на всички полети
CREATE OR REPLACE FUNCTION flight_report_cursor()
RETURNS TABLE(
    flight_number VARCHAR,
    destination VARCHAR,
    total_passengers INTEGER,
    total_revenue DECIMAL(10,2)
) AS $$
DECLARE
    flight_rec RECORD;
    flight_cursor CURSOR FOR 
        SELECT f.flight_number, f.destination 
        FROM flight f 
        ORDER BY f.flight_date;
BEGIN
    OPEN flight_cursor;
    LOOP
        FETCH flight_cursor INTO flight_rec;
        EXIT WHEN NOT FOUND;
        
        -- Изчисляване за всеки полет
        SELECT COUNT(t.ticket_id), COALESCE(SUM(t.actual_price), 0)
        INTO total_passengers, total_revenue
        FROM ticket t
        JOIN flight f ON t.flight_id = f.flight_id
        WHERE f.flight_number = flight_rec.flight_number;
        
        flight_number := flight_rec.flight_number;
        destination := flight_rec.destination;
        RETURN NEXT;
    END LOOP;
    CLOSE flight_cursor;
END;
$$ LANGUAGE plpgsql;