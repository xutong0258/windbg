import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class USB:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        cmd = ".load usb3kd"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        # time.sleep(TIME_OUT)

        cmd = "!usb_tree"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        # time.sleep(TIME_OUT)

        update_context(cmd_output, result_dict, 'usb_tree_Context')
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
