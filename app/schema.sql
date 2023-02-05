create database webapp default charset=utf8mb4;

use webapp;

create user 'www-data'@'localhost' identified by 'www-data';
grant all on webapp.* to 'www-data'@'localhost';

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
    `id` varchar(50) not null,
    `image_type` varchar(20) not null,
    `created_at` real not null,
    `url` varchar(50) not null,
    `private` boolean not null,
    primary key (`id`)
) engine=innodb default charset=utf8mb4;