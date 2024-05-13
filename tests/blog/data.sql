insert into user (username, password) values
  ('test', 'scrypt:32768:8:1$TmKcScZdMtWRnCoE$39ac5af8ca2ecd10e301ebe9e8c625ac18342865f1deee2c889c9362da384775f1c7adc6af1b4d938ce4d759fa0b25d071ab3b728e2736f6a6e5adb2138eba42'),
  ('other', 'scrypt:32768:8:1$iFVYxFXvgDZ2xGKw$3255af7898badde1de0d22b3aaa8b1d42677850025460c82b1784fc6427adfa3cc53631fadd213e8a30dbcae633a56c9826825bbaf07431634c9de0524a3e86a');

insert into post (title, body, author_id, created)
values ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00')