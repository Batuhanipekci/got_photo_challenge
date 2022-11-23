drop table if exists country_summary;
drop table if exists people;
drop table if exists person_info;
drop table if exists city;
drop table if exists county;
drop table if exists country;


create table `country` (
  `id` int not null auto_increment,
  `name` varchar(80) default null,
  primary key (`id`)
);

create table `county` (
  `id` int not null auto_increment,
  `name` varchar(80) default null,
  `country_id` int default null,
  primary key (`id`),
  foreign key (`country_id`) references `country`(`id`)
);

create table `city` (
  `id` int not null auto_increment,
  `name` varchar(80) default null,
  `county_id` int default null,
  primary key (`id`),
  foreign key (`county_id`) references `county`(`id`)
);

create table `person` (
  `id` int not null auto_increment,
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` date default null,
  `city_id` int default null,
  primary key (`id`),
  foreign key (`city_id`) references `city`(`id`)
);

create table `person_info` (
  `id` int not null auto_increment,
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` date default null,
  `city` varchar(80) default null,
  `county` varchar(80) default null,
  `country` varchar(80) default null,
  primary key (`id`)
);

create table `country_summary` (
  `country` varchar(80) default null,
  `count_of_people` varchar(80) default null
);
