import os
from Ui import Ui
if os.name == 'nt':
    import sys
    import win32com.shell.shell as shell
ASADMIN = 'asadmin'


def start_linux_version():
    os.chmod('chromedriver', 0o777)
    os.chmod('phantomjs', 0o777)
    main()


def start_window_version():
    try:
        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            sys.exit(0)
        main()
    except:
        return False

"""
Kim Hyeock Jin
"""


def main():
    ui = Ui()
    ui.reader.terminate_all_drivers()

if __name__ == '__main__':
    if os.name == "posix":
        start_linux_version()
    elif os.name == "nt":
        start_window_version()
    # if os.name == ''  platform 을 이용하자!

