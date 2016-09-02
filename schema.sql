drop table if exists edqos;
create table edqos (
  id integer primary key autoincrement,
  policy text not null,
  app text not null
);
