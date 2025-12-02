import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class NDIS:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        cmd = ".load ndiskd"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

        cmd = "!ndiskd.oid"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        update_context(cmd_output, result_dict, 'NDIS_OID_Context')

        cmd_output_list = cmd_output.splitlines()
        Ndis_netadapter1_address, Ndis_netadapter2_address = parse_ndiskd_oid(cmd_output_list, result_dict)

        if Ndis_netadapter1_address:
            cmd = f"!ndiskd.netadapter {Ndis_netadapter1_address}"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
            update_context(cmd_output, result_dict, 'NDIS_netadapter1_Context')

        # Ndis_netadapter2_address
        if Ndis_netadapter2_address:
            cmd = f"!ndiskd.netadapter {Ndis_netadapter2_address}"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
            update_context(cmd_output, result_dict, 'NDIS_netadapter2_Context')

        NDIS_OID_Pending_Status = result_dict.get('NDIS_OID_Pending_Status', None)
        NDIS_Status_Abnormal = 0
        if NDIS_OID_Pending_Status:
            NDIS_Status_Abnormal = 1
        result_dict['NDIS_Status_Abnormal'] = NDIS_Status_Abnormal
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
