"use client";

type Profile = {
  id: string;
  dancer_name: string;
  genre?: string;
};

export function InstructionalProfileList({ profiles }: { profiles: Profile[] }) {
  return (
    <div className="instructional-list">
      {profiles.map((profile) => (
        <article key={profile.id} className="instructional-row">
          <h2>{profile.dancer_name}</h2>
          <p>{profile.genre ?? "Indian classical"}</p>
        </article>
      ))}
    </div>
  );
}
