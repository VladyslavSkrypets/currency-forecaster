create table if not exists currency (
    id bigserial unique not null,
    sell numeric(16, 2) not null,
    buy numeric(16, 2) not null,
    created_at timestamp not null
);

create index if not exists currency_id_idx on currency(id);

create index if not exists currency_external_created_at_idx on currency(created_at);


create table if not exists trained_model (
    id bigserial unique not null,
    model bytea not null,
    mse numeric(16, 2) not null,
    training_params jsonb not null,
    created_at timestamp not null default current_timestamp
);

create index if not exists trained_model_id_idx on trained_model(id);
