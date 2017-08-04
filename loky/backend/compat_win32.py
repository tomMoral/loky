# flake8: noqa: F401
import sys

if sys.platform == "win32":
    # Avoid import error by code introspection tools such as test runners
    # trying to import this module while running on non-Windows systems.

    # Compat Popen
    if sys.version_info[:2] >= (3, 4):
        from multiprocessing.popen_spawn_win32 import Popen
    else:
        from multiprocessing.forking import Popen

    # wait compat
    if sys.version_info[:2] < (3, 3):
        from ._win_wait import wait
    else:
        from multiprocessing.connection import wait

    # Compat _winapi
    if sys.version_info[:2] >= (3, 4):
        import _winapi
    else:
        import os
        import msvcrt
        if sys.version_info[:2] < (3, 3):
            import _subprocess as win_api
            from _multiprocessing import win32
        else:
            import _winapi as win_api

        class _winapi:
            CreateProcess = win_api.CreateProcess

            @staticmethod
            def CreatePipe(*args):
                rfd, wfd = os.pipe()
                _current_process = win_api.GetCurrentProcess()
                rhandle = win_api.DuplicateHandle(
                    _current_process, msvcrt.get_osfhandle(rfd),
                    _current_process, 0, True,
                    win_api.DUPLICATE_SAME_ACCESS)
                if sys.version_info[:2] < (3, 3):
                    rhandle = rhandle.Detach()
                os.close(rfd)
                return rhandle, wfd

            @staticmethod
            def CloseHandle(h):
                if sys.version_info[:2] < (3, 3):
                    if type(h) != int:
                        h = h.Detach()
                    win32.CloseHandle(h)
                else:
                    win_api.CloseHandle(h)