# SPDX-License-Identifier: BUSL-1.1
"""Network presets and exported constants for anchorregistry."""

NETWORKS = {
    "base": {
        "contract_address": "TBD",
        "deploy_block": None,
        "chain_id": 8453,
        "rpc_url": "https://mainnet.base.org",
    },
    "sepolia": {
        "contract_address": "0xb0435faa6deedc1cb6a809008516fe4f4b094f76",
        "deploy_block": 40223000,  # SEAL contract deploy block (Base Sepolia)
        "chain_id": 84532,
        "rpc_url": "https://base-sepolia-rpc.publicnode.com",
    },
}

# Active-network values — updated by config.configure()
CONTRACT_ADDRESS: str = NETWORKS["base"]["contract_address"]
DEPLOY_BLOCK: int | None = NETWORKS["base"]["deploy_block"]
