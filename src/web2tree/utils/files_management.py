import os
import pathlib
import re
import zipfile
from io import TextIOWrapper
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from zipfile import ZipFile

_wout_period = re.compile(r"^\.")


def get_format_suffixes(filename):
    """returns file, compression suffixes"""
    filename = Path(filename)
    if not filename.suffix:
        return None, None

    compression_suffixes = ("bz2", "gz", "zip")
    suffixes = [_wout_period.sub("", sfx).lower() for sfx in filename.suffixes[-2:]]
    if suffixes[-1] in compression_suffixes:
        cmp_suffix = suffixes[-1]
    else:
        cmp_suffix = None

    if len(suffixes) == 2 and cmp_suffix is not None:
        suffix = suffixes[0]
    elif cmp_suffix is None:
        suffix = suffixes[-1]
    else:
        suffix = None
    return suffix, cmp_suffix


def open_zip(filename, mode="r", **kwargs):
    """open a single member zip-compressed file

    Note
    ----
    If mode="r". The function raises ValueError if zip has > 1 record.
    The returned object is wrapped by TextIOWrapper with latin encoding
    (so it's not a bytes string).

    If mode="w", returns an atomic_write() instance.
    """
    if mode.startswith("w"):
        return atomic_write(filename, mode=mode, in_zip=True)

    mode = mode.strip("t")
    with ZipFile(filename) as zf:
        if len(zf.namelist()) != 1:
            raise ValueError("Archive is supposed to have only one record.")
        opened = zf.open(zf.namelist()[0], mode=mode, **kwargs)
        return TextIOWrapper(opened, encoding="latin-1")


def open_(filename, mode="rt", **kwargs):
    """open that handles different compression"""
    from bz2 import open as bzip_open
    from gzip import open as gzip_open

    filename = Path(filename).expanduser().absolute()
    op = {".gz": gzip_open, ".bz2": bzip_open, ".zip": open_zip}.get(
        filename.suffix, open
    )
    return op(filename, mode, **kwargs)


class atomic_write:
    """performs atomic write operations, cleans up if fails"""

    def __init__(self, path, tmpdir=None, in_zip=None, mode="w"):
        path = pathlib.Path(path).expanduser()
        _, cmp = get_format_suffixes(path)
        if in_zip and cmp == "zip":
            in_zip = path if isinstance(in_zip, bool) else in_zip
            path = pathlib.Path(str(path)[: str(path).rfind(".zip")])

        self._path = path
        self._mode = mode
        self._file = None
        self._in_zip = in_zip
        self.succeeded = None
        self._close_func = (
            self._close_rename_zip if in_zip else self._close_rename_standard
        )
        if tmpdir is None:
            tmpdir = self._get_tmp_dir()
        self._tmpdir = tmpdir

    def _get_tmp_dir(self):
        """returns parent of destination file"""
        parent = Path(self._in_zip).parent if self._in_zip else Path(self._path).parent
        if not parent.exists():
            raise FileNotFoundError(f"{parent} directory does not exist")
        return parent

    def _get_fileobj(self):
        """returns file to be written to"""
        if self._file is None:
            self._file = NamedTemporaryFile(self._mode, delete=False, dir=self._tmpdir)

        return self._file

    def __enter__(self):
        return self._get_fileobj()

    def _close_rename_standard(self, p):
        try:
            f = Path(self._path)
            f.unlink()
        except FileNotFoundError:
            pass
        finally:
            p.rename(self._path)

    def _close_rename_zip(self, p):
        with zipfile.ZipFile(self._in_zip, "a") as out:
            out.write(str(p), arcname=self._path)

        p.unlink()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        p = Path(self._file.name)
        if exc_type is None:
            self._close_func(p)
            self.succeeded = True
        else:
            self.succeeded = False
            p.unlink()

    def write(self, text):
        """writes text to file"""
        fileobj = self._get_fileobj()
        fileobj.write(text)

    def close(self):
        """closes file"""
        self.__exit__(None, None, None)


def remove_files(list_of_filepaths, error_on_missing=True):
    """Remove list of filepaths, optionally raising an error if any are missing"""
    from os import remove

    missing = []
    for fp in list_of_filepaths:
        try:
            remove(fp)
        except OSError:
            missing.append(fp)

    if error_on_missing and missing:
        raise OSError("Some filepaths were not accessible: %s" % "\t".join(missing))
