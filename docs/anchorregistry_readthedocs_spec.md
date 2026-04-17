# anchorregistry — ReadTheDocs Specification

**Author:** Ian Moore (icmoore)  
**Date:** March 31, 2026  
**Status:** Pre-build spec — ships alongside mainnet launch  
**URL:** anchorregistry.readthedocs.io  
**Tool:** Sphinx + nbsphinx + ReadTheDocs  

---

## 1. Purpose & Positioning

The ReadTheDocs site is the technical credibility layer for the trustless claim. It exists to answer one question for any developer, researcher, or enterprise contact who encounters AnchorRegistry:

**"How do I know this is real and permanent?"**

The answer is demonstrated interactively through executable Jupyter notebooks that run against the live contract via RPC — no AnchorRegistry servers, no API key, no account. Anyone can clone the repo, run the notebooks, and verify the registry independently.

The docs lead with: **no API key, no account, no dependency on AnchorRegistry infrastructure.** Just an RPC endpoint and the contract address.

---

## 2. Tech Stack

| Component | Choice | Rationale |
|---|---|---|
| Doc framework | Sphinx | Standard, extensible, ReadTheDocs native |
| Notebook rendering | nbsphinx | Renders Jupyter notebooks directly into Sphinx build |
| Theme | sphinx-rtd-theme | Clean, familiar, ReadTheDocs default |
| API reference | autodoc + napoleon | Pulls docstrings automatically |
| Notebooks | Jupyter (.ipynb) | Executable examples against live Sepolia/mainnet contract |
| Hosting | ReadTheDocs | Free tier, auto-builds on push |

---

## 3. Site Structure

```
docs/
├── conf.py                  # Sphinx configuration
├── index.rst                # Landing page + toctree
├── quickstart.rst           # pip install → first call → output
├── configuration.rst        # configure(), env vars, network switching
├── api.rst                  # autodoc — all public functions
├── contract.rst             # contract reference — address, ABI, Etherscan
│
└── notebooks/
    ├── quickstart.ipynb     # get_by_arid — single anchor, live output
    ├── querying.ipynb       # all five query functions demonstrated
    ├── recover.ipynb        # full registry reconstruction — the trust proof
    ├── watermark.ipynb      # SPDX-Anchor / DAPX-Anchor generation
    └── dataframe.ipynb      # to_dataframe() — analytics use case
```

---

## 4. Page Specifications

### 4.1 `index.rst` — Landing Page

**Lead statement (verbatim):**
> No API key. No account. No dependency on AnchorRegistry infrastructure.  
> Just an RPC endpoint and the contract address.

**Content:**
- One-paragraph product description — what the package is and what it proves
- Installation block: `pip install anchorregistry`
- Toctree linking all pages and notebooks
- Link to anchorregistry.com and anchorregistry.ai

**Tone:** Direct. No marketing language. Developer-first.

---

### 4.2 `quickstart.rst` — Quickstart

Single page. Under 20 lines of prose. Gets a developer to a working first call in under 2 minutes.

**Structure:**
1. Install
2. Configure (one line — `configure(network="sepolia")` for testnet)
3. First call — `get_by_arid`
4. Output shown — the two-level record structure
5. Link to `quickstart.ipynb` for interactive version

```rst
Installation
------------
.. code-block:: bash

    pip install anchorregistry

    # With DataFrame support
    pip install anchorregistry[analytics]

Your first anchor
-----------------
.. code-block:: python

    from anchorregistry import configure, get_by_arid

    configure(network="sepolia")
    record = get_by_arid("AR-2026-x1llnO1")

.. nbinput:: python
   :execution-count: 1

   record["title"]     # → artifact title
   record["author"]    # → registrant name
   record["data"]      # → type-specific fields
```

---

### 4.3 `configuration.rst` — Configuration

Documents the full configuration system from Section 4 of the package spec.

**Sections:**
1. Environment variables — `ANCHOR_REGISTRY_ADDRESS`, `BASE_RPC_URL`, `NETWORK`
2. `configure()` function — explicit override
3. Network presets — Base mainnet and Sepolia with known values
4. Configuration resolution priority — the four-level chain
5. Switching networks within a process — code example

**Key values to document:**

| Network | Contract Address | Deploy Block | Chain ID |
|---|---|---|---|
| Base mainnet | TBD — mainnet deploy | TBD | 8453 |
| Sepolia testnet | 0x9dAb9f5B754f8C56B5F7BAd3E92A8bDe7317AD29 | 10562312 | 11155111 |

---

### 4.4 `api.rst` — API Reference

Autodoc from docstrings. No hand-writing. Every public function documented automatically.

**Autodoc directives:**
```rst
.. autofunction:: anchorregistry.get_by_arid
.. autofunction:: anchorregistry.get_by_registrant
.. autofunction:: anchorregistry.get_by_tree
.. autofunction:: anchorregistry.get_by_type
.. autofunction:: anchorregistry.get_all
.. autofunction:: anchorregistry.verify
.. autofunction:: anchorregistry.watermark
.. autofunction:: anchorregistry.configure
.. autofunction:: anchorregistry.to_dataframe

.. autoexception:: anchorregistry.exceptions.AnchorNotFoundError
.. autoexception:: anchorregistry.exceptions.ConfigurationError
```

**Docstring requirements** (Claude Code must have written these during the build):
- Parameters with types
- Return type and structure
- Raises section for exceptions
- One-line example per function

---

### 4.5 `contract.rst` — Contract Reference

Static reference page. No notebook needed.

**Content:**

```rst
Deployed Contract
-----------------

.. list-table::
   :header-rows: 1

   * - Network
     - Address
     - Deploy Block
     - Etherscan
   * - Base mainnet
     - TBD
     - TBD
     - TBD
   * - Sepolia testnet
     - 0x9dAb9f5B754f8C56B5F7BAd3E92A8bDe7317AD29
     - 10562312
     - https://sepolia.basescan.org/address/0x9dAb9f5B754f8C56B5F7BAd3E92A8bDe7317AD29

Anchored Event
--------------
[Full event signature with field descriptions]

READ_ABI
--------
[Full READ_ABI as Python code block — copied from package spec Section 3A]

Artifact Types
--------------
[Full 23-type taxonomy table with index, name, category]
```

---

## 5. Notebook Specifications

All notebooks run against **Sepolia testnet** by default. A note at the top of each notebook states:

> These examples run against Sepolia testnet (`network="sepolia"`).  
> To run against Base mainnet: replace `configure(network="sepolia")` with `configure(network="base")`.  
> All function calls, record structures, and output shapes are identical across networks.

### 5.1 `quickstart.ipynb`

**Purpose:** Minimal working example. One anchor, live output.

```python
# Cell 1 — setup
from anchorregistry import configure, get_by_arid
configure(network="sepolia")

# Cell 2 — fetch a single anchor
record = get_by_arid("AR-2026-x1llnO1")
record
```

**Expected output:** Full two-level record dict rendered in notebook.

---

### 5.2 `querying.ipynb`

**Purpose:** Demonstrate all five query functions against live Sepolia data.

```python
# Cell 1 — setup
from anchorregistry import configure, get_by_arid, get_by_registrant, get_by_tree, get_by_type, get_all
from anchorregistry.enums import ArtifactType
configure(network="sepolia")

# Cell 2 — get_by_arid
record = get_by_arid("AR-2026-x1llnO1")
print(f"Type: {record['artifact_type_name']}")
print(f"Title: {record['title']}")
print(f"Author: {record['author']}")

# Cell 3 — get_by_registrant
records = get_by_registrant("0xC7a7AFde1177fbf0Bb265Ea5a616d1b8D7eD8c44")
print(f"Total anchors by registrant: {len(records)}")

# Cell 4 — get_by_tree
records = get_by_tree("ar-operator-v1")
print(f"Total anchors in tree: {len(records)}")

# Cell 5 — get_by_type
code_anchors = get_by_type(ArtifactType.CODE)
print(f"CODE anchors on Sepolia: {len(code_anchors)}")

# Cell 6 — get_all
all_records = get_all()
print(f"Total anchors on Sepolia: {len(all_records)}")
```

---

### 5.3 `recover.ipynb` — The Trust Proof Page

**Purpose:** This is the most important notebook. It proves the registry is permanently reconstructible without AnchorRegistry infrastructure. Every developer, researcher, and enterprise contact gets pointed here.

**Lead text (markdown cell):**
> This notebook reconstructs the entire AnchorRegistry from on-chain events alone.  
> No AnchorRegistry API. No Supabase. No account.  
> Just an RPC endpoint and the contract address.  
> If AnchorRegistry's servers disappeared tomorrow, this notebook would still work.

```python
# Cell 1 — what you need
# - An Ethereum RPC endpoint (Infura, Alchemy, or your own node)
# - The contract address (public on Etherscan forever)
# - The deploy block number
# Nothing else.

from anchorregistry import configure, get_all, to_dataframe
from anchorregistry.constants import CONTRACT_ADDRESS, DEPLOY_BLOCK

configure(network="sepolia")
print(f"Contract: {CONTRACT_ADDRESS}")
print(f"Scanning from block: {DEPLOY_BLOCK}")

# Cell 2 — reconstruct the full registry
records = get_all()
print(f"Total anchors recovered: {len(records)}")

# Cell 3 — inspect a single record (raw dict)
records[0]

# Cell 4 — load into DataFrame
df = to_dataframe(records)
df.head()

# Cell 5 — explore the registry
df.groupby("artifact_type_name").size().sort_values(ascending=False)

# Cell 5 — reconstruct a specific tree
from anchorregistry import get_by_tree
tree = get_by_tree("ar-operator-v1")
for anchor in tree:
    indent = "  " * (1 if anchor["parent_ar_id"] else 0)
    print(f"{indent}{anchor['ar_id']} — {anchor['artifact_type_name']} — {anchor['title']}")

# Cell 6 — verify a specific artifact
from anchorregistry import verify
result = verify("AR-2026-x1llnO1")
print(f"Registered: {result['registered']}")
print(f"Manifest hash: {result['manifest_hash']}")
```

**Closing markdown cell:**
> The output above was generated entirely from public Ethereum event logs.  
> The contract address is permanent. The deploy block is documented.  
> Any RPC endpoint works. The registry cannot be suppressed.

---

### 5.4 `watermark.ipynb`

**Purpose:** Demonstrate SPDX-Anchor and DAPX-Anchor tag generation.

```python
# Cell 1 — setup
from anchorregistry import configure, watermark
configure(network="sepolia")

# Cell 2 — CODE type → SPDX-Anchor
line = watermark("AR-2026-x1llnO1", artifact_type="CODE")
print(line)
# → SPDX-Anchor: anchorregistry.ai/AR-2026-x1llnO1

# Cell 3 — auto-resolve type from chain
line = watermark("AR-2026-x1llnO1")
print(line)

# Cell 4 — non-CODE type → DAPX-Anchor
# [use a known RESEARCH or DATA anchor from Sepolia]
line = watermark("AR-2026-XXXXXX", artifact_type="RESEARCH")
print(line)
# → DAPX-Anchor: anchorregistry.ai/AR-2026-XXXXXX

# Cell 5 — embed in a README
readme_line = f"# My Project\n\n{watermark('AR-2026-x1llnO1')}"
print(readme_line)
```

---

### 5.5 `dataframe.ipynb`

**Purpose:** Analytics use case. Demonstrate `to_dataframe()` and pandas integration.

```python
# Cell 1 — setup
from anchorregistry import configure, get_all, to_dataframe
import pandas as pd
configure(network="sepolia")

# Cell 2 — load full registry into DataFrame
df = to_dataframe(get_all())
print(f"Shape: {df.shape}")
df.dtypes

# Cell 3 — filter by type
code_df = df[df.artifact_type_name == "CODE"]
code_df[["ar_id", "title", "author", "code_language", "code_version"]]

# Cell 4 — filter by author
ian_df = df[df.author == "Ian Moore"]
ian_df[["ar_id", "artifact_type_name", "title"]]

# Cell 5 — group by type
df.groupby("artifact_type_name").size().sort_values(ascending=False)

# Cell 6 — tree analysis
df.groupby("tree_id").size().sort_values(ascending=False)
```

---

## 6. `conf.py` Requirements

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",   # Google/NumPy style docstrings
    "sphinx.ext.viewcode",   # source code links
    "nbsphinx",              # Jupyter notebook rendering
]

html_theme = "sphinx_rtd_theme"

# nbsphinx — execute notebooks at build time
nbsphinx_execute = "never"   # pre-executed notebooks — output already saved
                              # set to "always" for live execution on build

# autodoc
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}
```

**`nbsphinx_execute = "never"`** — notebooks are pre-executed with saved output. This means the docs build fast and reliably on ReadTheDocs without needing an RPC endpoint at build time. The notebook outputs are the ground truth — saved from a real Sepolia run before publish.

---

## 7. `requirements.txt` for ReadTheDocs

```
sphinx
sphinx-rtd-theme
nbsphinx
ipython
pandoc
anchorregistry
```

ReadTheDocs needs these to build. `anchorregistry` itself is included so autodoc can import the package during the build.

---

## 8. `.readthedocs.yaml`

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - requirements: docs/requirements.txt
```

---

## 9. Build & Publish Sequencing

| Step | Action |
|---|---|
| 1 | Scaffold Sphinx structure — `conf.py`, `index.rst`, all `.rst` pages |
| 2 | Scaffold all five notebooks with cell structure — no output yet |
| 3 | Run all notebooks against Sepolia — save output |
| 4 | Verify autodoc pulls docstrings correctly from package |
| 5 | Connect ReadTheDocs to `ar-python` GitHub repo |
| 6 | Trigger first build — validate rendering |
| 7 | Fix any nbsphinx or autodoc issues |
| 8 | After mainnet deploy — update `contract.rst` with mainnet address and deploy block |
| 9 | Re-run notebooks against mainnet — save new output |
| 10 | Publish — docs live alongside mainnet launch |

---

## 10. Notes

- Notebooks use `nbsphinx_execute = "never"` — outputs are pre-saved from real Sepolia runs. This is the honest approach: the output in the docs is real, not generated at build time.
- After mainnet deploy, re-run all notebooks against mainnet and save new outputs before publishing. Sepolia outputs are fine for pre-launch validation but mainnet outputs should be in the published docs.
- The `recover.ipynb` closing statement is load-bearing marketing copy. It should be the last thing someone reads before they close the docs. Make it count.
- `contract.rst` mainnet values are TBD — populated at mainnet deploy, same as `constants.py`.
- DAPX-Anchor tag for the docs repo itself gets embedded in `README.md` after the docs repo is anchored post-mainnet.

---

*AnchorRegistry™ · anchorregistry.com · anchorregistry.ai · March 2026*
