create table shell
(id int AUTO_INCREMENT,
server varchar(60),
ip varchar(30),
shell varchar(90),
all_same varchar(30),
primary key(id)
)DEFAULT CHARSET=utf8;

create table shell_control
(id int AUTO_INCREMENT,
ip varchar(30),
shell varchar(90),
status varchar(90),
primary key(id)
)DEFAULT CHARSET=utf8;