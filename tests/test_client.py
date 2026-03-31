# SPDX-License-Identifier: BUSL-1.1
"""Integration tests for client.py — run against Sepolia testnet.

These tests require SEPOLIA_RPC_URL to be set. They are skipped otherwise.
"""

import os

import pytest

from anchorregistry import configure
from anchorregistry.exceptions import AnchorNotFoundError

TEST_CONTRACT = "0x9dAb9f5B754f8C56B5F7BAd3E92A8bDe7317AD29"
TEST_RPC = os.environ.get("SEPOLIA_RPC_URL")
TEST_AR_ID = "AR-2026-d6L3KJP"

needs_rpc = pytest.mark.skipif(
    TEST_RPC is None, reason="SEPOLIA_RPC_URL not set"
)


@pytest.fixture(autouse=True)
def _configure_sepolia():
    """Configure the package for Sepolia before each test."""
    if TEST_RPC:
        configure(network="sepolia", rpc_url=TEST_RPC)


@needs_rpc
class TestGetByArid:
    """Tests for get_by_arid()."""

    def test_returns_valid_record(self):
        from anchorregistry import get_by_arid

        record = get_by_arid(TEST_AR_ID)
        assert record["ar_id"] == TEST_AR_ID
        assert record["registered"] is True
        assert record["artifact_type_name"] in [t.name for t in __import__("anchorregistry.enums", fromlist=["ArtifactType"]).ArtifactType]
        assert record["tx"].startswith("0x")
        assert isinstance(record["block"], int)
        assert isinstance(record["data"], dict)

    def test_not_found_raises(self):
        from anchorregistry import get_by_arid

        with pytest.raises(AnchorNotFoundError):
            get_by_arid("AR-9999-NONEXISTENT")


@needs_rpc
class TestGetByRegistrant:
    """Tests for get_by_registrant()."""

    def test_returns_list(self):
        from anchorregistry import get_by_arid, get_by_registrant

        # Get a known registrant from the test anchor
        record = get_by_arid(TEST_AR_ID)
        registrant = record["registrant"]
        records = get_by_registrant(registrant)
        assert isinstance(records, list)
        assert len(records) > 0
        assert any(r["ar_id"] == TEST_AR_ID for r in records)


@needs_rpc
class TestGetByTree:
    """Tests for get_by_tree()."""

    def test_returns_tree_records(self):
        from anchorregistry import get_by_arid, get_by_tree

        record = get_by_arid(TEST_AR_ID)
        tree_id = record["tree_id"]
        records = get_by_tree(tree_id)
        assert isinstance(records, list)
        assert len(records) > 0
        assert all(r["tree_id"] == tree_id for r in records)


@needs_rpc
class TestGetByType:
    """Tests for get_by_type()."""

    def test_filters_by_type(self):
        from anchorregistry import get_by_arid, get_by_type

        record = get_by_arid(TEST_AR_ID)
        type_idx = record["artifact_type_index"]
        records = get_by_type(type_idx)
        assert isinstance(records, list)
        assert all(r["artifact_type_index"] == type_idx for r in records)


@needs_rpc
class TestGetAll:
    """Tests for get_all()."""

    def test_returns_all_records(self):
        from anchorregistry import get_all

        records = get_all()
        assert isinstance(records, list)
        assert len(records) > 0

    def test_block_range(self):
        from anchorregistry import get_by_arid, get_all

        record = get_by_arid(TEST_AR_ID)
        block = record["block"]
        records = get_all(from_block=block, to_block=block)
        assert any(r["ar_id"] == TEST_AR_ID for r in records)


@needs_rpc
class TestVerify:
    """Tests for verify()."""

    def test_verify_record_only(self):
        from anchorregistry import verify

        result = verify(TEST_AR_ID)
        assert result["verified"] is True
        assert result["hash_match"] is None
        assert result["ar_id"] == TEST_AR_ID

    def test_verify_with_file(self, tmp_path):
        from anchorregistry import verify

        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")
        result = verify(TEST_AR_ID, file_path=str(test_file))
        assert result["verified"] is True
        assert isinstance(result["hash_match"], bool)


@needs_rpc
class TestWatermark:
    """Tests for watermark() with on-chain resolution."""

    def test_resolves_type_on_chain(self):
        from anchorregistry import watermark

        result = watermark(TEST_AR_ID)
        assert "anchorregistry.ai/" + TEST_AR_ID in result
        assert result.startswith("SPDX-Anchor:") or result.startswith("DAPX-Anchor:")
