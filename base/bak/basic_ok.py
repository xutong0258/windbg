import subprocess
import os
from base.helper import *
from base import fileOP
windbgx_path=r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\WinDbgX.exe"


def windbg_dump_file():
    # 批量处理 Dump 文件
    dump_dir = r"D:\0_LOG_VIP\11\0x9f_3_Disk_FastBoot"
    for dump_file in os.listdir(dump_dir):
        if not dump_file.endswith(".DMP"):
            continue

        dump_path = os.path.join(dump_dir, dump_file)
        args = [windbgx_path,
                "-z", dump_path,
                "-c", ".logopen 3.log",
                "-c", "!analyze  -v",
                "-c", ".logclose",
                "-c", "qqd"]
        windbg(args=args)
    return

if __name__ == '__main__':

    pass