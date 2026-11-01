create table if not exists public.respon_evaluasi (
    id uuid primary key default gen_random_uuid(),
    data jsonb not null check (jsonb_typeof(data) = 'object'),
    created_at timestamptz not null default now()
);

alter table public.respon_evaluasi enable row level security;

revoke all on table public.respon_evaluasi from anon, authenticated;
grant usage on schema public to service_role;
grant select, insert on table public.respon_evaluasi to service_role;
