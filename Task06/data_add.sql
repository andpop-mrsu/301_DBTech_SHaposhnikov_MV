-- Добавляем 5 пользователей (без указания ID, база сама их назначит)
INSERT INTO users (name, email, gender, register_date, occupation_id) VALUES
('Шапошников Максим', 'shaposhnikov@mail.ru', 'M', DATE('now'), (SELECT id FROM occupations WHERE name = 'student')),
('Цветков Максим', 'tsvetkov@mail.ru', 'M', DATE('now'), (SELECT id FROM occupations WHERE name = 'student')),
('Яськин Дмитрий', 'yaskin@mail.ru', 'M', DATE('now'), (SELECT id FROM occupations WHERE name = 'student')),
('Умяров Арслан', 'umyarov@mail.ru', 'M', DATE('now'), (SELECT id FROM occupations WHERE name = 'student')),
('Смирнов Александр', 'smirnov@mail.ru', 'M', DATE('now'), (SELECT id FROM occupations WHERE name = 'student'));

-- Добавляем 3 новых фильма (без указания ID)
INSERT INTO movies (title, year, genres) VALUES
('Мой любимый фильм 1', 2023, 'Action'),
('Мой любимый фильм 2', 2024, 'Comedy'),
('Мой любимый фильм 3', 2022, 'Drama');

-- Добавляем 3 отзыва от тебя (без указания ID)
INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES
((SELECT id FROM users WHERE email = 'shaposhnikov@mail.ru'), (SELECT id FROM movies WHERE title = 'Мой любимый фильм 1'), 5.0, strftime('%s', 'now')),
((SELECT id FROM users WHERE email = 'shaposhnikov@mail.ru'), (SELECT id FROM movies WHERE title = 'Мой любимый фильм 2'), 4.5, strftime('%s', 'now')),
((SELECT id FROM users WHERE email = 'shaposhnikov@mail.ru'), (SELECT id FROM movies WHERE title = 'Мой любимый фильм 3'), 3.0, strftime('%s', 'now'));