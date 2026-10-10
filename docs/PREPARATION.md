# Repository preparation

Prepared on 2026-10-10 from the individual coursework copy. Original coursework files were preserved.

Changes in this copy:

- Removed the hardcoded API-key value. Configuration is read from local .env or environment variables.
- Added .env.example and .gitignore. The real key and original memory.db were not copied.
- Updated the default model identifier from the coursework's deepseek-v4-flash to deepseek-flash, as documented by DeepSeek at preparation time. Live calls were not made.
- Added a clear missing-configuration message to the Streamlit interface.
- Corrected the UI's project-root import path and retained the original UI design.
- Retained the four coursework JSON reference files, with explicit provenance and accuracy limits.
- Reduced runtime dependencies to Streamlit, the compatible API client and dotenv. Office-document generators and the unrelated utility script are not required by the app.
- Added English / Chinese readmes and offline regression checks.

AI assistance was used for repository preparation. These changes are maintenance work on the course application, not new research or performance results.

The original API key was not sent to a provider or validated. This repository does not contain it. If it was previously exposed elsewhere, revoke or rotate it through the provider.
