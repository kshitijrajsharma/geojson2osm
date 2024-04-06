from pytest_mock import MockerFixture
from geojson2osm.__main__ import main


def test_main(mocker: MockerFixture) -> None:
    mocker.patch(
        "sys.argv",
        [
            "geojson2osm",
            "tests/files/input.geojson",
            "output.xml"
        ],
    )
    main()
    f = open("output.xml", "r")
    file = f.read()
    f1 = open("tests/files/output.xml", "r")
    expected = f1.read()
    assert file == expected
