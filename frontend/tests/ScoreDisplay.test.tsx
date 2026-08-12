import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { ScoreDisplay } from "@/components/ScoreDisplay";

describe("ScoreDisplay", () => {
  test("renders score as rounded percentage", () => {
    render(<ScoreDisplay score={0.847} theme="western" />);

    expect(screen.getByText("85%")).toBeTruthy();
  });
});
