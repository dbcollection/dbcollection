"""
Global exception and warning classes.
"""


class MD5HashNotEqual(Exception):
    """The MD5 hashes are not equal."""
    pass


class URLDoesNotExist(Exception):
    """URL path does not exist."""
    pass


class GoogleDriveFileIdDoesNotExist(Exception):
    """Google drive's file id does not exist."""
    pass


class InvalidURLDownloadSource(Exception):
    """The url source is invalid/undefined."""
    pass
