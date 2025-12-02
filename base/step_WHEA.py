import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class WHEA_0x124:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        BUGCHECK_P2 = Automatic_dict.get('BUGCHECK_P2')
        WHEA_Status_Abnormal = 1
        result_dict['WHEA_Status_Abnormal'] = WHEA_Status_Abnormal

        WHEA_ERROR_RECORD_Address = BUGCHECK_P2

        # errrec WHEA_ERROR_RECORD_Address
        cmd = f"!errrec {WHEA_ERROR_RECORD_Address}"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        # logger.info(f'errrec cmd_output: {cmd_output}')

        result_dict['WHEA_ERROR_RECORD_Context'] = cmd_output

        cmd_output_list = cmd_output.splitlines()

        WHEA_ERROR_RECORD_Type = get_list_text_line(cmd_output_list, 'Notify Type')
        CPU_Status_Abnormal = 0
        if WHEA_ERROR_RECORD_Type:
            WHEA_ERROR_RECORD_Type = WHEA_ERROR_RECORD_Type.replace('Notify Type', '').strip()
            WHEA_ERROR_RECORD_Type = WHEA_ERROR_RECORD_Type.replace(':', '').strip()
            logger.info(f'WHEA_ERROR_RECORD_Type: {WHEA_ERROR_RECORD_Type}')
            result_dict['WHEA_ERROR_RECORD_Type'] = WHEA_ERROR_RECORD_Type
            result_dict['BSOD_Suspicious_Device'] = WHEA_ERROR_RECORD_Type
            if 'Machine Check Exception' == WHEA_ERROR_RECORD_Type:
                CPU_Status_Abnormal = 1

        result_dict['CPU_Status_Abnormal'] = CPU_Status_Abnormal
        logger.info(f'CPU_Status_Abnormal: {CPU_Status_Abnormal}')

        # !WHEA
        cmd = f"!WHEA"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        # logger.info(f'WHEA cmd_output: {cmd_output}')
        result_dict['WHEA_Context'] = cmd_output
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
