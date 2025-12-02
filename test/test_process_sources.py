from ..processing import process_sources as ps 
import pytest
from unittest.mock import MagicMock, patch
import os
import pandas as pd

def test_get_engine_correctly(monkeypatch):
    mock_engine = MagicMock()
    mock_create = MagicMock(return_value=mock_engine)

    monkeypatch.setenv("DATABASE_URL", "postgres://test")
    monkeypatch.setattr(ps, "create_engine", mock_create)

    with ps.get_engine() as engine:
        assert engine is mock_engine
    mock_create.assert_called_once_with("postgres://test")
    mock_engine.dispose.assert_called_once()

def test_load_source_type(monkeypatch):
    monkeypatch.setenv('SOURCE_TESTING_TYPE', 'source_type')
    monkeypatch.setenv('SOURCE_TESTING_PATH', 'source_path')
    sources = ps.load_source()[1]

    assert sources['TESTING'] == {
        'type': 'source_type',
        'path': 'source_path'
    }

def test_load_raw_type(monkeypatch):
    monkeypatch.setenv('RAW_TESTING_TYPE', 'raw_type')
    monkeypatch.setenv('RAW_TESTING_PATH', 'raw_path')
    raw_sources = ps.load_source()[0]

    assert raw_sources['TESTING'] == {
        'type': 'raw_type',
        'path': 'raw_path'
    }

def test_read_source_csv():
    df = pd.DataFrame({
        'col1': [10,20,30],
        'col2': ['a','b','c']
    })
    source = {
        'type': 'csv',
        'path': 'fake/path.csv'
    }
    with patch.object(ps.pd, 'read_csv', return_value = df) as mock_read_csv:
        result = ps.read_source(source)
        
    assert result.equals(df)
    mock_read_csv.assert_called_once_with('fake/path.csv')

def test_read_source_json():
    df = pd.DataFrame({
        'col1': [10,20,30],
        'col2': ['a','b','c']
    })
    source = {
        'type': 'json',
        'path': 'fake/path.json'
    }

    with patch.object(ps.pd, 'read_json', return_value=df) as mock_read_json:
        result = ps.read_source(source)

    assert result.equals(df)
    mock_read_json.assert_called_once_with('fake/path.json')

def test_read_source_error():
    source = {
        'type': 'testing',
    }

    with pytest.raises(ValueError) as info:
        result = ps.read_source(source)
    
    assert 'testing' in str(info.value)

