create database awesome default charset=utf8mb4;

use awesome;

create user 'www-data'@'%' identified by 'www-data';
grant all on awesome.* to 'www-data'@'%';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    primary key (`id`)
) engine=innodb default charset=utf8mb4;

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `name` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` text not null,
    `created_at` real not null,
    `tag` varchar(20) not null,
    primary key (`id`)
) engine=innodb default charset=utf8mb4;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` text not null,
    `created_at` real not null,
    primary key (`id`)
) engine=innodb default charset=utf8mb4;

create table atlas (
    `name` varchar(50) not null,
    `created_at` real not null,
    `url` varchar(50) not null,
    `private` boolean not null,
    primary key (`name`)
) engine=innodb default charset=utf8mb4;