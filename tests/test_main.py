import pytest
from pathlib import Path
from pytest_mock import MockerFixture
from typing import Generator
from geojson2osm.__main__ import main


test_files = [
    "polygon",
    "repeated_point"
]


@pytest.fixture(autouse=True)
def run_around_tests() -> Generator:
    # Code that will run before your test, for example:
    # A test function will be run at this point
    yield
    # Code that will run after your test:
    p = Path("output.xml")
    if p.exists():
        p.unlink()


@pytest.mark.parametrize("filename", test_files)
def test_main(mocker: MockerFixture, filename: str) -> None:
    mocker.patch(
        "sys.argv",
        [
            "geojson2osm",
            "tests/files/" + filename + ".geojson",
            "output.xml"
        ],
    )
    main()
    f = open("output.xml", "r")
    file = f.read()
    f1 = open("tests/files/" + filename + ".xml", "r")
    expected = f1.read()
    assert file == expected
