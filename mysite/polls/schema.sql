PRAGMA foreign_keys = ON;

drop table if EXISTS polls_question;
drop table if EXISTS polls_choice;

CREATE TABLE polls_question (
    id INTEGER NOT NULL PRIMARY KEY autoincrement,
    question_text text not null,
    pub_date datetime default (datetime('now', 'localtime'))
);

create table polls_choice (
    id INTEGER not null primary key autoincrement,
    choice_text text not null,
    votes integer not null default 0,
    question_id integer not null, 
    foreign key (question_id) references polls_question (id) on delete cascade
);

insert into polls_question (question_text) values
("What's new?"),
("What's up?");

insert into polls_choice (choice_text, question_id) values
('test1', 1),
('test2', 2),
('test3', 1);