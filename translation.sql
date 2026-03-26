-- Създаваме таблица за преводи на градове
CREATE TABLE IF NOT EXISTS city_dictionary (
    city_en VARCHAR(50) PRIMARY KEY,
    city_bg VARCHAR(50) NOT NULL
);

-- Напълваме я с твоите дестинации
INSERT INTO city_dictionary (city_en, city_bg) VALUES
('London', 'Лондон'),
('Paris', 'Париж'),
('Berlin', 'Берлин'),
('Frankfurt', 'Франкфурт'),
('Rome', 'Рим'),
('Beijing', 'Пекин'),
('Bangkok', 'Бангкок'),
('Sofia', 'София'),
('Varna', 'Варна');