# Releasing compounder

Two branches matter. `main` is where work lands and where the site deploys from. `release` is what
the Claude plugin directory follows: a commit reaches the directory only when it is merged into
`release`. Every release also gets a `vX.Y.Z` tag on that merge commit.

## Everyday change

1. Branch from `main` and open a PR into `main`. The **Check plugin** workflow runs the directory
   checks that work offline (`claude plugin validate --profile directory --strict`), the btw hook
   cases, the changelog tests and a site stamp dry run.
2. If the PR touches `compounder/`, also run the directory's own Validate on the PR branch: in
   claude.ai/directory/manage, Submit new → Plugin bundle → Source, path `compounder`, Branch or tag
   = the PR branch → Validate, then Start over without saving. The portal runs checks the CLI does
   not, such as whether it can follow the hook's script.
3. Merge. Nothing reaches the directory yet.

## Release

1. One PR into `main` raises `version` in `compounder/.claude-plugin/plugin.json` and adds the
   matching `## [X.Y.Z] — YYYY-MM-DD` entry at the top of `compounder/CHANGELOG.md`. The site
   deploy refuses a version without its changelog entry.
2. Open a PR from `main` into `release` and merge it with a merge commit. The workflow fails the
   PR if the version did not change or its tag already exists.
3. Tag the merge commit and push the tag:
   `git fetch origin && git tag -a vX.Y.Z origin/release -m "compounder X.Y.Z" && git push origin vX.Y.Z`
4. The directory picks up the new commit on `release` (push webhook, or **Check for new commits**
   on the plugin's page) and publishes it according to the plugin's publish setting.

One version per release, never one per fix: iterate on the PR branch until the portal's Validate
is clean, then release once.
