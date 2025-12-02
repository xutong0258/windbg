import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class DPC:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        result_dict['The_DPC_Status_Abnormal'] = 1

        cmd = "!swd"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        update_context(cmd_output, result_dict, 'swd_DPCTimeout_Context')

        swd_DPCTimeout_CPU = None
        if cmd_output:
            cmd_output_list = cmd_output.splitlines()
            Bugcheck_P1 = Automatic_dict['BUGCHECK_P1']
            logger.info(f'Bugcheck_P1: {Bugcheck_P1}')
            if Bugcheck_P1 == '0':
                swd_DPCTimeout_CPU = fileOP.get_swd_DPCTimeout_CPU_P1_0(cmd_output_list)
            elif Bugcheck_P1 == '1':
                swd_DPCTimeout_CPU = fileOP.get_swd_DPCTimeout_CPU_P1_1(cmd_output_list)
        logger.info(f'swd_DPCTimeout_CPU: {swd_DPCTimeout_CPU}')
        result_dict['swd_DPCTimeout_CPU'] = swd_DPCTimeout_CPU

        cmd = "!dpcwatchdog"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        update_context(cmd_output, result_dict, 'dpcwatchdog_context')

        swd_DPCTimeout_CPU = result_dict.get('swd_DPCTimeout_CPU', None)
        logger.info(f'swd_DPCTimeout_CPU: {swd_DPCTimeout_CPU}')
        if swd_DPCTimeout_CPU is not None:
            cmd = f"~{swd_DPCTimeout_CPU}"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
            result_dict['thread_Context'] = cmd_output

            cmd = f"!thread"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
            update_context(cmd_output, result_dict, 'thread_Context')

        cmd = "!running -it"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        update_context(cmd_output, result_dict, 'running_Context')
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
