USE seat_reservation;

INSERT INTO students (student_id, name, password, wechat_number, school, breach_count)
VALUES 
('23210240001', 'Alice', '123456', 'wx_alice', '复旦大学计算机科学技术学院', 0),
('23210240002', 'Bob', '123456', 'wx_bob', '复旦大学管理学院', 0),
('23210240003', 'Charlie', '123456', 'wx_charlie', '复旦大学国际关系与公共事务学院', 0),
('23210240004', 'David', '123456', 'wx_david', '复旦大学新闻学院', 0),
('23210240005', 'Eve', '123456', 'wx_eve', '复旦大学法学院', 0),
('23210240006', 'Frank', '123456', 'wx_frank', '复旦大学外国语言文学学院', 0),
('23210240007', 'Grace', '123456', 'wx_grace', '复旦大学化学系', 0),
('23210240008', 'Hank', '123456', 'wx_hank', '复旦大学数学科学学院', 0),
('23210240009', 'Ivy', '123456', 'wx_ivy', '复旦大学物理学系', 0),
('23210240010', 'Jack', '123456', 'wx_jack', '复旦大学生命科学学院', 0);

INSERT INTO Administer (name, password, wechat_number)
VALUES 
    ('Admin1', 'adminpass123', 'adminwechat001'),
    ('Admin2', 'adminpass456', 'adminwechat002');

INSERT INTO Building (name, campus, open_time, close_time, deprecated)
VALUES 
    ('Main Library', 'H', '08:00:00', '22:00:00', False),
    ('Science Building', 'H', '09:00:00', '21:00:00', False);

INSERT INTO Room (building_id, school, name, open_time, close_time, deprecated)
VALUES 
    (1, 'Computer', 'A6010', '08:00:00', '22:00:00', False),
    (2, 'English', 'D2010', '09:00:00', '21:00:00', False);

INSERT INTO Seat (room_id, near_fixed_socket, near_movable_socket, near_window, deprecated)
VALUES 
    (1, True, False, True, False),
    (1, False, True, False, False),
    (2, True, True, True, False),
    (2, False, False, False, False);

INSERT INTO Reservation (user_id, room_id, seat_id, create_time, start_time, end_time, status)
VALUES 
    (1, 1, 1, '2024-06-25 10:00:00', '2024-06-25 10:30:00', '2024-06-25 12:30:00', 0),
    (2, 2, 3, '2024-06-26 14:00:00', '2024-06-26 14:30:00', '2024-06-26 16:30:00', 0);

INSERT INTO AdminConfig (config_key, config_value)
VALUES 
    ('max_reservation_duration', 5);
