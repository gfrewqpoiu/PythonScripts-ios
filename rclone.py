import decimal
import json
from abc import ABC
from pathlib import *

rclone_flags = '--fast-list'


def decode(input):
    if input is None:
        return
    return json.loads(input)


def split(list):
    files = []
    folders = []
    for item in list:
        if item["IsDir"]:
            folders.append(item)
        else:
            files.append(item)
    return files, folders


class RcloneItem(ABC):
    """Represents the concept of an object on a rclone Drive.
    Both files and folders."""

    def __init__(self, item, drive: str, path):
        self.drive = drive
        self.path = PurePosixPath(path, item['Path'])
        if not drive.endswith(':'):
            drive += ':'
        self.fullpath = PurePosixPath(drive, self.path)
        self.name = item['Name']
        self.parent = self.path.parent
        self.is_directory = False
        self._size = None
        self._hash = None

    def __str__(self):
        return self.name

    async def get_size(self):
        raise NotImplementedError

    async def get_size_str(self):
        size = decimal.Decimal(await self.get_size())
        if size > 1024:
            size = size / 1024 #KB
            if size > 1024:
                size = size / 1024 #MB
                if size > 1024:
                    size = size / 1024 #GB
                    if size > 1024:
                        size = size / 1024 #TB
                        if size > 1024:
                            size = size / 1024 #PB
                            return str(round(size, 3)) + " PBytes"
                        else:
                            return str(round(size, 3)) + " TBytes"
                    else:
                        return str(round(size, 3)) + " GBytes"
                else:
                    return str(round(size, 3))+ " MBytes"

            else:
                return str(round(size, 3)) + " KBytes"

        else:
            return str(size) + " Bytes"


class RcloneFile(RcloneItem):
    """Represents a file on a Rclone Drive"""

    def __init__(self, item, drive, path):
        super().__init__(item, drive, path)
        self.filetype = item['MimeType']
        self.purename = self.path.stem
        self.extension = self.path.suffix
        if int(item["Size"]) > 0:
            self._size = item['Size']
        else:
            self._size = 0

    async def get_size(self):
        return self._size

    def get_hash(self):
        if self._hash is None:
            self._hash = fetch_hash(self.fullpath)
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, RcloneFile):
            return False
        hash1 = self.get_hash()
        hash2 = other.get_hash()
        if (hash1 == hash2) and (self.get_size() == other.get_size()):
            return True
        else:
            return False


class RcloneDirectory(RcloneItem):
    """Represents a folder on a rclone Drive"""

    def __init__(self, item, drive, path):
        super().__init__(item, drive, path)
        self.is_directory = True
        self.populated = False
        self._contents = []
        self._amount = -1

    async def populate(self):
        self._contents = await ls(self.drive, self.path)
        self.populated = True

    async def get_contents(self, recursive = False):
        if not self.populated:
            await self.populate()
        if recursive:
            for item in self._contents:
                if isinstance(item, RcloneDirectory):
                    await item.get_contents(True)
        return self._contents

    async def get_size(self):
        if self._size is None:
            self._amount, self._size = await size(self.fullpath)
        if self._size < 0:
            self._size = 0
        return self._size

    async def get_amount(self):
        if self._size is None:
            await self.get_size()
        return self._amount


async def ls(drive: str, directory, recursive_flat=False) -> [RcloneItem]:
    raise NotImplementedError


async def tree(drive, directory) -> RcloneDirectory:
    raise NotImplementedError

    async def fill_path(path: RcloneDirectory, items: list):
        raise NotImplementedError


async def flatls(drive: str, directory: str or PurePosixPath) -> [RcloneItem]:
    raise NotImplementedError


async def size(full_path: str or PurePosixPath):
    raise NotImplementedError


async def fetch_hash(full_path: str or PurePosixPath):
    raise NotImplementedError

async def copy(src_full_path: PurePosixPath, dest_full_path: PurePosixPath):
    raise NotImplementedError


async def move(src_full_path: str or PurePosixPath, dest_full_path: str or PurePosixPath):
    raise NotImplementedError


async def delete_file(full_path: str or PurePosixPath):
    raise NotImplementedError


async def sync(src_full_path: str or PurePosixPath, dest_full_path: str or PurePosixPath, *args):
    raise NotImplementedError


async def main():
    raise NotImplementedError
