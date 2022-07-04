create table problem
(
    uid        varchar,
    site       varchar,
    title      varchar,
    tags       set<varchar>,
    time_step  timestamp,
    contest_id int,
    id         int,
    code       varchar,
    difficulty int,
    solved     int,
    total      int,
    primary key ((uid), time_step)
);

create table problem_by_tag
(
    tag        varchar,
    uid        varchar,
    time_step  timestamp,
    site       varchar,
    title      varchar,
    difficulty int,
    solved     int,
    total      int,
    primary key ( (tag), uid, time_step )
);

create materialized view problem_by_tag_difficulty as
select *
from problem_by_tag
where tag is not null
  and difficulty is not null
  and uid is not null
  and time_step is not null
primary key ( tag, difficulty, uid, time_step )
with clustering order by (difficulty desc, uid asc, time_step desc);

create materialized view problem_by_tag_solved as
select *
from problem_by_tag
where tag is not null
  and solved is not null
  and uid is not null
  and time_step is not null
primary key ( tag, solved, uid, time_step )
with clustering order by (solved desc, uid asc, time_step desc);

create materialized view problem_by_tag_total as
select *
from problem_by_tag
where tag is not null
  and total is not null
  and uid is not null
  and time_step is not null
primary key ( tag, total, uid, time_step )
with clustering order by (total desc, uid asc, time_step desc);

create materialized view problem_by_site as
select *
from problem
where site is not null
  and uid is not null
  and time_step is not null
primary key ( (site), uid, time_step );

create materialized view problem_by_site_tag as
select *
from problem_by_tag
where site is not null
  and tag is not null
  and uid is not null
  and time_step is not null
primary key ( (site, tag), uid, time_step );
