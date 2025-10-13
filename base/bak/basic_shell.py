import subprocess
import os
from base.contants import *

windbgx_path=r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\WinDbgX.exe"
kdX86_path = r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\kdX86.exe"
def analyze_dump(dump_path):
    args = [windbgx_path,
            "-z", dump_path,
            "-c", ".logopen 3.log",
            # "-y", f'{SYMBOL_PATH}',
            "-c", "!analyze  -v",
            # "-c", ".logclose",
            # "-c", "qqd"
            ]

    process = subprocess.Popen(
            args=args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

    print(f'hello')
    # 提供输入
    input_data = "张三\n25\n"
    input_data = f"{windbgx_path} -c .logclose\n"
    stdout, stderr = process.communicate(input=input_data)

    print(f'hello2')
    return

if __name__ == '__main__':
    # 批量处理 Dump 文件
    dump_file = r"D:\0_LOG_VIP\11\0x9f_3_Disk_FastBoot\MEMORY.DMP"
    analyze_dump(dump_file)