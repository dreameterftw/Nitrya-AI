"use client";

import { Auth } from "@supabase/auth-ui-react";
import { ThemeSupa } from "@supabase/auth-ui-shared";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { supabase } from "@/lib/supabase-client";

export default function SignupPage() {
  const router = useRouter();

  useEffect(() => {
    const { data } = supabase.auth.onAuthStateChange((event) => {
      if (event === "SIGNED_IN") router.push("/onboarding/theme");
    });
    return () => data.subscription.unsubscribe();
  }, [router]);

  return (
    <main className="auth-page">
      <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} providers={["google"]} />
    </main>
  );
}
