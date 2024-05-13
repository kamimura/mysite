DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);

create table post (
    id integer primary key autoincrement,
    author_id integer not null,
    created datetime not null default (datetime('now', 'localtime')),
    title text not null,
    body text  not null,
    foreign key (author_id) references user(id)
);

-- insert into user (username, password)
-- values
-- ('user1', 'passwd1'),
-- ('user2', 'passwd2');

-- INSERT into post (author_id, title, body)
-- values
-- (1, 'test title1', 'test body1'),
-- (1, 'test title2', 'test body2'),
-- (2, 'test title1', 'test body2');