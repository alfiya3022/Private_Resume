import { expect, test } from "@playwright/test";

test("frontend can reach the FastAPI health endpoint", async ({ page }) => {
  const healthResponse = page.waitForResponse(
    (response) =>
      response.url().endsWith("/api/health") &&
      response.request().method() === "GET",
  );

  await page.goto("/");

  await page
    .getByRole("button", {
      name: "Check backend connection",
    })
    .click();

  const response = await healthResponse;

  expect(response.status()).toBe(200);

  await expect(page.getByRole("status")).toHaveText("Backend response: ok");
});
