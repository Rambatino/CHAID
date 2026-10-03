# Automatic PyPI releases from version tags

## Request

"can we fix into github actions that when you push a version tag and update the
code it auto releases to pypi"

Follow-up: "you can add the credentials into github from ~/.pypirc"

## Changes

- Added `.github/workflows/release.yml`, triggered by `v*` tag pushes and pull
  requests. Only tag pushes can reach the publishing job.
- Builds a wheel and source archive, validates their metadata with Twine,
  installs the wheel, and checks its import and version outside the checkout.
  The release tag must match the built version and its commit must be on master.
- Reuses the existing Python 3.9–3.13 test workflow through `workflow_call`.
  Publishing requires successful build and test jobs. Coverage uploads are
  omitted on tags so coverage reporting does not block a release.
- Transfers the validated distributions as a GitHub Actions artifact to a
  separate publishing job in the `pypi` environment. The build and test jobs do
  not receive the publishing token. Concurrent runs of the same ref do not
  cancel an in-progress upload.
- Stored the token from the local `.pypirc` production section as repository
  Actions secret `PYPI_API_TOKEN` using standard input. Credential values were
  not printed, written into the repository, or included in command arguments.
- Uses API-token authentication as requested. OIDC attestations are disabled
  for this authentication method; the workflow has read-only repository access.
- Documented version bumps, annotated tags, publishing prerequisites and release
  failure handling in README.md. Ordinary code pushes do not publish packages.

## Verification

- `actionlint .github/workflows/tests.yml .github/workflows/release.yml`: passed.
- `python -m build`: built `chaid-5.5.0.tar.gz` and the universal Python wheel.
- `python -m twine check dist/*`: both distributions passed, with an existing
  warning about unspecified long-description content type.
- Installed the built wheel in an isolated Python 3.13 environment; imported
  the package from site-packages outside the source checkout.
- Executed the workflow's actual version-check script: pull-request mode and
  `v5.5.0` passed; `v5.5.1` and `5.5.0` failed as expected.
- `git diff --check`: passed.
- Existing full suite: `python -m pytest -q` — 122 passed, including rendering.
- The master-ancestry guard accepted master and rejected the unmerged branch.
- GitHub secret listing confirms `PYPI_API_TOKEN` exists; its value is not
  readable through that listing.

## Remaining work and operational visibility

Merge the workflow PR before pushing a new release tag. GitHub Actions must
validate the PR's package build and existing test matrix. No release tag or
package upload was created during setup, so PyPI token scope and upload success
will be verified by the first authorized release.

Build, version-check, test and upload failures are visible as distinct Actions
steps, and the distributions are retained as a workflow artifact. This library
has no Grafana integration; no runtime metrics or logging changes are involved.
