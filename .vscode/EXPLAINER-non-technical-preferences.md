# Workspace: Non-technical explanation preferences

This workspace contains a small, custom workspace setting to help assistants provide answers tailored for non-technical users.

Settings added:

- "user.prefersNonTechnicalExplanations": true
  - Purpose: instruct any assistant or integrated tool to give plain-language explanations, describe benefits, pros/cons, and simple next steps.

- "user.background": "non-IT"
  - Purpose: short hint to indicate the user does not have an IT or coding background.

How this affects suggestions you receive

- Explanations will: use plain language (no jargon), include a short "what it does", "why you might want it", and "pros/cons" for each recommendation.
- Where a command or code change is suggested, the assistant will also include simple step-by-step guidance and one-line commands where appropriate.
- If a suggestion has risk (e.g., modifying many files, running installation scripts), the assistant will highlight the risks and provide a safer alternative.

How to change these preferences

1. Open the workspace settings file: `.vscode/settings.json`.
2. Edit the values:
   - Set `"user.prefersNonTechnicalExplanations"` to `false` if you prefer short/technical answers.
   - Set `"user.background"` to `"IT"` or remove the key if you don't want background hints.
3. Save the file. Assistants and extensions that read workspace settings should adapt automatically.

If you want, I can also add these preferences to a README in the project root or create a small VS Code recommended-extensions hint.
