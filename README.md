[![test-deploy](https://github.com/explorable-viz/fluid-article/actions/workflows/test-deploy.yml/badge.svg?branch=main)](https://github.com/explorable-viz/fluid-article/actions/workflows/test-deploy.yml)
[![GitHub pages](https://github.com/explorable-viz/fluid-article/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/explorable-viz/fluid-article/actions/workflows/pages/pages-build-deployment)

# fluid-article

Template repo for Fluid article websites, built with SvelteKit.

## Creating new article

1. Create new repository from this template
2. In repo Workflow Permissions settings, enable:
   - Read and write permissions
   - Create and approve pull requests
3. Once `test-deploy` workflow succeeds, configure GitHub Pages to deploy from `gh-pages` branch

## Setup

Requires [Node.js](https://nodejs.org/) >= 22.

```bash
yarn install
npx install-website article
cd website/article
yarn install
```

## Running locally

From `website/article/`:

```bash
yarn dev
```

Production-like preview:

```bash
yarn build && yarn preview
```

## Testing

From `website/article/`:

```bash
yarn test
```
