create table genre_configs (
  genre text primary key check (genre in ('bharatanatyam','kathak','hip_hop','freestyle')),
  posture_weight numeric not null,
  rhythm_weight numeric not null,
  spatial_tolerance text not null check (spatial_tolerance in ('strict','loose')),
  form_scale numeric not null,
  active_submodels text[] not null default '{}',
  keyframes int[] default '{}'
);

insert into genre_configs (
  genre,
  posture_weight,
  rhythm_weight,
  spatial_tolerance,
  form_scale,
  active_submodels,
  keyframes
) values
  ('bharatanatyam', 0.6,  0.4,  'strict', 0.35, '{keyframe_matcher,mudra_layer}', '{12,45,78,110}'),
  ('kathak',        0.55, 0.45, 'strict', 0.35, '{keyframe_matcher}',             '{10,40,70}'),
  ('hip_hop',       0.3,  0.7,  'loose',  0.5,  '{}',                             '{}'),
  ('freestyle',     0.3,  0.7,  'loose',  0.5,  '{}',                             '{}');
