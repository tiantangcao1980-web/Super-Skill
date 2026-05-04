# LLM Exploration To Playwright

Use LLM/browser exploration to discover a flow, then freeze it into deterministic selectors.

## Translation Pattern

1. Record visible labels and stable roles.
2. Prefer `getByRole`, `getByLabel`, and `getByText` over brittle CSS paths.
3. Wait for user-visible state, not arbitrary time.
4. Assert the final business result.

```ts
await page.getByRole('button', { name: 'Create' }).click();
await expect(page.getByText('Created')).toBeVisible();
```
