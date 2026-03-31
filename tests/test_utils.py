# SPDX-License-Identifier: BUSL-1.1
"""Tests for utils.py — topic builder, address topic, to_dataframe."""

import pytest
from web3 import Web3

from anchorregistry.utils import _address_topic, _build_topic, to_dataframe


class TestBuildTopic:
    """Tests for _build_topic()."""

    def test_returns_hex_string(self):
        topic = _build_topic("hello")
        assert topic.startswith("0x")
        assert len(topic) == 66  # 0x + 64 hex chars

    def test_known_hash(self):
        """Verify against independently computed keccak256."""
        expected = "0x" + Web3.keccak(text="ar-operator-v1").hex()
        assert _build_topic("ar-operator-v1") == expected

    def test_different_inputs_different_hashes(self):
        assert _build_topic("AR-2026-001") != _build_topic("AR-2026-002")


class TestAddressTopic:
    """Tests for _address_topic()."""

    def test_pads_to_32_bytes(self):
        topic = _address_topic("0xc7a7afde1177fbf0bb265ea5a616d1b8d7ed8c44")
        assert len(topic) == 66  # 0x + 64 hex chars
        assert topic.startswith("0x000000000000000000000000")

    def test_lowercase(self):
        topic = _address_topic("0xC7A7AFDE1177FBF0BB265EA5A616D1B8D7ED8C44")
        assert "C7A7" not in topic
        assert "c7a7afde" in topic


class TestToDataframe:
    """Tests for to_dataframe()."""

    def test_flat_columns(self):
        records = [
            {
                "ar_id": "AR-001",
                "artifact_type_name": "CODE",
                "block": 100,
                "data": {},
            }
        ]
        df = to_dataframe(records)
        assert "ar_id" in df.columns
        assert "block" in df.columns
        assert "data" not in df.columns

    def test_type_prefixed_data_columns(self):
        records = [
            {
                "ar_id": "AR-001",
                "artifact_type_name": "CODE",
                "data": {"git_hash": "abc123", "license": "MIT"},
            },
            {
                "ar_id": "AR-002",
                "artifact_type_name": "RESEARCH",
                "data": {"doi": "10.1234/test", "institution": "MIT"},
            },
        ]
        df = to_dataframe(records)
        assert "code_git_hash" in df.columns
        assert "code_license" in df.columns
        assert "research_doi" in df.columns
        assert "research_institution" in df.columns

    def test_mixed_types_have_nan_for_missing(self):
        import pandas as pd

        records = [
            {"ar_id": "AR-001", "artifact_type_name": "CODE", "data": {"url": "http://x"}},
            {"ar_id": "AR-002", "artifact_type_name": "RESEARCH", "data": {"doi": "10.1"}},
        ]
        df = to_dataframe(records)
        assert pd.isna(df.loc[df.ar_id == "AR-001", "research_doi"].iloc[0])
        assert pd.isna(df.loc[df.ar_id == "AR-002", "code_url"].iloc[0])

    def test_empty_records(self):
        df = to_dataframe([])
        assert len(df) == 0
