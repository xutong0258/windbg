import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger

class Process_vm:
    def __init__(self):
        return

    def run(self, result_dict, current_step):
        cmd = "!VM"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        # time.sleep(15)

        result_dict['VM_Context'] = cmd_output
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
