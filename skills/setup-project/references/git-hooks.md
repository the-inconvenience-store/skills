# Git hooks

Hooks are the **fast** gate. CI is the real one. Anything here that takes long enough to be annoying gets bypassed with `--no-verify` within a week, and a bypassed hook is worse than no hook, because everyone believes it ran.

So the budget comes first: **pre-commit under about five seconds**. Measure it in the prove step, and if it's over, move work to `pre-push` or CI rather than asking people to wait.

Every hook below is independently optional. Ask about each; install the ones the user takes.

## Docs to read before configuring

Read the docs for **whichever manager the user picks** — not all of them.

| Read | For |
| --- | --- |
| <https://typicode.github.io/husky/get-started.html> | husky: install, `init`, hook file format |
| <https://github.com/lint-staged/lint-staged> | Staged-file config format and current option names |
| <https://commitlint.js.org/guides/local-setup.html> | Wiring commitlint into the `commit-msg` hook |
| <https://www.conventionalcommits.org/en/v1.0.0/> | The commit format, if the user wants to see what they're agreeing to |
| <https://lefthook.dev/configuration/> | lefthook: `lefthook.yml`, `{staged_files}`, `stage_fixed`, parallel runs |
| <https://github.com/toplenboren/simple-git-hooks> | simple-git-hooks: the `package.json` key and the reinstall caveat |
| <https://pre-commit.com/#plugins> | pre-commit: `.pre-commit-config.yaml` repos and hook entries |
| <https://github.com/sds/overcommit#configuration> | Overcommit: `.overcommit.yml` |
| <https://github.com/voidzero-dev/vite-plus> | Vite+: `vp config`, `vp staged`, `vp migrate` |

Hook file formats churn — husky's `#!/usr/bin/env sh` + `. "$(dirname -- "$0")/_/husky.sh"` preamble is gone in v9+, and writing it from memory produces a hook that fails on every commit. Read the current docs.

## Put the logic in scripts, not in the manager

Before picking a manager, decide the shape — and the shape should make the manager barely matter.

Every manager below does the same job: get git to run a command at a lifecycle point. What differs is only the config syntax. So **write each hook's logic as a script in the repo** (`scripts/hooks/pre-commit.sh` and friends) and let the manager do nothing but point at it. Two things follow:

- Switching managers becomes a two-line change instead of a rewrite. That matters more than it sounds — hook managers are the most-churned dev dependency in a JS repo.
- The hook is runnable by hand. `./scripts/hooks/pre-commit.sh` is how you debug it, and how the prove step exercises it without making commits.

Everything below is written as a command. Where a manager has a genuinely better native idiom for staged files, it is noted.

## Pick the manager

Ask the user. Lead with the default, and skip the question entirely if the repo already has one.

**Default: [husky](https://typicode.github.io/husky/) + [lint-staged](https://github.com/lint-staged/lint-staged)** where a `package.json` exists. It is the one most people have seen, `husky init` does the setup, and the `prepare` script installs hooks on a teammate's clone with no extra instruction.

| Manager | Config | Reach for it when |
| --- | --- | --- |
| **husky** | `.husky/<hook>`, `prepare` script | **Default** for any repo with Node |
| **`core.hooksPath`** | `.githooks/<hook>` + `git config core.hooksPath .githooks` | No manager at all. Zero dependencies, works in any language — the cost is that every clone must run the `git config` line, which people forget |
| **[lefthook](https://github.com/evilmartians/lefthook)** | `lefthook.yml` | Go-only or polyglot repos, and monorepos. Single binary, no Node needed, parallel execution, and `{staged_files}` replaces lint-staged |
| **[simple-git-hooks](https://github.com/toplenboren/simple-git-hooks)** | `simple-git-hooks` key in `package.json` | You want husky's job in ~1 KB with zero dependencies. Note it does **not** auto-reinstall on config change — someone must re-run `npx simple-git-hooks` |
| **[Vite+](https://github.com/voidzero-dev/vite-plus)** (`vp`) | `.vite-hooks/` + `staged` in `vite.config.ts` | The project already uses Vite+. `vp config` installs the dispatcher, `vp staged` is its lint-staged. `vp migrate` converts an existing husky/lint-staged setup |
| **[pre-commit](https://pre-commit.com)** | `.pre-commit-config.yaml` | The repo is Python-leaning or polyglot-with-Python. It manages each tool's own environment, which no JS manager does |
| **[Overcommit](https://github.com/sds/overcommit)** | `.overcommit.yml` | The repo is Ruby |
| **yorkie / ghooks / git-hooks-js** | varies | **Legacy only.** All unmaintained — yorkie and ghooks last released in 2018, and yorkie is a husky fork carried by older Vue CLI projects. If one is already installed, add to it rather than migrating unasked; say in the report that it is unmaintained |

Two things on that list that are **not** hook managers, and get placed accordingly:

- **`core.hooksPath`** is the git primitive every manager on this list drives. Listing it as an option means "no manager" — write the scripts, point git at the directory, done.
- **[pretty-quick](https://github.com/prettier/pretty-quick)** is a staged-file runner, not a manager: it is a peer of `lint-staged` and `vp staged`, and it only runs Prettier. Reach for it in place of lint-staged when formatting is genuinely the only thing the hook does; the moment you also want lint or typecheck, lint-staged is the one that handles both.

**An existing manager wins.** If `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`, `.overcommit.yml`, a `simple-git-hooks` key, or a set `core.hooksPath` is already there, do not install a second one — two managers fighting over `.git/hooks` produces hooks that silently stop running. Add to what exists, translate the commands below into its syntax, and say so in the report.

## Install and wire

The four hooks are defined in the sections after this. Whichever manager, the wiring is the same three steps: install the manager, point each lifecycle point at the corresponding script, and make sure a fresh clone gets the hooks.

That last step is where every manager leaks, and it is worth checking explicitly:

```bash
# husky — `prepare` runs on install, so a clone + install is enough
<pm> add -D husky lint-staged && npx husky init
```

```yaml
# lefthook.yml — commit this; a fresh clone needs `lefthook install` once
pre-commit:
  commands:
    staged:
      run: ./scripts/hooks/pre-commit.sh
commit-msg:
  commands:
    conventional:
      run: ./scripts/hooks/commit-msg.sh {1}
post-merge:
  commands:
    deps:
      run: ./scripts/hooks/post-merge.sh
```

```jsonc
// package.json — simple-git-hooks. Re-run `npx simple-git-hooks` after ANY change here
{
  "simple-git-hooks": {
    "pre-commit": "./scripts/hooks/pre-commit.sh",
    "commit-msg": "./scripts/hooks/commit-msg.sh $1",
    "post-merge": "./scripts/hooks/post-merge.sh"
  },
  "scripts": { "prepare": "simple-git-hooks" }
}
```

```bash
# core.hooksPath — no manager. Each clone must run the config line.
mkdir -p .githooks && git config core.hooksPath .githooks
# then .githooks/pre-commit is a two-line shim: #!/bin/sh + exec ./scripts/hooks/pre-commit.sh "$@"
```

For `pre-commit` and Overcommit, read their docs — both express hooks as declarative entries rather than raw commands, and both manage tool environments themselves, so translating the sections below means expressing each check as one of their hook entries rather than shelling out. Vite+ is its own case: `vp config` sets up the dispatcher and `vp staged` reads the `staged` section of `vite.config.ts` in place of lint-staged.

**Verify the fresh-clone path.** Clone to a temp directory, install, and confirm the hooks are live. A hook set that works only on the machine that created it is the single most common failure here, and it is invisible until someone else's bad commit lands.

Every script gets `chmod +x`. A non-executable hook fails silently in most managers.

## pre-commit — format and lint staged files

Two jobs, in that order: **fix what can be fixed, then report what can't.** Formatting and autofixable lint findings should never reach a human, because a human reading a diff full of whitespace churn stops reading diffs.

The formatter is the one from Section C, and the same tool serves all three places it's needed — here as the **fix** command, in CI as the **check** command, and optionally in the agent's edit loop:

| Ecosystem | Fix (hook) | Check (CI) |
| --- | --- | --- |
| TypeScript / JS / CSS / JSON / MD | `prettier --write`, or `oxfmt` | `prettier --check`, or `oxfmt --check` |
| Go | `golangci-lint fmt` | `golangci-lint fmt --diff` |
| Biome, if already in use | `biome check --write` | `biome check` |

If the project has no formatter at all, one gets installed here — that is Section C's decision, not one to make silently in the hook. If it already has one, keep it; migrating formatters rewrites the whole repo and buys nothing.

```bash
# scripts/hooks/pre-commit.sh — the manager points here
npx lint-staged
```

```jsonc
// package.json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": ["oxlint --fix", "prettier --write"],
    "*.{json,css,md}": ["prettier --write"]
  }
}
```

Staged files only — linting the whole repo on every commit is how the five-second budget dies. `--fix` means the autofixable rules (import sorting, Tailwind class order, `prefer-const`) never reach a human at all.

Order matters: `oxlint --fix` before the formatter, so the formatter gets the last word on layout. Run them the other way and the linter's fixes arrive unformatted.

If Tailwind is in play, `prettier-plugin-tailwindcss` and `oxlint-tailwindcss`'s `enforce-sort-order` must read the **same CSS entry point**, or the two rewrite each other's class order on every commit.

### Go

golangci-lint gives you both halves — `fmt` autofixes, `run` reports — so the hook does the same two steps as the TypeScript one.

The wrinkle is that the two commands take different arguments. `golangci-lint fmt` takes **files**; `golangci-lint run` analyses **packages**, and mixing files from different packages in one invocation is an error. So format the staged files, then lint the directories those files live in:

```sh
# scripts/hooks/pre-commit.sh — Go branch
files=$(git diff --cached --name-only --diff-filter=ACMR -- '*.go')
[ -z "$files" ] && exit 0

# shellcheck disable=SC2086
golangci-lint fmt $files
git add $files

dirs=$(printf '%s\n' $files | xargs -n1 dirname | sort -u)
# shellcheck disable=SC2086
golangci-lint run $dirs
```

`git add` after `fmt` is what makes the autofix reach the commit rather than sitting in the working tree as an unstaged diff — without it the commit lands unformatted and the next `git status` is confusing.

The lefthook equivalent, which handles the staged-file plumbing for you:

```yaml
# lefthook.yml
pre-commit:
  parallel: false
  commands:
    fmt:
      glob: "*.go"
      run: golangci-lint fmt {staged_files}
      stage_fixed: true
    lint:
      glob: "*.go"
      run: golangci-lint run {staged_files}
```

`stage_fixed: true` is lefthook's version of the `git add` above.

Two things to check in the prove step. First, that **`golangci-lint run` on a subset of directories is fast enough** — most of its cost is loading type information, so a small diff is quick but a diff touching a widely-imported package is not. Time it; if it blows the budget, move `run` to `pre-push` and keep only `fmt` on `pre-commit`, which is nearly free. Second, that the advisory budget pass (if `go.md`'s second-pass option was taken) is **not** in the hook — it does not block, so running it here only costs time.

## pre-commit — typecheck

**Go needs no separate step.** `golangci-lint run` already loads full type information — `staticcheck` and friends can't work without it — so a passing lint is a passing typecheck. Adding `go build ./...` to the hook pays for the same work twice. Skip this section for a Go-only repo.

TypeScript cannot meaningfully typecheck a subset of files: types cross file boundaries, so a staged-file typecheck reports errors that aren't real and misses ones that are. It's the whole project or nothing.

```bash
# scripts/hooks/pre-commit.sh
npx lint-staged
<pm> run typecheck
```

**Time it before committing to it.** `tsc --noEmit` on a large repo is tens of seconds, which blows the budget outright. The branches, in order of preference:

- **Fast enough** (small or mid-size repo, or `tsc --incremental` with a warm cache) → leave it in `pre-commit`.
- **Too slow** → move it to `pre-push`, where a multi-second wait is expected.
- **Far too slow** (monorepo, minutes) → CI only, and say so in the report so nobody assumes local coverage.

Measure, then pick. Don't guess from repo size.

## commit-msg — Conventional Commits

```bash
<pm> add -D @commitlint/cli @commitlint/config-conventional
```

```js
// commitlint.config.js
export default { extends: ["@commitlint/config-conventional"] };
```

```bash
# scripts/hooks/commit-msg.sh — receives the message file as $1
npx --no -- commitlint --edit "$1"
```

Use `commitlint.config.cjs` with `module.exports` if the package is not `"type": "module"`.

**Without Node**, don't add a `package.json` just to run commitlint — a regex in the hook covers the format at a fraction of the cost:

```sh
# scripts/hooks/commit-msg.sh — no-Node variant
pattern='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9/_-]+\))?!?: .{1,72}$'
head -1 "$1" | grep -qE "$pattern" && exit 0
grep -qE '^(Merge|Revert|fixup!|squash!)' "$1" && exit 0
echo "Commit message must follow Conventional Commits, e.g. 'fix(api): handle empty cursor'"
exit 1
```

The second `grep` is load-bearing: git generates merge, revert, and `--fixup` messages itself, and a hook that rejects them makes ordinary git operations fail for no reason. This checks the format only — it won't catch the subtler things commitlint does, which is the trade for having no Node dependency.

This is the cheapest hook here — it runs in milliseconds and never blocks on a slow toolchain — and the one with the most downstream value: conventional messages are what let `semantic-release` or `changesets` derive versions and changelogs without anyone writing them.

The default types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Offer `scope-enum` in a monorepo, pinned to the workspace package names, so a commit says which package it touched:

```js
export default {
  extends: ["@commitlint/config-conventional"],
  rules: { "scope-enum": [2, "always", ["api", "web", "ui", "config"]] },
};
```

Generate the scope list from the workspace packages found in step 1. Say in the conventions doc that adding a package means adding its scope.

## pre-push — the fuller check

Optional, and worth offering when the typecheck got pushed out of `pre-commit`:

```bash
# scripts/hooks/pre-push.sh
<pm> run typecheck
<pm> run test
```

Go:

```sh
# scripts/hooks/pre-push.sh — Go
golangci-lint run ./...      # whole module, if pre-commit only linted the diff
go test -race ./...
```

A push is already a pause, so a few seconds here costs nothing. Tests belong here rather than `pre-commit` — a test suite in a commit hook is the single most reliable way to get everyone using `--no-verify`. For Go, `-race` is what makes the run worth waiting for: it finds the concurrency bugs no linter can, and it needs the tests to actually execute.

## post-merge — keep dependencies fresh

On by default wherever the language has a lockfile. When a merge or pull brings in a changed one, the working tree's dependencies are stale until someone remembers to install.

The reason this earns a hook is that the failure it prevents **points nowhere near its cause**. A missing dependency surfaces as a module-not-found from a file nobody touched; a stale one surfaces as a type error, a runtime error, or nothing at all until a subtly different version behaves differently. Either way the next hour goes into debugging code that is fine. An agent picking the work up fares worse than a human, because "did you pull?" is not in its differential.

Guard on the lockfile actually changing, so a merge that touched no dependencies costs nothing:

```sh
# scripts/hooks/install-if-lockfile-changed.sh
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -q '^pnpm-lock\.yaml$'; then
  echo "Lockfile changed — installing dependencies"
  pnpm install --frozen-lockfile
fi
```

```sh
# scripts/hooks/post-merge.sh
. "$(dirname "$0")/install-if-lockfile-changed.sh"
```

Match the lockfile name and install command to the detected ecosystem, and use the **frozen** flag so the hook installs exactly what the lockfile says rather than quietly rewriting it:

| Ecosystem | Watch | Run |
| --- | --- | --- |
| pnpm | `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` |
| yarn | `yarn.lock` | `yarn install --immutable` |
| bun | `bun.lock` | `bun install --frozen-lockfile` |
| npm | `package-lock.json` | `npm ci` |
| Go | `go.sum`, `go.mod` | `go mod download` |

`npm ci` deletes and rebuilds `node_modules` — on a large project that is slow enough to be worth `npm install` instead, at the cost of letting the lockfile drift.

Go's version is cheaper and quieter: `go mod download` populates the module cache and is a no-op when everything is already there, so it can run unconditionally if the guard feels like more machinery than it's worth. The guard still earns its place in a polyglot repo, where the same script decides between several ecosystems.

**`post-merge` does not cover every way a lockfile arrives.** It fires on `git merge` and on a plain `git pull` — not on `git pull --rebase`, and not on `git checkout`. Reuse the same script for full coverage:

```sh
# scripts/hooks/post-rewrite.sh   (rebases, including git pull --rebase)
. "$(dirname "$0")/install-if-lockfile-changed.sh"
```

Branch switching needs a different diff range, since `post-checkout` is passed the previous and new HEAD as `$1` and `$2`:

```sh
# scripts/hooks/post-checkout.sh   — $3 is 1 for a branch checkout, 0 for a file checkout
[ "$3" = "1" ] || exit 0
if git diff-tree -r --name-only --no-commit-id "$1" "$2" | grep -q '^pnpm-lock\.yaml$'; then
  pnpm install --frozen-lockfile
fi
```

Offer `post-checkout` separately — it fires on every branch switch, and on a repo where people hop branches constantly the surprise install is more irritating than the stale `node_modules` it prevents. `post-merge` and `post-rewrite` are the pair worth taking by default.

In a monorepo the guard should match every lockfile in the workspace, and the install runs at the workspace root — `pnpm install` at the root installs for all packages, so there is nothing per-package to do.

Say in the report that this hook exists. An install that starts on its own after a pull looks like something has gone wrong if nobody was told to expect it.

## Report and document

Two things go in the conventions doc, both because agents need them and neither is discoverable from config:

- **The commit format**, with one real example: `feat(api): add cursor pagination to /discussions`.
- **The escape hatch.** `git commit --no-verify` exists, and pretending otherwise just means it gets discovered and used silently. Document it as being for a genuine emergency, with CI as the backstop that still catches what was skipped.

In the report, state the measured `pre-commit` duration and which checks run where — `pre-commit`, `pre-push`, or CI only. A user who thinks typechecking runs locally when it doesn't will find out at the worst moment.
