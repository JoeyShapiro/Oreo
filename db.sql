-- auto-generated definition
create table hooks
(
    id          integer                               not null
        primary key autoincrement
        unique,
    channel     varchar(256)                          not null,
    platform_id integer                               not null,
    hook_type   varchar(64)                           not null,
    message     varchar(2048)                         not null,
    creator     varchar(128),
    created     datetime    default CURRENT_TIMESTAMP not null,
    uuid        varchar(36) default unknown           not null
);

-- auto-generated definition
create table platforms
(
    id   integer      not null
        primary key autoincrement
        unique,
    name varchar(128) not null
        unique
);

create table followers
(
    id          integer      not null
        primary key autoincrement
        unique,
    username    varchar(128) not null,
    hook_id     integer      not null -- this lets someone choose what they want to know, rather than channel name
);
