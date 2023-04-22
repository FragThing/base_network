"""
This test suite covers the functionality of the URLParse class. It includes
tests for:
- Encoding and decoding data using Base85 and SHAKE256 algorithms
- Extracting and resetting schemes from a URL
- Test the encoding and decoding process for both decodable (Base85) and
  non-decodable (SHAKE256) algorithms

Test cases use the pytest library and parameterization to provide a variety
of input data and expected results.
"""

import pytest
from ucn.url_parse import URLParse

# Define a list of test parameters for the default encoding algorithm selection
default_encode_params = [
    # Test case 1: A short data input, should be encoded with Base85
    (b"test_data", "Base85://bY*jNUu0o)VE"),

    # Test case 2: Data input with exactly 128 bytes,
    # should still be encoded with Base85
    (
        b"long_data_long_data_long_data_long_data_long_data_long_data_long_"
        b"data_long_data_long_data_long_data_long_data_long_data_long_dat",
        "Base85://Y;SI7Uu0o)VP9--Zf9R)VRT_%Y;SI7Uu0o)VP9--Zf9R)VRT_%Y;SI7Uu0o)"
        "VP9--Zf9R)VRT_%Y;SI7Uu0o)VP9--Zf9R)VRT_%Y;SI7Uu0o)VP9--Zf9R)VRT_%Y;"
        "SI7Uu0o)VP9--Zf9R)VRT_%Y;SI7Uu0o)",
    ),

    # Test case 3: Data input with exactly 129 bytes,
    # should be encoded with SHAKE256
    (
        b"long_data_long_data_long_data_long_data_long_data_long_data_long_"
        b"data_long_data_long_data_long_data_long_data_long_data_long_data",
        "SHAKE256://ab1829f053f1abc913acbb5be17b08db8980cded13b59cd70d1ab6685"
        "5f43912c2a4604c034092253b25613be08624e445782ef88f035ca2bb993368e3bf3"
        "e8a4bf6b2d4a1770a360cfd08e048a25b2c8fa91f8481d2cfaf3bc7efcdda65c062e"
        "08ba0f886a1d963187a456c86aa384025f42ca77401ad41381dde49f010cd4a"
    ),
]

base85_encode_params = [
    (b"test_data", "Base85://bY*jNUu0o)VE"),
]

shake256_encode_params = [
    (
        b"test_data",
        "SHAKE256://a50bad10f9b2bbde9a1fa6454d9578bec74aa738d418eba7"
        "88a9d940b222a245ffb5fb8e7f738aab0a18049ade60bd06"
        "2b7c86c5fab12bebd3a6100e63b9b0c800edc421c232afd8"
        "a9ee6e1a4884965e14235953f5911a7ba3cf67c3d0c29643"
        "8129c04db1aacb4b8a939ad16f30a73e72d23cb5d07bf437"
        "21dc6fea708b1b39",
    ),
]


@pytest.fixture
def url_parse():
    """Fixture to provide a URLParse object for the test functions."""
    return URLParse()


@pytest.mark.parametrize("data, expected", default_encode_params)
def test_encode_default_algo(url_parse, data, expected):
    """Test encoding data using the default encoding algorithm."""
    result = url_parse.encode(data)
    assert result == expected


@pytest.mark.parametrize("data, expected", base85_encode_params)
def test_encode_base85(url_parse, data, expected):
    """Test encoding data using Base85."""
    result = url_parse.encode(data, encode_algo="Base85")
    assert result == expected


@pytest.mark.parametrize("data, expected", shake256_encode_params)
def test_encode_shake256(url_parse, data, expected):
    """Test encoding data using SHAKE256."""
    result = url_parse.encode(data, encode_algo="SHAKE256")
    assert result == expected


@pytest.mark.parametrize(
    "url, expected",
    [(url, expected) for expected, url in base85_encode_params],
)
def test_decode_base85(url_parse, url, expected):
    """Test decoding Base85 encoded data."""
    result = url_parse.decode(url)
    assert result == expected


@pytest.mark.parametrize(
    "url, expected",
    [(url, expected) for expected, url in shake256_encode_params],
)
def test_decode_shake256(url_parse, url, expected):
    """Test decoding shake256 encoded data (should return None)."""
    result = url_parse.decode(url)
    assert result != expected
    assert result is None


@pytest.mark.parametrize(
    "url, expected",
    [
        ("scheme1+scheme2+scheme3://content", ["scheme1", "scheme2", "scheme3"]),
    ],
)
def test_get_scheme(url_parse, url, expected):
    """Test extracting scheme list from a URL."""
    result = url_parse.get_scheme(url)
    assert result == expected


@pytest.mark.parametrize(
    "url, new_scheme_list, expected",
    [
        (
            "scheme1+scheme2+scheme3://content",
            ["new_scheme1", "new_scheme2"],
            "new_scheme1+new_scheme2://content",
        ),
    ],
)
def test_reset_scheme(url_parse, url, new_scheme_list, expected):
    """Test resetting the scheme of a URL."""
    result = url_parse.reset_scheme(url, new_scheme_list)
    assert result == expected


@pytest.mark.parametrize(
    "data, encode_algo, decodable",
    [
        (b"test_data", "Base85", True),
        (b"test_data", "SHAKE256", False),
    ],
)
def test_encode_decode(url_parse, data, encode_algo, decodable):
    """Test the encoding and decoding process."""
    encoded = url_parse.encode(data, encode_algo=encode_algo)
    decoded = url_parse.decode(encoded)

    if decodable:
        assert decoded == data
    else:
        assert decoded is None
