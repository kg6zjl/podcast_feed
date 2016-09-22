-- Schema for podcast_app.

create table podcast_items
(
    id                  integer primary key autoincrement not null,
    itunes_subtitle     varchar(255),
    itunes_author       varchar(255),
    pubDate             varchar(255),
    title               varchar(255),
    itunes_image        varchar(255),
    enclosure_length    varchar(255),
    itunes_explicit     varchar(255),
    enclosure_url       varchar(255),
    link                varchar(255),   
    guid                varchar(255),   
    dc_creator          varchar(255),
    itunes_duration     varchar(255), 
    enclosure_type      varchar(255)
);

CREATE UNIQUE INDEX IF NOT EXISTS uniquepodcasts ON podcast_items (title,enclosure_url);
CREATE UNIQUE INDEX IF NOT EXISTS unique_guid_url ON podcast_items (guid);

-- create table podcast_channel (
--     id           integer primary key autoincrement not null,
--     priority     integer default 1,
--     details      text,
--     status       text,
--     deadline     date,
--     completed_on date,
--     project      text not null references project(name)
-- );