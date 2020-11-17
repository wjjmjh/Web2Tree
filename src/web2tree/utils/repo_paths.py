import os


def _wrapping_refreshing(func):
    def wrapped(self):
        got = func(self)
        self.refresh_base()
        return got

    return wrapped


# A manager that efficiently manages paths in this repo.
class repoPathManager:
    def __init__(self):
        self.base = ""

    def refresh_base(self):
        self.base = ""

    def _combine_one(self, component):
        self.base = os.path.join(self.base, component)

    def combine(self, *directed_folders):
        for folder in directed_folders:
            self._combine_one(folder)
        got = self.base
        self.refresh_base()
        return got

    def find_root(self):
        explore = str(os.path.dirname(os.path.abspath(__file__))).split(os.sep)
        self.base = os.path.sep.join(explore[: explore.index("Web2Tree") + 1])
        return self

    def find_src(self):
        explore = str(os.path.dirname(os.path.abspath(__file__))).split(os.sep)
        self.base = os.path.sep.join(explore[: explore.index("src") + 1])
        return self

    def find_tests(self):
        self.find_root()
        self._combine_one("tests")
        return self

    @property
    def test_data(self):
        self.find_root()
        return self.combine("tests", "data")

    @property
    @_wrapping_refreshing
    def web2tree(self):
        self.find_src()
        self._combine_one("web2tree")
        return self.base

    @property
    @_wrapping_refreshing
    def output(self):
        self.find_src()
        self._combine_one("output")
        return self.base
