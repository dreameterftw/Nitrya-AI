"use client";

type Profile = {
  id: string;
  dancer_name: string;
  reference_video_url: string;
};

export function ProfileBrowser({ profiles }: { profiles: Profile[] }) {
  return (
    <div className="profile-browser">
      {profiles.map((profile) => (
        <article key={profile.id} className="profile-reel">
          <video src={profile.reference_video_url} className="profile-video" autoPlay loop muted playsInline />
          <div className="profile-overlay">
            <p>{profile.dancer_name}</p>
          </div>
        </article>
      ))}
    </div>
  );
}
