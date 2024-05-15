create table if not exists "user" (
    id bigserial unique not null,
    telegram_chat_id bigint unique not null,
    telegram_username varchar,
    telegram_first_name varchar,
    telegram_last_name varchar,
    telegram_language_code varchar(2),
    created_at_utc timestamp not null,
    updated_at_utc timestamp not null
);

create index if not exists user_id_idx on "user"(id);

create index if not exists user_telegram_chat_id_idx on "user"(telegram_chat_id);
