from unittest.mock import MagicMock
from ..processing import clean_data as cd


def test_main(monkeypatch):
    raw_df = MagicMock(name="raw_df")
    valid_df = MagicMock(name="valid_df")
    cleaned_df = MagicMock(name="cleaned_df")
    invalid_df = MagicMock(name="invalid_df")
    teams_df = MagicMock(name="teams_df")
    games_df = MagicMock(name="games_df")
    engine = MagicMock(name="engine")

    raw_sources = {"CSV": {"type": "csv", "path": "fake/raw.csv"}}
    monkeypatch.setattr(cd.process, "load_source", MagicMock(return_value=[raw_sources, {}]))
    monkeypatch.setattr(cd.process, "read_source", MagicMock(return_value=raw_df))

    monkeypatch.setattr(cd.vd, "split_valid_invalid", MagicMock(return_value=[valid_df, invalid_df]))
    monkeypatch.setattr(cd.vd, "clean_valid_df", MagicMock(return_value=cleaned_df))

    monkeypatch.setattr(cd.wr, "build_teams_df", MagicMock(return_value=teams_df))
    monkeypatch.setattr(cd.wr, "build_games_df", MagicMock(return_value=games_df))

    mock_engine = MagicMock()
    mock_create = MagicMock(return_value=mock_engine)
    monkeypatch.setattr(cd.process, "create_engine", mock_create)

    monkeypatch.setattr(cd.wr, "build_tables", MagicMock())

    cd.main()

    cd.process.load_source.assert_called_once()
    cd.process.read_source.assert_called_once_with(raw_sources["CSV"])
    cd.vd.split_valid_invalid.assert_called_once_with(raw_df)
    cd.vd.clean_valid_df.assert_called_once_with(valid_df)

    cleaned_df.to_csv.assert_called_once_with("./data/CLEANED.CSV", index=False)
    cleaned_df.to_json.assert_called_once_with("./data/CLEANED.JSON", index=False)
    invalid_df.to_csv.assert_called_once_with("./data/INVALID.CSV", index=False)

    cd.wr.build_teams_df.assert_called_once_with(cleaned_df)
    cd.wr.build_games_df.assert_called_once_with(cleaned_df)
    cd.wr.build_tables.assert_called_once_with(teams_df, games_df, invalid_df, mock_engine)
