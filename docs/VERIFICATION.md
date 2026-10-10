# Verification notes

Prepared and checked on 2026-10-10.

Environment: Python 3.12.10 on Windows. Direct dependencies: streamlit 1.65.0, openai 2.54.0, python-dotenv 1.2.4.
requirements-tested.txt pins these direct dependencies; transitive packages are not locked.

## Completed

- Seven offline regression tests passed: missing-key handling; environment configuration; explicit argument precedence; configured model use; persisted preference separation; conversation separation/resumption; and a request flow with local reference lookup and stored mock reply.
- Streamlit AppTest confirmed that missing configuration produces a visible message without an uncaught exception.
- Streamlit AppTest confirmed initialization, text input and Send-button processing with a mocked model and a separate temporary database.
- Python source syntax and JSON validity were checked.
- Git staging checks confirmed that .env and user databases are ignored, while .env.example is tracked.
- The prepared source and ZIP were scanned for the original key value; it is absent. Original source hashes were unchanged.
- An unchanged interface image was extracted from slide 4 of the original coursework presentation. It is historical source material, not a new browser capture or a generated travel-plan example.

## Not performed

- Live DeepSeek requests, API-account validation, output-quality evaluation, factual accuracy checks or performance comparisons.
- Actual phone-browser testing, new browser screenshot capture or a public deployment.

Mock replies are test fixtures, not examples of real model performance. The original user database was not used.
