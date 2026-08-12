import { expect, test } from "@playwright/test";

test("record page exposes camera upload flow controls", async ({ context, page }) => {
  await context.grantPermissions(["camera", "microphone"]);
  await page.goto("/record");

  await expect(page.getByRole("button", { name: "Enable Camera" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Record" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Stop & Analyze" })).toBeVisible();
});
