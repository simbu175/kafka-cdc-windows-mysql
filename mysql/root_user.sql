select user, host from mysql.user;

drop user if exists super_user;

CREATE USER 'super_user' IDENTIFIED BY 'Lumia@820';

GRANT ALL PRIVILEGES ON *.* TO 'super-user'@'%' WITH GRANT OPTION;

GRANT ALL PRIVILEGES ON *.* TO 'super_user' WITH GRANT OPTION;
FLUSH PRIVILEGES;

ALTER USER 'super_user'@'%' IDENTIFIED WITH mysql_native_password BY 'Lumia@820';

select @@shared_memory_base_name;