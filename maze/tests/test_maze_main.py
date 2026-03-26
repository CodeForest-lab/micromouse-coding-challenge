import pytest
import argparse

from maze.maze_main import (
    parse_pair,
    corner_to_coord,
    parse_view_path,
    parse_args,
    main
)

def test_parse_pair_valid():
    assert parse_pair("10,20") == (10, 20)


def test_parse_pair_none():
    assert parse_pair(None) is None


def test_parse_pair_invalid():
    with pytest.raises(argparse.ArgumentTypeError):
        parse_pair("invalid")

def test_corner_to_coord():
    rows, cols = 10, 20

    assert corner_to_coord(1, rows, cols) == (0, cols - 1)
    assert corner_to_coord(2, rows, cols) == (rows - 1, cols - 1)
    assert corner_to_coord(3, rows, cols) == (rows - 1, 0)
    assert corner_to_coord(4, rows, cols) == (0, 0)

def test_corner_to_coord_invalid():
    assert corner_to_coord(99, 10, 10) is None

def test_parse_view_path_full_file():
    path = "maze/maze_1/map.txt"
    assert parse_view_path(path) == path


def test_parse_view_path_folder():
    path = "maze/maze_1"
    assert parse_view_path(path) == "maze/maze_1/map.txt"


def test_parse_view_path_short_name():
    path = "maze_1"
    assert parse_view_path(path) == "maze/maze_1/map.txt"

def test_parse_args_generate(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["prog", "--generate", "--size", "10,10"]
    )

    args = parse_args()

    assert args.generate is True
    assert args.view is None
    assert args.size == (10, 10)


def test_parse_args_view(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["prog", "--view", "maze_1"]
    )

    args = parse_args()

    assert args.view == "maze_1"
    assert args.generate is False

def test_main_generate_called(monkeypatch):
    called = {}

    def fake_generate(gui, config, size, count):
        called["generate"] = True

    monkeypatch.setattr("maze.maze_main.main_generate", fake_generate)

    args = argparse.Namespace(
        generate=True,
        view=None,
        gui=False,
        size=(10, 10),
        loops=False,
        target_coordinates=None,
        set_start=None,
        count=1
    )

    main(args)

    assert called.get("generate") is True

def test_main_view_called(monkeypatch):
    called = {}

    def fake_view(path):
        called["view"] = path

    monkeypatch.setattr("maze.maze_main.main_view", fake_view)

    args = argparse.Namespace(
        generate=False,
        view="maze_1",
        gui=False,
        size=None,
        loops=False,
        target_coordinates=None,
        set_start=None,
        count=1
    )

    main(args)

    assert called["view"] == "maze_1"