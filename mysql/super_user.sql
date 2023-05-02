show databases;

drop database if exists local_db;
create database local_db;

CREATE USER 'local_user' IDENTIFIED BY 'Lumia@820';
GRANT SELECT ON local_db.* TO 'local_user';
GRANT SELECT ON sakila.* TO 'local_user';
GRANT SELECT ON world.* TO 'local_user';

FLUSH PRIVILEGES;

select current_user();
SHOW VARIABLES LIKE '%name%';

SELECT user, host, select_priv, insert_priv, shutdown_priv, grant_priv 
FROM mysql.user;

use local_db; 

drop table if exists actor_local;
create table actor_local
select * from sakila.actor
where 1 = 2;

truncate table actor_local;
insert into actor_local 
select * from sakila.actor
LIMIT 5;

select * from actor_local;

show master status;
flush logs;

use sakila;
show tables;

select * from nicer_but_slower_film_list;

select a.*
from nicer_but_slower_film_list a
join (	select * from 
			(select title, price,
				row_number() over (partition by category order by price desc) max_price
		from nicer_but_slower_film_list ) x
		where x.max_price = 1
        ) b
on a.title = b.title and a.price = b.price;