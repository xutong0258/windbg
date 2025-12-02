import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import parse_analyze_v


class Analyze_v:
    def __init__(self):
        return

    def run(self, result_dict, clue_step, current_step):
        # time.sleep(3)  # 等待初始化
        cmd = "!analyze -v"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step=1, timeout=15)

        # logger.info(f'cmd_output type:\n{cmd_output}')

        parse_analyze_v(cmd_output, result_dict)
        clue_step.append(f'command: !analyze -v, get: BUGCHECK_Code, BUGCHECK_P1-BUGCHECK_P4, FAILURE_BUCKET_ID')
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
