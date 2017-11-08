import os
import sys
if os.name == 'nt':
    import win32com.shell.shell as shell
from Ui import Ui
ASADMIN = 'asadmin'


def uac_require():
    try:
        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            sys.exit(0)
        return True
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
        os.chmod('chromedriver', 0o777)
        os.chmod('phantomjs', 0o777)
        main()
    if os.name == "nt":
        # if uac_require():  # 관리자 권한
            main()
    # if os.name == ''  platform 을 이용하자!

