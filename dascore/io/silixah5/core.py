"""
Support for Silixa's hdf5-based format.
"""

from pathlib import Path
from typing import List, Optional, Union

from dascore.constants import timeable_types
from dascore.core import MemorySpool
from dascore.core.schema import PatchFileSummary
from dascore.io.core import FiberIO
from dascore.utils.hdf5 import open_hdf5_file

from .utils import _get_default_attrs


class SilixaHDF52_1(FiberIO):
    """
    Support for Silixa's HDF5 format version 2.1.
    """

    name = "SilixaH5"
    version = "2.1"
    preferred_extensions = (
        "h5",
        "hdf5",
    )

    def get_format(self, path: Union[str, Path]) -> Union[tuple[str, str], bool]:
        """
        Return a tuple of (TDMS, version) if TDMS else False.

        Parameters
        ----------
        path
            A path to the file which may contain silixa data.
        """
        with open_hdf5_file(path, "r") as fi:
            print(fi)

    def scan(self, path: Union[str, Path]) -> List[PatchFileSummary]:
        """
        Scan a silixa tdms file, return summary information about the file's contents.
        """
        with open(path, "rb") as tdms_file:
            out = _get_default_attrs(tdms_file)
            out["path"] = path
            out["file_format"] = self.name
            out["file_version"] = self.version
            return [PatchFileSummary(**out)]

    def read(
        self,
        path: Union[str, Path],
        time: Optional[tuple[timeable_types, timeable_types]] = None,
        distance: Optional[tuple[float, float]] = None,
        **kwargs
    ) -> MemorySpool:
        """
        Read a silixa tdms file, return a DataArray.

        """
        with open_hdf5_file(path, "r"):
            pass
