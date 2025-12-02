import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger

class Current_thread:
    def __init__(self):
        return

    def run(self, result_dict, current_step):
        cmd = "!thread"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        result_dict['thread_Context'] = cmd_output

        cmd = "!running -it"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        result_dict['running_Context'] = cmd_output

        Current_Thread_Power_Status_Abnormal = 0
        result_dict['Current_Thread_Power_Status_Abnormal'] = Current_Thread_Power_Status_Abnormal
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
