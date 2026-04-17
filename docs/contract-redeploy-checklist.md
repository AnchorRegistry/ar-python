# Contract Redeploy Checklist

When the AnchorRegistry contract is redeployed to a new chain or address, update the following.

## Information needed upfront

- [ ] New chain name (e.g. Base Sepolia, Base mainnet)
- [ ] New contract address
- [ ] A sample TX hash with an Anchored event (to verify and derive deploy block)
- [ ] Block explorer URL (e.g. `https://sepolia.basescan.org/`)
- [ ] Working RPC endpoint for the new chain
- [ ] A test ownership token + AR-ID that exists on the new contract

## ar-python updates

### 1. `src/anchorregistry/constants.py`
- [ ] `contract_address` — new address
- [ ] `deploy_block` — block just before the first Anchored event
- [ ] `chain_id` — new chain ID
- [ ] `rpc_url` — public RPC for the new chain

### 2. `docs/anchorregistry_readthedocs_spec.md`
- [ ] Update the Deployed Contract table (address, deploy block, explorer link)

### 3. Run tests
```bash
python3 -m pytest tests/ -v --ignore=tests/test_client.py
```

### 4. Verify end-to-end with the library
```python
from anchorregistry import configure, get_all, authenticate_anchor
configure(network="sepolia")  # or "base"
print(get_all())
print(authenticate_anchor(ownership_token="0x...", ar_id="AR-2026-..."))
```

### 5. Commit and reinstall
```bash
git add src/anchorregistry/constants.py docs/anchorregistry_readthedocs_spec.md
git commit -m "fix: update contract to <new chain>"
pip install -e .
```

## ar-python-docs notebook updates

All notebooks in `docs/notebooks/` need:

- [ ] **Remove any `rpc_url=` overrides** in `configure()` calls — let the library default handle it
- [ ] **Replace AR-IDs** with ones that exist on the new contract
- [ ] **Replace tree IDs** with valid ones from the new contract
- [ ] **Clear all cell outputs** (stale outputs contain old data and error traces)
- [ ] **Update markdown** references (chain name, explorer URLs)

### Notebooks to update
- [ ] `quickstart.ipynb`
- [ ] `querying.ipynb`
- [ ] `dataframe.ipynb`
- [ ] `watermark.ipynb` — needs AR-IDs of different types (CODE, DATA, RESEARCH)
- [ ] `recover.ipynb`
- [ ] `authenticate.ipynb`

### Gotcha: NotebookEdit vs raw JSON
The `.ipynb` format stores cell source as JSON string arrays. If an edit tool doesn't persist, use a Python script to patch the raw JSON directly (see `authenticate.ipynb` fix as precedent).

### Gotcha: Jupyter kernel caching
After `pip install -e .`, a kernel restart alone may not pick up changes. Kill the entire Jupyter server and relaunch if the old code persists.
