create table if not exists forecast_subscription (
    id bigserial unique not null,
    user_id bigint not null,
    is_active boolean not null default true,
    created_at_utc timestamp not null,
    updated_at_utc timestamp not null
);

create index if not exists forecast_subscription_id_idx on forecast_subscription(id);

create index if not exists forecast_subscription_user_id_idx on forecast_subscription(user_id);
