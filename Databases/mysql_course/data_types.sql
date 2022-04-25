-- CREATE TABLE people (
--     name VARCHAR(100),
--     birthdate DATE,
--     birthtime TIME,
--     birthdt DATETIME
-- );
-- INSERT INTO people (name, birthdate, birthtime, birthdt)
-- VALUES(
--         'Padma',
--         '1983-11-11',
--         '10:07:35',
--         '1983-11-11 10:07:35'
--     );
-- INSERT INTO people (name, birthdate, birthtime, birthdt)
-- VALUES(
--         'Larry',
--         '1943-12-25',
--         '04:10:42',
--         '1943-12-25 04:10:42'
--     );
-- SELECT *
-- FROM people;
-- INSERT INTO people (name, birthdate, birthtime, birthdt)
-- VALUES(
--         'Toaster',
--     curdate(),curtime(), now()
--     );
create table comments2 (
    content varchar(100),
    created_at timestamp default now() on update now()
);
insert into comments2 (content)
values('asdassrv');
update comments2
set content = 'This is totally great !!!'
where content = 'jrtsbvf';
update comments2
set content = 'Enjoy this sweet moment!'
where content = 'asdassrv';