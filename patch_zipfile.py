"""
Fix thread safety bug in ZipFile
https://bugs.python.org/issue42369
"""
import zipfile


class PatchedSharedFile(zipfile._SharedFile):
    """
    Credits and thanks to Kevin Mehall for this patch.
    https://bugs.python.org/issue42369#msg396792
    """

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.tell = lambda: self._pos


zipfile._SharedFile = PatchedSharedFile
