create extension if not exists "uuid-ossp";
create table if not exists site_avail_stats (
    id uuid primary key default uuid_generate_v4(),
    ts timestamp with time zone not null default now(),
    url text not null,
    response_time_ms int not null,
    http_status_code int not null,
    regexp text,
    regexp_matched bool
);
