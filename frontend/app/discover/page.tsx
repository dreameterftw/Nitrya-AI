"use client";

import { InstructionalProfileList } from "@/components/indian/InstructionalProfileList";
import { ProfileBrowser } from "@/components/western/ProfileBrowser";
import { useTheme } from "@/lib/theme-context";

const demoProfiles = [
  {
    id: "demo-hip-hop",
    dancer_name: "Hip-Hop Reference",
    genre: "hip_hop",
    reference_video_url: "",
  },
  {
    id: "demo-bharatanatyam",
    dancer_name: "Bharatanatyam Reference",
    genre: "bharatanatyam",
    reference_video_url: "",
  },
];

export default function DiscoverPage() {
  const { theme } = useTheme();

  return (
    <main>
      <h1>Discover Profiles</h1>
      {theme === "western" ? (
        <ProfileBrowser profiles={demoProfiles} />
      ) : (
        <InstructionalProfileList profiles={demoProfiles} />
      )}
    </main>
  );
}
