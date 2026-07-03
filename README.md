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

## Adding a new Fluid figure

This section documents how to add a new figure to the site, using the CO₂ example as reference.

### 1. Prepare the data

Place your dataset under `dataset/`.
The output JSON should use **plain alphabetic field names** — avoid names starting with or containing digits (e.g. use `ppm` not `co2`), as the Fluid parser treats `.co2` as field `.co` followed by integer `2`.

### 2. Write the Fluid `.fld` files

Place `.fld` files under `fluid/`. Split data loading from the figure definition:

**`fluid/co2_data.fld`** — loads data, defines a single variable:
```
def co2: load_json("../dataset/co2_mm_mlo.json")
```

**`fluid/co2.fld`** — imports the data file and defines the figure:
```
import co2_data

def n: length(co2)
def ppm_vals: [row.ppm for row in co2]
def x_vals: [row.year + (row.month - 1) / 12 for row in co2]

def raw_series: [{ x: nth(i, x_vals), y: nth(i, ppm_vals) } for i in [0 .. n - 1]]

LineChart({
   size: { width: 600, height: 330 },
   ...
})
```

Key Fluid syntax rules (learned from this project):
- Definitions use `def name:` or `def name(args):`, **not** `let ... in`
- List comprehensions use `[expr for x in list if cond]`, **not** `| x <- list, cond`
- Range syntax is `[0 .. n - 1]`, **not** `range(0, n)`
- Charts and plots use `()` not `{}`: `LineChart({...})`, `LinePlot({...})`
- `inputs` in the Svelte spec lists variables defined in *imported* data `.fld` files; leave it `[]` if the figure loads its own data

### 3. Symlink `.fld` files into `static/`

The dev server and build only serve files from `website/article/static/`. Use symlinks so edits to source files are reflected immediately:

```bash
cd website/article/static/fluid
ln -s ../../../../fluid/co2.fld co2.fld
ln -s ../../../../fluid/co2_data.fld co2_data.fld
```

Copy (not symlink) JSON data files, since they are regenerated:

```bash
cp dataset/co2_mm_mlo.json website/article/static/dataset/co2_mm_mlo.json
```

### 4. Create the SvelteKit route

Create `website/article/src/routes/co2/+page.svelte`:

```svelte
<script>
  import { DataPane, Figure, Grid } from '@explorable-viz/fluid';

  let showDataPane = false;

  const spec = {
    fluidSrcPath: ['../fluid'],
    inputs: [],
    query: false,
    linking: false
  };

  const toggleDataPane = () => { showDataPane = !showDataPane; };
</script>

<Grid {showDataPane}>
  <div></div>
  <div></div>
  <div class="flex-left-align"><h3>My Figure</h3></div>

  <DataPane {showDataPane} toggle={toggleDataPane}>
    <div id="fig-data-pane" class="flex-right-align data-pane">
      <div id="fig-input" class="data-pane-column"></div>
    </div>
  </DataPane>

  <div class="flex-left-align">
    <Figure {spec} fld="../fluid/co2.fld" />
  </div>
</Grid>
```

### 5. Build and deploy

The `gh-pages` branch is the deployed static site — the repo root *is* the built output. To publish:

```bash
cd website/article
BASE_PATH=/your-repo-name yarn build
cp -r build/co2 ../../
cd ../..
git add co2/index.html fluid/co2.fld fluid/co2_data.fld dataset/co2_mm_mlo.json
git commit -m "add co2 figure"
git push
```

Replace `BASE_PATH` with your GitHub Pages base path (typically `/<repo-name>`).
