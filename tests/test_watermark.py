# SPDX-License-Identifier: BUSL-1.1
"""Tests for watermark() — SPDX vs DAPX routing."""

import pytest

from anchorregistry.client import watermark


class TestWatermark:
    """Tests for the watermark tag generation."""

    def test_code_returns_spdx_anchor(self):
        result = watermark("AR-2026-Pvdp0W5", artifact_type="CODE")
        assert result == "SPDX-Anchor: anchorregistry.ai/AR-2026-Pvdp0W5"

    def test_research_returns_dapx_anchor(self):
        result = watermark("AR-2026-XXXXXX", artifact_type="RESEARCH")
        assert result == "DAPX-Anchor: anchorregistry.ai/AR-2026-XXXXXX"

    def test_all_non_code_types_return_dapx(self):
        non_code_types = [
            "RESEARCH", "DATA", "MODEL", "AGENT", "MEDIA", "TEXT", "POST",
            "ONCHAIN", "REPORT", "NOTE", "WEBSITE", "EVENT", "RECEIPT",
            "LEGAL", "ENTITY", "PROOF", "RETRACTION", "REVIEW", "VOID",
            "AFFIRMED", "ACCOUNT", "OTHER",
        ]
        for t in non_code_types:
            result = watermark("AR-2026-TEST", artifact_type=t)
            assert result.startswith("DAPX-Anchor:"), f"{t} should produce DAPX-Anchor"

    def test_format_contains_ar_id(self):
        result = watermark("AR-2026-MyCustomId", artifact_type="CODE")
        assert "AR-2026-MyCustomId" in result

    def test_format_contains_domain(self):
        result = watermark("AR-2026-TEST", artifact_type="CODE")
        assert "anchorregistry.ai/" in result
