"""
Tests for Silixa hdf5 version 2.1
"""
from pathlib import Path

import pytest

import dascore
from dascore.constants import REQUIRED_DAS_ATTRS
from dascore.core.schema import PatchFileSummary
from dascore.io.silixah5.core import SilixaHDF52_1
from dascore.utils.downloader import fetch


@pytest.fixture()
def silixa_h5_das_example_path():
    """Get path for test file"""
    file_path = fetch("iDAS005_hdf5_example.626.h5")
    return Path(file_path)


@pytest.fixture()
def silixa_h5_das_patch(silixa_h5_das_example_path):
    """Make patch for test data"""
    ft = SilixaHDF52_1()
    spool = ft.read(silixa_h5_das_example_path)
    return spool[0]


class TestReadSilixa:
    """Tests for reading the silixa format."""

    def test_type(self, silixa_h5_das_patch):
        """Ensure the expected type is returned."""
        assert isinstance(silixa_h5_das_patch, dascore.Patch)

    def test_attributes(self, silixa_h5_das_patch):
        """Ensure a few of the expected attrs exist in array."""
        attrs = silixa_h5_das_patch.attrs
        expected_attrs = {"time_min", "time_max", "distance_min", "data_units"}
        assert set(expected_attrs).issubset(set(attrs))

    def test_has_required_attrs(self, silixa_h5_das_patch):
        """ "Ensure the required das attrs are found"""
        assert set(REQUIRED_DAS_ATTRS).issubset(set(silixa_h5_das_patch.attrs))

    def test_coord_attr_time_equal(self, silixa_h5_das_patch):
        """The time reported in the attrs and coords should match"""
        attr_time = silixa_h5_das_patch.attrs["time_max"]
        coord_time = silixa_h5_das_patch.coords["time"].max()
        assert attr_time == coord_time

    def test_time_dist_slice(self, silixa_h5_das_patch, silixa_h5_das_example_path):
        """Ensure slicing distance and time works from read func."""
        time_array = silixa_h5_das_patch.coords["time"]
        dist_array = silixa_h5_das_patch.coords["distance"]
        t1, t2 = time_array[10], time_array[40]
        d1, d2 = dist_array[10], dist_array[40]

        patch = silixa_h5_das_example_path().read(
            silixa_h5_das_example_path, time=(t1, t2), distance=(d1, d2)
        )[0]
        attrs, coords = patch.attrs, patch.coords
        assert attrs["time_min"] == coords["time"].min() == t1
        assert attrs["time_max"] == coords["time"].max() == t2
        assert attrs["distance_min"] == coords["distance"].min() == d1
        assert attrs["distance_max"] == coords["distance"].max() == d2


class TestGetFormat:
    """Tests for function to determine if a file is a silixa file."""

    def test_not_silixa_not_tdms(self, dummy_text_file):
        """Test for not a silixa tdms file."""
        parser = SilixaHDF52_1()
        assert not parser.get_format(dummy_text_file)
        assert not parser.get_format(dummy_text_file.parent)

    def test_silixa_get_format(self, silixa_h5_das_example_path):
        """Test for a silixa tdms file."""
        parser = SilixaHDF52_1()
        assert parser.get_format(silixa_h5_das_example_path)
        format_name, format_version = parser.get_format(silixa_h5_das_example_path)
        assert format_name == parser.name


class TestScanSilixaH5:
    """Tests for scanning silixa hdf5 file."""

    def test_scanning(self, silixa_h5_das_patch, silixa_h5_das_example_path):
        """Tests for getting summary info from silixa data."""
        parser = SilixaHDF52_1()
        out = parser.scan(silixa_h5_das_example_path)
        assert isinstance(out, list)
        assert len(out) == 1
        assert isinstance(out[0], PatchFileSummary)
