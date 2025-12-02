import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import parse_vertarget, parse_sysinfo_cpuspeed

class System_info:
    def __init__(self):
        return

    def run(self, result_dict, current_step):
        cmd = "vertarget"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        parse_vertarget(cmd_output, result_dict)

        cmd = "!sysinfo cpuinfo"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        result_dict['cpuinfo_Context'] = cmd_output

        cmd = "!sysinfo cpumicrocode"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        result_dict['cpumicrocode_context'] = cmd_output

        cmd = "!sysinfo cpuspeed"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        parse_sysinfo_cpuspeed(cmd_output, result_dict)

        #
        cmd = "!sysinfo smbios"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        result_dict['smbios_context'] = cmd_output
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
