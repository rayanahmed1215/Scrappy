# Contributing to Scrappy

Thanks for helping build Scrappy. This guide covers how we work together.

## Before your first contribution

Scrappy is licensed under the **GNU Affero General Public License v3.0 only** (see [LICENSE](LICENSE)).

Every contributor signs the [Contributor License Agreement](CLA.md) once. When you open your first pull request, a bot will comment with a link. Click it, sign in with GitHub, and you're done. Pull requests can't be merged until the CLA is signed.

In short: you keep the copyright to your code, and you allow the project to use it under the AGPL and under other licenses, such as a future paid version. Read [CLA.md](CLA.md) for the full terms, and ask the project lead if anything is unclear.

## Workflow

1. **Pick or create an issue.** All work should be tied to a GitHub Issue so the team can see who is doing what. Assign yourself before starting.
2. **Create a branch** from `main`:
   ```bash
   git checkout main
   git pull
   git checkout -b feature/short-description
   ```
   Use `feature/` for new work, `fix/` for bug fixes, and `docs/` for documentation.
3. **Commit in small steps** with clear messages, such as `Add CPU usage reporting to NodeWatch`.
4. **Open a pull request** into `main`. Link the issue it closes (for example, `Closes #12`) and describe what changed and how you tested it.
5. **Get one review.** At least one other team member must approve before merging.
6. **Merge, then delete your branch.**

Never push directly to `main`.

## License headers

Add this line at the top of every new source file:

```python
# SPDX-License-Identifier: AGPL-3.0-only
```

In Rust, use `//` instead of `#`.

## Code of conduct

Be respectful, give constructive feedback in reviews, and ask questions early. Nobody is expected to know everything, and many of us are building a distributed system for the first time.

## Questions

Ask in the team chat or open an issue labeled `question`.
