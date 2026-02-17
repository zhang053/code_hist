# Repository Guidelines

## Project Structure & Module Organization
The codebase is intentionally split by learning track: SelfStudy/basics collects numbered Python fundamentals (a##_* scripts plus Graph.py utilities), SelfStudy/spider holds practical crawlers, JS helpers, and assets, while SelfStudy/playwright课件 stores Playwright study notes. Production-style experiments live under WORK/w01_XiaoHongShu, and generated browser profiles (pw_user_data/) plus env_forStudy/ and 
ode_modules/ are runtime artifacts that should stay untracked.

## Build, Test, and Development Commands
Activate the curated interpreter before running scripts: .\venv_forStudy\Scripts\activate. Install Python needs ad hoc with pip install playwright requests pillow and record them via pip freeze > requirements_work.txt near the script you touched. JS helpers require 
pm install once (see package.json / crypto-js). Typical entry points are python SelfStudy/spider/sp2600_multiplePages.py for crawling demos and python WORK/w01_XiaoHongShu/get_comments.py --note-id <id> for the XiaoHongShu pipeline; JS-only encryptors can be verified with 
ode SelfStudy/spider/sp2003_ParamsReverse.js.

## Coding Style & Naming Conventions
Follow PEP 8: 4-space indents, snake_case for variables/functions, and PascalCase for classes; keep numbered prefixes (a##, sp####) so lessons stay chronologically ordered. Use f-strings, type hints on new modules, and guard runnable files with if __name__ == "__main__":. JavaScript snippets should stay CommonJS (matching current equire usage) with camelCase helpers and descriptive log output.

## Testing Guidelines
While no suite exists yet, add smoke tests whenever you stabilize a crawler or data utility. Prefer pytest and place files beside the code as 	est_<module>.py (e.g., SelfStudy/spider/test_sp2600_multiplePages.py) or group them in a 	ests/ sibling when sharing fixtures. Use frozen HTML/JSON samples under spider/tests/data/ to avoid live traffic, and gate merges on pytest SelfStudy -k sp2600 running cleanly.

## Commit & Pull Request Guidelines
Recent history mixes Conventional Commits (chore: update gitignore) with concise Chinese summaries; keep either format but lead with a clear type (eat|fix|docs|chore) and optionally append the module scope (spider, WORK). Commits should bundle one logical change and mention affected scripts in the body. Pull requests need: problem statement, reproduction or command samples, expected output snapshots (e.g., snippet from esult_comments.json), and any data sanitization steps. Link GitHub issues when available and note required credentials.

## Security & Data Handling
Never commit personal artifacts under WORK/w01_XiaoHongShu/pw_user_data or large checkpoint/result JSON files—refresh .gitignore instead. Scrub cookies, API keys, and user identifiers from examples, and keep sample payloads anonymized before sharing in documentation or PRs.
