import shutil
import os
from base.logger import *

def delete_folder(folder_path):
    """
    删除指定的文件夹，包括其中的所有文件和子文件夹
    
    参数:
        folder_path: 要删除的文件夹路径
    """
    try:
        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            logger.info(f"错误: 文件夹 '{folder_path}' 不存在")
            return
            
        # 检查是否是文件夹
        if not os.path.isdir(folder_path):
            logger.info(f"错误: '{folder_path}' 不是一个文件夹")
            return
            
        # 删除文件夹及其内容
        shutil.rmtree(folder_path)
        logger.info(f"文件夹 '{folder_path}' 已成功删除")
        
    except PermissionError:
        logger.info(f"错误: 没有权限删除 '{folder_path}'")
    except Exception as e:
        logger.info(f"删除文件夹时发生错误: {str(e)}")

# 使用示例
if __name__ == "__main__":
    # 要删除的文件夹路径
    folder_to_delete = "/path/to/your/folder"  # 替换为实际的文件夹路径
    delete_folder(folder_to_delete)
