from pathlib import Path

def get_latest_file_recursive(directory, pattern="*"):
    path = Path(directory)
    files = [f for f in path.rglob(pattern) if f.is_file()]
    print(files)
    if not files:
        return None
    return str(max(files, key=lambda f: f.stat().st_mtime))

# 示例：递归查找所有 .py 文件中最新的
latest_py = get_latest_file_recursive(r"D:\00\04_异常关机重启唤不醒\log\OneDrive_8_2025-10-30\JINGWEI2_IML-SVT-LE46081L004-41A6B8AB", "*.dump")
