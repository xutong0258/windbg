import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class PnP:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        # "!pnptriage"
        pnptriage(result_dict, current_step)

        # !irp blocked_IRP_address
        blocked_IRP_Address = result_dict.get('blocked_IRP_Address', None)
        blocked_device_Address = None
        if blocked_IRP_Address:
            blocked_device_Address = irp_blocked_IRP_Address(result_dict, blocked_IRP_Address, current_step)

        # !devstack blocked_device_Address
        if blocked_device_Address:
            devstack_blocked_device_Address(result_dict, blocked_device_Address, current_step)

        cmd = "!devnode 1"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        cmd_output_list = cmd_output.splitlines()
        count = get_list_text_count(cmd_output_list, 'Pending Removal')
        Pending_Removal_Status = 0
        if count:
            Pending_Removal_Status = 1
            update_context(cmd_output, result_dict, 'Pending_Removal_Context')

        result_dict['pending_Removal_status'] = Pending_Removal_Status

        cmd = "!devnode 0 1"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

        PnP_blocked_IRP_address_status = result_dict.get('PnP_blocked_IRP_address_status', None)

        # !powertriage
        powertriage(result_dict, current_step)

        PnP_Status_Abnormal = 0
        if PnP_blocked_IRP_address_status or Pending_Removal_Status:
            PnP_Status_Abnormal = 1

        result_dict['PnP_Status_Abnormal'] = PnP_Status_Abnormal


        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
