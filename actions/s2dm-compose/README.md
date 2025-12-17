# S2DM Compose Action

GitHub Action for composing GraphQL schema files and optionally creating releases.

## Features

- Compose multiple GraphQL schema files into a single schema
- Optional automated release creation with version bumping
- Automatic change detection to skip unnecessary releases
- Integration with `.bumpversion.toml` for version management

## Usage

### Basic Example (Compose Only)

Compose GraphQL schemas without creating a release:

```yaml
name: Compose Schema
on:
  push:
    branches:
      - main
    paths:
      - 'spec/**'

jobs:
  compose:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Compose GraphQL schema
        uses: COVESA/s2dm/actions/s2dm-compose@main
        with:
          repository-path: .
          spec-path: spec
```

### With Release Creation

Compose schemas and create a GitHub release when changes are detected:

```yaml
name: Compose and Release
on:
  push:
    branches:
      - main
    paths:
      - 'spec/**'

jobs:
  compose-and-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for version bumping

      - name: Compose and release
        uses: COVESA/s2dm/actions/s2dm-compose@main
        with:
          repository-path: .
          spec-path: spec
          create-release: 'true'
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Using Outputs

```yaml
- name: Compose GraphQL schema
  id: compose
  uses: COVESA/s2dm/actions/s2dm-compose@main
  with:
    repository-path: .
    spec-path: spec
    create-release: 'true'
    github-token: ${{ secrets.GITHUB_TOKEN }}

- name: Print outputs
  run: |
    echo "Schema path: ${{ steps.compose.outputs.composed-schema-path }}"
    echo "Version bump: ${{ steps.compose.outputs.version-bump }}"
    echo "Latest tag: ${{ steps.compose.outputs.latest-tag }}"

- name: Use the composed schema
  run: |
    # The schema is available at the path from the output
    cat "${{ steps.compose.outputs.composed-schema-path }}"
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `repository-path` | Path to the git repository root | Yes | - |
| `spec-path` | Path to the spec directory relative to repository root | No | `spec` |
| `create-release` | Whether to create a GitHub release | No | `false` |
| `github-token` | GitHub token for creating releases | No* | `''` |
| `s2dm-path` | Path where S2DM repository will be checked out | No | `s2dm` |

\* Required when `create-release` is `true`

## Outputs

| Output | Description |
|--------|-------------|
| `composed-schema-path` | Path to the composed schema file |
| `version-bump` | Type of version bump (major, minor, patch, none) |
| `latest-tag` | The latest git tag after release |

## Requirements

### For Basic Usage

- GraphQL schema files in the specified directory

### For Release Creation

- `.bumpversion.toml` file in the repository root
- `contents: write` permission for the workflow
- `fetch-depth: 0` when checking out the repository (for version bumping)

## How It Works

### Compose Mode (create-release: false)

1. Checks out the S2DM repository
2. Installs dependencies
3. Composes GraphQL schemas into a single file at a temporary location
4. Outputs the absolute path to the composed schema

### Compose + Release Mode (create-release: true)

1. Performs all compose mode steps
2. Validates prerequisites (`.bumpversion.toml`, `github-token`)
3. Downloads the latest release (if it exists)
4. Compares the new schema with the previous release
5. Determines version bump type (major, minor, patch, none)
6. If changes detected:
   - Bumps version using `.bumpversion.toml`
   - Pushes new tag
   - Creates GitHub release with the composed schema
7. If no changes detected:
   - Skips release creation
