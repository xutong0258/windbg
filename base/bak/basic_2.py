import subprocess
import os

windbgx_path=r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\WinDbgX.exe"

def analyze_dump(dump_path):
    args = [windbgx_path,
            "-z", dump_path,
            "-c", ".logopen 3.log",
            "-c", "!analyze  -v",
            "-c", ".logclose",
            "-c", "qqd"]

    # 调用 WinDbgX 执行命令
    try:
        process = subprocess.Popen(args)
        process.wait()
        logger.info(f"结果已保存到")
    except Exception as e:
        logger.info(f"错误: {str(e)}")
    return

if __name__ == '__main__':
    # 批量处理 Dump 文件
    dump_dir = r"D:\0_LOG_VIP\11\0x9f_3_Disk_FastBoot"
    for dump_file in os.listdir(dump_dir):
        if dump_file.endswith(".DMP"):
            analyze_dump(os.path.join(dump_dir, dump_file))