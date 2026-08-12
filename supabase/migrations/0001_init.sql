create table profiles (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid references auth.users(id),
  dancer_name text not null,
  genre text not null check (genre in ('bharatanatyam','kathak','hip_hop','freestyle')),
  reference_video_url text,
  pose_sequence_url text,
  created_at timestamptz default now()
);

create table attempts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  profile_id uuid references profiles(id),
  video_url text,
  score numeric,
  feedback jsonb,
  created_at timestamptz default now()
);
