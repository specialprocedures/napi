"""Tests for napi CLI tool."""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
import napi


def test_get_api_key_from_args():
    """Test API key retrieval from arguments."""
    api_key = napi.get_api_key("test_key")
    assert api_key == "test_key"


@patch.dict("os.environ", {"NEWSAPI_API_KEY": "env_key"})
def test_get_api_key_from_env():
    """Test API key retrieval from environment variables."""
    api_key = napi.get_api_key()
    assert api_key == "env_key"


def test_get_api_key_missing():
    """Test error when no API key is found."""
    with patch.dict("os.environ", {}, clear=True):
        with patch("napi.load_dotenv"):
            with pytest.raises(TypeError, match="Error: No API key found"):
                napi.get_api_key()


def test_parse_args_pull():
    """Test argument parsing for pull command."""
    with patch(
        "sys.argv",
        ["napi", "pull", "query.json", "output.json", "--api_key", "test_key"],
    ):
        args = napi.parse_args()
        assert args.command == "pull"
        assert args.query_json == "query.json"
        assert args.output_json == "output.json"
        assert args.api_key == "test_key"


@patch("napi.requests")
def test_get_page(mock_requests):
    """Test getting a single page of results."""
    # Mock response
    mock_response = mock_requests.post.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "articles": {"results": [{"title": "Test Article"}], "pages": 5}
    }

    query_params = {"test": "param"}
    result = napi.get_page(query_params, 1)

    assert result["results"] == [{"title": "Test Article"}]
    assert result["pages"] == 5
    assert query_params["articlesPage"] == 1


if __name__ == "__main__":
    pytest.main([__file__])
