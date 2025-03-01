__package__ = 'archivebox.config'

import os
import re
import platform

from typing import Dict
from pathlib import Path
from collections.abc import Mapping

from benedict import benedict

from ..misc.logging import DEFAULT_CLI_COLORS

from .paths import (
    PACKAGE_DIR,
    DATA_DIR,
    ARCHIVE_DIR,
    get_collection_id,
    get_machine_id,
    get_machine_type,
)
from .permissions import (
    IS_ROOT,
    IN_DOCKER,
    RUNNING_AS_UID,
    RUNNING_AS_GID,
    DEFAULT_PUID,
    DEFAULT_PGID,
    ARCHIVEBOX_USER,
    ARCHIVEBOX_GROUP,
)
from .version import detect_installed_version

###################### Config ##########################


class ConstantsDict(Mapping):
    PACKAGE_DIR: Path                   = PACKAGE_DIR
    DATA_DIR: Path                      = DATA_DIR
    ARCHIVE_DIR: Path                   = ARCHIVE_DIR
    
    MACHINE_TYPE: str                   = get_machine_type()
    MACHINE_ID: str                     = get_machine_id()
    COLLECTION_ID: str                  = get_collection_id(DATA_DIR)
    
    # Host system
    VERSION: str                        = detect_installed_version(PACKAGE_DIR)
    IN_DOCKER: bool                     = IN_DOCKER
    
    # Permissions
    IS_ROOT: bool                       = IS_ROOT
    ARCHIVEBOX_USER: int                = ARCHIVEBOX_USER
    ARCHIVEBOX_GROUP: int               = ARCHIVEBOX_GROUP
    RUNNING_AS_UID: int                 = RUNNING_AS_UID
    RUNNING_AS_GID: int                 = RUNNING_AS_GID
    DEFAULT_PUID: int                   = DEFAULT_PUID
    DEFAULT_PGID: int                   = DEFAULT_PGID
    
    # Source code dirs
    PACKAGE_DIR_NAME: str               = PACKAGE_DIR.name
    TEMPLATES_DIR_NAME: str             = 'templates'
    TEMPLATES_DIR: Path                 = PACKAGE_DIR / TEMPLATES_DIR_NAME
    STATIC_DIR_NAME: str                = 'static'
    STATIC_DIR: Path                    = TEMPLATES_DIR / STATIC_DIR_NAME

    # Data dirs
    ARCHIVE_DIR_NAME: str               = 'archive'
    SOURCES_DIR_NAME: str               = 'sources'
    PERSONAS_DIR_NAME: str              = 'personas'
    CRONTABS_DIR_NAME: str              = 'crontabs'
    CACHE_DIR_NAME: str                 = 'cache'
    LOGS_DIR_NAME: str                  = 'logs'
    USER_PLUGINS_DIR_NAME: str          = 'user_plugins'
    CUSTOM_TEMPLATES_DIR_NAME: str      = 'user_templates'
    ARCHIVE_DIR: Path                   = DATA_DIR / ARCHIVE_DIR_NAME
    SOURCES_DIR: Path                   = DATA_DIR / SOURCES_DIR_NAME
    PERSONAS_DIR: Path                  = DATA_DIR / PERSONAS_DIR_NAME
    LOGS_DIR: Path                      = DATA_DIR / LOGS_DIR_NAME
    CACHE_DIR: Path                     = DATA_DIR / CACHE_DIR_NAME
    CUSTOM_TEMPLATES_DIR: Path          = DATA_DIR / CUSTOM_TEMPLATES_DIR_NAME
    USER_PLUGINS_DIR: Path              = DATA_DIR / USER_PLUGINS_DIR_NAME

    # Data dir files
    CONFIG_FILENAME: str                = 'ArchiveBox.conf'
    SQL_INDEX_FILENAME: str             = 'index.sqlite3'
    QUEUE_DATABASE_FILENAME: str        = 'queue.sqlite3'
    CONFIG_FILE: Path                   = DATA_DIR / CONFIG_FILENAME
    DATABASE_FILE: Path                 = DATA_DIR / SQL_INDEX_FILENAME
    QUEUE_DATABASE_FILE: Path           = DATA_DIR / QUEUE_DATABASE_FILENAME
    
    JSON_INDEX_FILENAME: str            = 'index.json'
    HTML_INDEX_FILENAME: str            = 'index.html'
    ROBOTS_TXT_FILENAME: str            = 'robots.txt'
    FAVICON_FILENAME: str               = 'favicon.ico'
    
    # Runtime dirs
    TMP_DIR_NAME: str                   = 'tmp'
    TMP_DIR: Path                       = DATA_DIR / TMP_DIR_NAME / MACHINE_ID
    LIB_DIR_NAME: str                   = 'lib'
    LIB_DIR: Path                       = DATA_DIR / LIB_DIR_NAME / MACHINE_TYPE
    LIB_PIP_DIR: Path                   = LIB_DIR / 'pip'
    LIB_NPM_DIR: Path                   = LIB_DIR / 'npm'
    LIB_BROWSERS_DIR: Path              = LIB_DIR / 'browsers'
    LIB_BIN_DIR: Path                   = LIB_DIR / 'bin'
    BIN_DIR: Path                       = LIB_BIN_DIR

    # Config constants
    TIMEZONE: str                       = 'UTC'
    DEFAULT_CLI_COLORS: Dict[str, str]  = DEFAULT_CLI_COLORS
    DISABLED_CLI_COLORS: Dict[str, str] = benedict({k: '' for k in DEFAULT_CLI_COLORS})

    ALLOWDENYLIST_REGEX_FLAGS: int      = re.IGNORECASE | re.UNICODE | re.MULTILINE

    STATICFILE_EXTENSIONS: frozenset[str] = frozenset((
        # 99.999% of the time, URLs ending in these extensions are static files
        # that can be downloaded as-is, not html pages that need to be rendered
        'gif', 'jpeg', 'jpg', 'png', 'tif', 'tiff', 'wbmp', 'ico', 'jng', 'bmp',
        'svg', 'svgz', 'webp', 'ps', 'eps', 'ai',
        'mp3', 'mp4', 'm4a', 'mpeg', 'mpg', 'mkv', 'mov', 'webm', 'm4v',
        'flv', 'wmv', 'avi', 'ogg', 'ts', 'm3u8',
        'pdf', 'txt', 'rtf', 'rtfd', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx',
        'atom', 'rss', 'css', 'js', 'json',
        'dmg', 'iso', 'img',
        'rar', 'war', 'hqx', 'zip', 'gz', 'bz2', '7z',

        # Less common extensions to consider adding later
        # jar, swf, bin, com, exe, dll, deb
        # ear, hqx, eot, wmlc, kml, kmz, cco, jardiff, jnlp, run, msi, msp, msm,
        # pl pm, prc pdb, rar, rpm, sea, sit, tcl tk, der, pem, crt, xpi, xspf,
        # ra, mng, asx, asf, 3gpp, 3gp, mid, midi, kar, jad, wml, htc, mml

        # These are always treated as pages, not as static files, never add them:
        # html, htm, shtml, xhtml, xml, aspx, php, cgi
    ))

    PIP_RELATED_NAMES: frozenset[str] = frozenset((
        ".venv",
        "venv",
        "virtualenv",
        ".virtualenv",
    ))
    NPM_RELATED_NAMES: frozenset[str] = frozenset((
        "node_modules",
        "package.json",
        "package-lock.json",
        "yarn.lock",
    ))

    # When initializing archivebox in a new directory, we check to make sure the dir is
    # actually empty so that we dont clobber someone's home directory or desktop by accident.
    # These files are exceptions to the is_empty check when we're trying to init a new dir,
    # as they could be from a previous archivebox version, system artifacts, dependencies, etc.
    ALLOWED_IN_DATA_DIR: frozenset[str] = frozenset((
        *PIP_RELATED_NAMES,
        *NPM_RELATED_NAMES,
        
        ### Dirs:
        ARCHIVE_DIR_NAME,
        SOURCES_DIR_NAME,
        LOGS_DIR_NAME,
        CACHE_DIR_NAME,
        LIB_DIR_NAME,
        TMP_DIR_NAME,
        PERSONAS_DIR_NAME,
        CUSTOM_TEMPLATES_DIR_NAME,
        USER_PLUGINS_DIR_NAME,
        CRONTABS_DIR_NAME,
        "static",                # created by old static exports <v0.6.0
        "sonic",                 # created by docker bind mount / sonic FTS process
        ".git",
        ".svn",
        
        ### Files:
        CONFIG_FILENAME,
        SQL_INDEX_FILENAME,
        f"{SQL_INDEX_FILENAME}-wal",
        f"{SQL_INDEX_FILENAME}-shm",
        QUEUE_DATABASE_FILENAME,
        f"{QUEUE_DATABASE_FILENAME}-wal",
        f"{QUEUE_DATABASE_FILENAME}-shm",
        "search.sqlite3",
        JSON_INDEX_FILENAME,
        HTML_INDEX_FILENAME,
        ROBOTS_TXT_FILENAME,
        FAVICON_FILENAME,
        CONFIG_FILENAME,
        f"{CONFIG_FILENAME}.bak",
        f".{CONFIG_FILENAME}.bak",
        "static_index.json",
        ".DS_Store",
        ".gitignore",
        "lost+found",
        ".DS_Store",
        ".env",
        ".collection_id",
        ".archivebox_id",
        "Dockerfile",
    ))

    CODE_LOCATIONS = benedict({
        'PACKAGE_DIR': {
            'path': (PACKAGE_DIR).resolve(),
            'enabled': True,
            'is_valid': os.access(PACKAGE_DIR / '__main__.py', os.X_OK),                                                                  # executable
        },
        'TEMPLATES_DIR': {
            'path': TEMPLATES_DIR.resolve(),
            'enabled': True,
            'is_valid': os.access(STATIC_DIR, os.R_OK) and os.access(STATIC_DIR, os.X_OK),                                                # read + list
        },
        'LIB_DIR': {
            'path': LIB_DIR.resolve(),
            'enabled': True,
            'is_valid': os.access(LIB_DIR, os.R_OK) and os.access(LIB_DIR, os.X_OK) and os.access(LIB_DIR, os.W_OK),                      # read + write
        },
        'TMP_DIR': {
            'path': TMP_DIR.resolve(),
            'enabled': True,
            'is_valid': os.access(TMP_DIR, os.R_OK) and os.access(TMP_DIR, os.X_OK) and os.access(TMP_DIR, os.W_OK),                      # read + write
        },
    })
        
    DATA_LOCATIONS = benedict({
        "DATA_DIR": {
            "path": DATA_DIR.resolve(),
            "enabled": True,
            "is_valid": os.access(DATA_DIR, os.R_OK) and os.access(DATA_DIR, os.W_OK) and os.access(DATA_DIR, os.X_OK),
            "is_mount": os.path.ismount(DATA_DIR.resolve()),
        },
        "CONFIG_FILE": {
            "path": CONFIG_FILE.resolve(),
            "enabled": True,
            "is_valid":  os.access(CONFIG_FILE, os.R_OK) and os.access(CONFIG_FILE, os.W_OK),
        },
        "SQL_INDEX": {
            "path": DATABASE_FILE.resolve(),
            "enabled": True,
            "is_valid": os.access(DATABASE_FILE, os.R_OK) and os.access(DATABASE_FILE, os.W_OK),
            "is_mount": os.path.ismount(DATABASE_FILE.resolve()),
        },
        "QUEUE_DATABASE": {
            "path": QUEUE_DATABASE_FILE.resolve(),
            "enabled": True,
            "is_valid": os.access(QUEUE_DATABASE_FILE, os.R_OK) and os.access(QUEUE_DATABASE_FILE, os.W_OK),
            "is_mount": os.path.ismount(QUEUE_DATABASE_FILE.resolve()),
        },
        "ARCHIVE_DIR": {
            "path": ARCHIVE_DIR.resolve(),
            "enabled": True,
            "is_valid": os.access(ARCHIVE_DIR, os.R_OK) and os.access(ARCHIVE_DIR, os.W_OK) and os.access(ARCHIVE_DIR, os.X_OK),
            "is_mount": os.path.ismount(ARCHIVE_DIR.resolve()),
        },
        "SOURCES_DIR": {
            "path": SOURCES_DIR.resolve(),
            "enabled": True,
            "is_valid": os.access(SOURCES_DIR, os.R_OK) and os.access(SOURCES_DIR, os.W_OK) and os.access(SOURCES_DIR, os.X_OK),
        },
        "LOGS_DIR": {
            "path": LOGS_DIR.resolve(),
            "enabled": True,
            "is_valid": os.access(LOGS_DIR, os.R_OK) and os.access(LOGS_DIR, os.W_OK) and os.access(LOGS_DIR, os.X_OK),                              # read + write
        },
        # "CACHE_DIR": {
        #     "path": CACHE_DIR.resolve(),
        #     "enabled": True,
        #     "is_valid": os.access(CACHE_DIR, os.R_OK) and os.access(CACHE_DIR, os.W_OK) and os.access(CACHE_DIR, os.X_OK),                        # read + write
        # },
        "PERSONAS_DIR": {
            "path": PERSONAS_DIR.resolve(),
            "enabled": os.access(PERSONAS_DIR, os.R_OK),
            "is_valid": os.access(PERSONAS_DIR, os.R_OK) and os.access(PERSONAS_DIR, os.W_OK) and os.access(PERSONAS_DIR, os.X_OK),                 # read + write
        },
        'CUSTOM_TEMPLATES_DIR': {
            'path': CUSTOM_TEMPLATES_DIR.resolve(),
            'enabled': os.access(CUSTOM_TEMPLATES_DIR, os.R_OK),
            'is_valid': os.access(CUSTOM_TEMPLATES_DIR, os.R_OK) and os.access(CUSTOM_TEMPLATES_DIR, os.X_OK),                                      # read
        },
        'USER_PLUGINS_DIR': {
            'path': USER_PLUGINS_DIR.resolve(),
            'enabled': os.access(USER_PLUGINS_DIR, os.R_OK),
            'is_valid': os.access(USER_PLUGINS_DIR, os.R_OK) and os.access(USER_PLUGINS_DIR, os.X_OK),                                              # read
        },
    })

    @classmethod
    def __getitem__(cls, key: str):
        return getattr(cls, key)
    
    @classmethod
    def __benedict__(cls):
        return benedict({key: value for key, value in cls.__dict__.items() if key.isupper() and not key.startswith('_')})
    
    @classmethod
    def __len__(cls):
        return len(cls.__benedict__())

    @classmethod
    def __iter__(cls):
        return iter(cls.__benedict__())

CONSTANTS = ConstantsDict()
CONSTANTS_CONFIG = CONSTANTS.__benedict__()

# add all key: values to globals() for easier importing
globals().update(CONSTANTS)
