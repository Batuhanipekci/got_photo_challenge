insert into `person_info` (
  `given_name`,
  `family_name`,
  `date_of_birth`,
  `city`,
  `county`,
  `country`
)
select 
  `person`.`given_name`     as `given_name`,
  `person`.`family_name`    as `family_name`,
  `person`.`date_of_birth`  as `date_of_birth`,
  `city`.`name`             as `city`,
  `county`.`name`           as `county`,
  `country`.`name`          as `country`
from `person`
left join `city`
on `person`.`city_id`=`city`.`id`
left join `county`
on `city`.`county_id`=`county`.`id`
left join `country`
on `county`.`country_id`=`country`.`id`;

insert into `country_summary`(
    `country`,
    `count_of_people`
)
select 
  `person_info`.`country`   as `country`,
  count(1)         as `count_of_people`
from `person_info`
group by `person_info`.`country`
order by count(1) desc;