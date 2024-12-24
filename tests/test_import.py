"""Test pyn8n."""

import pyn8n


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(pyn8n.__name__, str)
