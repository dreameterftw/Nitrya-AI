import Link from "next/link";

const starterProfiles = [
  { id: "starter-bharatanatyam", name: "Bharatanatyam Starter", genre: "bharatanatyam" },
  { id: "starter-kathak", name: "Kathak Starter", genre: "kathak" },
  { id: "starter-hip-hop", name: "Hip-Hop Starter", genre: "hip_hop" },
  { id: "starter-freestyle", name: "Freestyle Starter", genre: "freestyle" },
];

export default function ProfileStepPage() {
  return (
    <main>
      <h1>Choose a starter profile</h1>
      <div className="instructional-list">
        {starterProfiles.map((profile) => (
          <article className="instructional-row" key={profile.id}>
            <h2>{profile.name}</h2>
            <p>{profile.genre}</p>
            <Link href={`/record?profileId=${profile.id}`}>Try this profile</Link>
          </article>
        ))}
      </div>
    </main>
  );
}
