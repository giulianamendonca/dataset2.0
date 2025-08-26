import project
import pytest


class DummyParameters:
    def __init__(self, min_digits: int, max_digits: int, rows: int):
        self.min_digits = min_digits
        self.max_digits = max_digits
        self.rows = rows


def test_get_number(monkeypatch):
    # valid input
    monkeypatch.setattr("builtins.input", lambda _: 50)
    assert project.get_number("number") == 50

    # invalid input
    inputs = iter(["T", 50])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert project.get_number("number") == 50


def test_get_distribution(monkeypatch):
    # uniform distribution
    monkeypatch.setattr("builtins.input", lambda _: "U")
    assert project.get_distribution() == ("U", 0)

    # triangular distribution
    inputs = iter(["T", 50])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert project.get_distribution() == ("T", 0.5)

    # invalid input
    inputs = iter(["X", "T", "abc", "T", 50])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert project.get_distribution() == ("T", 0.5)


def test_get_digits():
    dummy_parameters = DummyParameters(min_digits=2, max_digits=4, rows=5)
    results = project.get_digits(12345, dummy_parameters)

    # shape
    assert len(results) == 5
    assert all(2 <= r <= 4 for r in results)
    assert all(isinstance(r, int) for r in results)

    # values
    assert results == [3, 4, 2, 3, 3]


def test_get_range():
    # valid cases
    assert project.get_range(1) == (1, 9)
    assert project.get_range(3) == (100, 999)
    assert project.get_range(5) == (10000, 99999)

    # invalid cases
    with pytest.raises(TypeError):
        project.get_range("cat")
