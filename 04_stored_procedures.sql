-- =================================================================
-- ИЗЧИСТВАНЕ НА СТАРИ ОБЕКТИ (АКО СЪЩЕСТВУВАТ)
-- =================================================================
DROP TRIGGER IF EXISTS validate_seat_trigger ON ticket;
DROP TRIGGER IF EXISTS log_ticket_purchase ON ticket;
DROP FUNCTION IF EXISTS validate_seat_number() CASCADE;
DROP FUNCTION IF EXISTS update_flight_stats() CASCADE;
DROP FUNCTION IF EXISTS get_flight_revenue(INTEGER) CASCADE;
DROP FUNCTION IF EXISTS get_available_seats(INTEGER) CASCADE;
DROP FUNCTION IF EXISTS find_frequent_travelers(INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS flight_report_cursor() CASCADE;
DROP PROCEDURE IF EXISTS book_ticket(INTEGER, INTEGER, VARCHAR, DECIMAL);
DROP PROCEDURE IF EXISTS upsert_passenger(INT, VARCHAR, VARCHAR, VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS delete_flight_safe(INT);
DROP PROCEDURE IF EXISTS update_aircraft_details(INT, VARCHAR, INT, VARCHAR);
DROP PROCEDURE IF EXISTS add_employee_record(VARCHAR, VARCHAR, VARCHAR, VARCHAR);

-- =================================================================
-- 1. ПОМОЩНИ ФУНКЦИИ (Utility Functions)
-- =================================================================

-- Изчисляване на общите приходи за конкретен полет
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

-- Получаване на броя свободни места в полет
CREATE OR REPLACE FUNCTION get_available_seats(flight_id_param INTEGER)
RETURNS INTEGER AS $$
DECLARE
    capacity_val INTEGER;
    sold_val INTEGER;
BEGIN
    SELECT a.capacity INTO capacity_val
    FROM flight f
    JOIN aircraft a ON f.aircraft_id = a.aircraft_id
    WHERE f.flight_id = flight_id_param;
    
    SELECT COUNT(*) INTO sold_val
    FROM ticket
    WHERE flight_id = flight_id_param;
    
    RETURN capacity_val - sold_val;
END;
$$ LANGUAGE plpgsql;

-- Намиране на чести пътници (Справка чрез функция)
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

-- =================================================================
-- 2. ТРИГЕРИ (Валидация и Логове)
-- =================================================================

-- Валидиране на формата на номера на място (напр. 15A)
CREATE OR REPLACE FUNCTION validate_seat_number()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.seat_number !~ '^[0-9]{1,2}[A-Z]$' THEN
        RAISE EXCEPTION 'Невалиден формат на номер на място. Използвайте формат като 15A, 8C и т.н.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_seat_trigger
    BEFORE INSERT OR UPDATE ON ticket
    FOR EACH ROW
    EXECUTE FUNCTION validate_seat_number();

-- Логове при покупка на билет
CREATE OR REPLACE FUNCTION update_flight_stats()
RETURNS TRIGGER AS $$
BEGIN
    RAISE NOTICE 'Нов закупен билет: Полет %, Място %, Цена %', 
                 NEW.flight_id, NEW.seat_number, NEW.actual_price;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_ticket_purchase
    AFTER INSERT ON ticket
    FOR EACH ROW
    EXECUTE FUNCTION update_flight_stats();

-- =================================================================
-- 3. ФУНКЦИИ С КУРСОР
-- =================================================================

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
        
        SELECT COUNT(t.ticket_id), COALESCE(SUM(t.actual_price), 0)
        INTO total_passengers, total_revenue
        FROM ticket t
        WHERE t.flight_id = (SELECT f.flight_id FROM flight f WHERE f.flight_number = flight_rec.flight_number LIMIT 1);
        
        flight_number := flight_rec.flight_number;
        destination := flight_rec.destination;
        RETURN NEXT;
    END LOOP;
    CLOSE flight_cursor;
END;
$$ LANGUAGE plpgsql;

-- =================================================================
-- 4. СЪХРАНЕНИ ПРОЦЕДУРИ (Минимум 5 броя за CRUD и Бизнес логика)
-- =================================================================

-- Процедура 1: Резервиране на билет с бизнес валидация
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
    available_seats := get_available_seats(flight_id_param);
    
    IF available_seats <= 0 THEN
        RAISE EXCEPTION 'Няма свободни места в този полет';
    END IF;
    
    SELECT COUNT(*) INTO existing_booking
    FROM ticket
    WHERE passenger_id = passenger_id_param AND flight_id = flight_id_param;
    
    IF existing_booking > 0 THEN
        RAISE EXCEPTION 'Пътникът вече има билет за този полет';
    END IF;
    
    INSERT INTO ticket (passenger_id, flight_id, seat_number, actual_price)
    VALUES (passenger_id_param, flight_id_param, seat_number_param, ticket_price);
    
    RAISE NOTICE 'Билетът е резервиран успешно за място %', seat_number_param;
END;
$$ LANGUAGE plpgsql;

-- Процедура 2: CRUD - Добавяне или Обновяване на пътник
CREATE OR REPLACE PROCEDURE upsert_passenger(
    p_id INT, f_name VARCHAR, l_name VARCHAR, p_num VARCHAR, nat VARCHAR
) AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM passenger WHERE passenger_id = p_id) THEN
        UPDATE passenger SET first_name = f_name, last_name = l_name, passport_number = p_num, nationality = nat
        WHERE passenger_id = p_id;
    ELSE
        INSERT INTO passenger (first_name, last_name, passport_number, nationality)
        VALUES (f_name, l_name, p_num, nat);
    END IF;
END; $$ LANGUAGE plpgsql;

-- Процедура 3: CRUD - Безопасно изтриване на полет (Каскадна логика)
CREATE OR REPLACE PROCEDURE delete_flight_safe(f_id INT) AS $$
BEGIN
    DELETE FROM crew_assignment WHERE flight_id = f_id;
    DELETE FROM ticket WHERE flight_id = f_id;
    DELETE FROM flight WHERE flight_id = f_id;
END; $$ LANGUAGE plpgsql;

-- Процедура 4: CRUD - Обновяване на данни за самолет
CREATE OR REPLACE PROCEDURE update_aircraft_details(a_id INT, new_model VARCHAR, new_cap INT, new_airline VARCHAR) AS $$
BEGIN
    UPDATE aircraft SET model = new_model, capacity = new_cap, airline = new_airline WHERE aircraft_id = a_id;
END; $$ LANGUAGE plpgsql;

-- Процедура 5: CRUD - Добавяне на нов служител
CREATE OR REPLACE PROCEDURE add_employee_record(f_name VARCHAR, l_name VARCHAR, pos VARCHAR, ph VARCHAR) AS $$
BEGIN
    INSERT INTO employee (first_name, last_name, position, phone) VALUES (f_name, l_name, pos, ph);
END; $$ LANGUAGE plpgsql;

-- =================================================================
-- 5. ОСЕМ ЛОГИЧЕСКИ РАЗЛИЧНИ СПРАВКИ (За интерфейса)
-- =================================================================

-- 1. Многокритериално търсене (Реализирано динамично в Python)

-- 2. Вложена заявка - Пътници, летели със самолети Boeing
-- SELECT first_name, last_name FROM passenger WHERE passenger_id IN (...)

-- 3. Диапазонна справка - Полети в ценови диапазон
-- SELECT * FROM flight WHERE base_price BETWEEN 150 AND 500;

-- 4. Агрегатна справка - Общи приходи по авиокомпании
-- SELECT a.airline, SUM(t.actual_price) FROM aircraft a JOIN flight f...

-- 5. Сортировъчна справка - Полети подредени по заетост (процент)

-- 6. Времева справка - Продажби за последните 30 дни
-- SELECT * FROM ticket WHERE purchase_date >= CURRENT_DATE - INTERVAL '30 days';

-- 7. Сложен JOIN - Пълен списък на екипажа с техните роли и дестинации
-- SELECT e.first_name, e.last_name, ca.role, f.destination FROM employee e...

-- 8. Топ дестинации - Град с най-много продадени билети
-- SELECT destination, COUNT(ticket_id) as sales FROM flight f JOIN ticket t...
