import logging
from pathlib import *
import sys
from collections import deque
if sys.platform != "ios":
    raise EnvironmentError("This is only for Pythonista on iOS")

temppath = Path(Path.cwd(), 'tmp')
basepath = PurePosixPath("Videos/")
logging.basicConfig(level=logging.INFO)
server = None
queue = deque()
running_job = None

class Job():
    """Dummy Job Class for Pythonista"""
    _temppath = temppath
    newext = ".mp4"
    log = logging.getLogger()

    def __init__(self, inputfile):
        self.is_downloaded = False
        self.is_converted = False
        self.is_uploaded = False
        self.inputfile = inputfile
        self.path = Path(self._temppath, self.inputfile.name)
        self.newfilepath = self.path.with_suffix('.mp4')
        self.parentpath = self.inputfile.fullpath.parent
        self.newname = self.inputfile.purename
        self.newname += '.mp4'
        self.log.debug("New Job created with:")
        self.log.debug("Inputtfile: " + str(inputfile.path))

    def __str__(self):
        return f"{self.inputfile.purename}: Downloaded: {self.is_downloaded}, Converted: {self.is_converted}, Uploaded: {self.is_uploaded}"
