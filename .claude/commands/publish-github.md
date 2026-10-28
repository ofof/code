---
description: Publish this project to GitHub (push, README, About, Pages, CI/CD) after a secrets check
argument-hint: <owner/repo or https://github.com/owner/repo>
---

Publish this project to the GitHub repo given in `$ARGUMENTS`. If it is empty, ask the user for the repo (owner/name or URL) before doing anything else. Work through the steps in order and report what each one did.

## 0. Preflight
- Normalise the repo to `owner/name`. Confirm `git` is initialised and an identity is set (`git config user.name` / `user.email`); if not, ask the user for them. Never invent an email.
- Check `gh auth status`. If `gh` is missing or not logged in, stop and tell the user to install it and run `gh auth login` themselves. Never ask for, accept or type a password or token, and never put credentials in a remote URL.
- Check whether the repo exists (`gh repo view`). If it does not, ask before creating it, and ask whether it should be public or private.

## 1. Make sure nothing sensitive goes online (do this before any push)
- Read `git status` and the tracked/untracked file list. Scan every file that would be pushed, and the full git history if commits already exist (`git log -p`), for: API keys, tokens, passwords, private keys, `.env` files, credentials JSON, connection strings, cloud keys, personal emails or phone numbers, internal hostnames and IPs.
- Make sure `.gitignore` covers `.env*`, `*.pem`, `*.key`, virtualenvs (`.venv/`), `node_modules/`, caches, build output, and editor/OS junk. Add what is missing.
- Do not stage `.claude/settings.local.json` or anything else that holds local-only settings.
- If anything sensitive is found, stop. List each finding (file and line, never the secret value), remove it from the working tree and ask the user how to proceed. Anything already in history needs a history rewrite and a key rotation, so tell the user and wait for a decision.
- Show the user the exact list of files to be pushed and the repo visibility, and get an explicit yes before the first push.

## 2. README
- Create or update `README.md` from what the code actually does: title, one-paragraph summary, features, how to install and run, how to test, project layout if non-obvious, and the live Pages link once it exists (step 5). Keep any existing sections the user wrote; edit in place rather than overwrite.
- Do not invent features, badges or claims.

## 3. Push
- Set `origin` to `https://github.com/<owner/name>.git` (update it if it differs), name the branch `main`, commit the changes with a clear message, and `git push -u origin main`.
- Do not force-push. If the push is rejected, report why and ask.

## 4. CI/CD with GitHub Actions
- Detect the stack (Python: `requirements.txt`/`pyproject.toml`; Node: `package.json`; static site: `index.html`) and create or update `.github/workflows/ci.yml` to install dependencies and run the project's tests or lint. If there are no tests, run a basic check (syntax/build) and say so.
- If the project is a static site, add `.github/workflows/pages.yml` that deploys to GitHub Pages with the official `actions/configure-pages`, `actions/upload-pages-artifact` and `actions/deploy-pages` actions, with the minimal `permissions` block they need.
- Pin actions to a major version tag. Never write secrets into workflow files; reference `${{ secrets.NAME }}` and tell the user which secrets to add in the repo settings.
- Commit and push the workflows, then check the first run with `gh run list` / `gh run watch` and report the result.

## 5. GitHub Pages
- If the project has a static front end (`index.html` at the root or in `docs/`), enable Pages with GitHub Actions as the source (`gh api -X POST repos/<owner/name>/pages -f build_type=workflow`, or update it with PUT if it already exists) and wait for the first deploy.
- If it is a backend-only project (for example a FastAPI service), Pages cannot run it: publish a simple `docs/index.html` landing page generated from the README (and OpenAPI docs if available) instead, and say that it is documentation only.
- Get the live URL from `gh api repos/<owner/name>/pages --jq .html_url`.

## 6. About section
- Set the repo description, topics and homepage with `gh repo edit <owner/name> --description "..." --add-topic ... --homepage <pages-url>`. The description is one short line taken from the README summary; topics are 3 to 6 relevant lowercase terms. Set the homepage to the Pages link from step 5, and add that link to the README as well.

## Finish
Report: repo URL, Pages URL, CI status, what the secrets scan checked and found, and anything the user must still do (adding secrets, enabling a setting that needs admin rights). If a step could not be completed, say which and why instead of skipping it quietly.
