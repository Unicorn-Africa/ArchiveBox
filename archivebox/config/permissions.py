__package__ = 'archivebox.config'

import os
import pwd
import sys

from rich import print

from pathlib import Path
from contextlib import contextmanager

#############################################################################################

DATA_DIR = Path(os.getcwd())

try:
    DATA_DIR_STAT           = DATA_DIR.stat()
    DATA_DIR_UID            = DATA_DIR_STAT.st_uid
    DATA_DIR_GID            = DATA_DIR_STAT.st_gid
except PermissionError:
    DATA_DIR_UID            = 0
    DATA_DIR_GID            = 0

DEFAULT_PUID            = 911
DEFAULT_PGID            = 911
RUNNING_AS_UID          = os.getuid()
RUNNING_AS_GID          = os.getgid()
EUID                    = os.geteuid()
EGID                    = os.getegid()
USER: str               = Path('~').expanduser().resolve().name

IS_ROOT = RUNNING_AS_UID == 0
IN_DOCKER = os.environ.get('IN_DOCKER', False) in ('1', 'true', 'True', 'TRUE', 'yes')

FALLBACK_UID = RUNNING_AS_UID
FALLBACK_GID = RUNNING_AS_GID
if RUNNING_AS_UID == 0:
    try:
        # if we are running as root it's really hard to figure out what the correct archivebox user should be
        # as a last resort instead of setting DATA_DIR ownership to 0:0 (which breaks it for non-root users)
        # check if 911:911 archivebox user exists on host system, and use it instead of 0
        import pwd
        if pwd.getpwuid(DEFAULT_PUID).pw_name == 'archivebox':
            FALLBACK_UID = DEFAULT_PUID
            FALLBACK_GID = DEFAULT_PGID
    except Exception:
        pass


os.environ.setdefault('PUID', str(DATA_DIR_UID or EUID or RUNNING_AS_UID or FALLBACK_UID))
os.environ.setdefault('PGID', str(DATA_DIR_GID or EGID or RUNNING_AS_GID or FALLBACK_GID))

ARCHIVEBOX_USER = int(os.environ['PUID'])
ARCHIVEBOX_GROUP = int(os.environ['PGID'])
if not USER:
    try:
        # alternative method 1 to get username
        USER = pwd.getpwuid(ARCHIVEBOX_USER).pw_name
    except Exception:
        pass
        
if not USER:
    try:
        # alternative method 2 to get username
        import getpass
        USER = getpass.getuser()
    except Exception:
        pass
    
if not USER:
    try:
        # alternative method 3 to get username
        USER = os.getlogin() or 'archivebox'
    except Exception:
        USER = 'archivebox'
        
ARCHIVEBOX_USER_EXISTS = False
try:
    pwd.getpwuid(ARCHIVEBOX_USER)
    ARCHIVEBOX_USER_EXISTS = True
except Exception:
    ARCHIVEBOX_USER_EXISTS = False
    

#############################################################################################

def drop_privileges():
    """If running as root, drop privileges to the user that owns the data dir (or PUID)"""
    
    # always run archivebox as the user that owns the data dir, never as root
    if os.getuid() == 0:
        # drop permissions to the user that owns the data dir / provided PUID
        if os.geteuid() != ARCHIVEBOX_USER and ARCHIVEBOX_USER != 0 and ARCHIVEBOX_USER_EXISTS:
            os.seteuid(ARCHIVEBOX_USER)
            
            # try:
            #     from .paths import PACKAGE_DIR
            # except ModuleNotFoundError:
            #     print(f'[red][X] Failed to get package dir for {__file__}[/red]')
                
            # if not os.access(__file__, os.R_OK):
            #     # ARCHIVEBOX_USER is not able to read the source code, chown it so they can
            #     with SudoPermission(uid=0, fallback=True):
            #         os.system(f'chown -R :{ARCHIVEBOX_GROUP} "{PACKAGE_DIR}"')
        # if we need sudo (e.g. for installing dependencies) code should use SudoPermissions() context manager to regain root
    if ARCHIVEBOX_USER == 0 or not ARCHIVEBOX_USER_EXISTS:
        print('[yellow]:warning:  Running as [red]root[/red] is not recommended and may make your [blue]DATA_DIR[/blue] inaccessible to other users on your system.[/yellow]', file=sys.stderr)


@contextmanager
def SudoPermission(uid=0, fallback=False):
    """Attempt to run code with sudo permissions for a given user (or root)"""
    
    if os.geteuid() == uid:
        # no need to change effective UID, we are already that user
        yield
        return

    try:
        # change our effective UID to the given UID
        os.seteuid(uid)
    except PermissionError as err:
        if not fallback:
            raise PermissionError(f'Not enough permissions to run code as uid={uid}, please retry with sudo') from err
    try:
        # yield back to the caller so they can run code inside context as root
        yield
    finally:
        # then set effective UID back to DATA_DIR owner
        try:
            os.seteuid(ARCHIVEBOX_USER)
        except PermissionError as err:
            if not fallback:
                raise PermissionError(f'Failed to revert uid={uid} back to {ARCHIVEBOX_USER} after running code with sudo') from err
