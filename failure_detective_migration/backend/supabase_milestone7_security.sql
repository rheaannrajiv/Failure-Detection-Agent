-- Milestone 7: secure diagnostic session ownership.
-- Run in Supabase SQL Editor after the existing supabase_schema.sql.
create table if not exists public.diagnostic_sessions (
    session_id uuid primary key,
    owner_user_id uuid null references auth.users(id) on delete cascade,
    guest_token_hash text null,
    created_at timestamptz not null default now(),
    constraint diagnostic_sessions_one_owner check (
        (owner_user_id is not null and guest_token_hash is null) or
        (owner_user_id is null and guest_token_hash is not null)
    )
);
create index if not exists diagnostic_sessions_owner_created_idx
    on public.diagnostic_sessions (owner_user_id, created_at desc);
alter table public.diagnostic_sessions enable row level security;
-- No browser-facing policies: all session ownership checks are performed by
-- the FastAPI backend using the server-only service role key.
-- Existing diagnostic_messages remains backend-only (RLS enabled, no policies).
