# Security Policy

## Supported Versions

This project is in active development on `main`. Only the latest commit on `main` is supported with security fixes.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it privately rather than opening a public GitHub issue:

1. Go to the [Security tab](https://github.com/Krysis1411/Financial-coach/security) of this repository and use "Report a vulnerability" (GitHub Private Vulnerability Reporting), or
2. Contact the maintainer directly with details of the issue.

Please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce it
- Any relevant logs, configuration, or code references

We will acknowledge reports as soon as possible and work on a fix. Please allow time for a patch to be released before disclosing publicly.

## Scope Notes

This project uses:

- A **Google Makersuite / Gemini API key** (`GOOGLE_API_KEY`) for the ADK agent — never commit this key to the repository.
- Local `.env` files for secrets — these are excluded via `.gitignore` and should never be committed.
