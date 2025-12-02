import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class Power_0x9f_4:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        result_dict['The_Power_Management_Status_Abnormal'] = 1
        # result_dict['blocked_IRP_address_status'] = 0

        Bugcheck_P3 = Automatic_dict['BUGCHECK_P3']
        blocked_thread_Address = Bugcheck_P3
        result_dict['blocked_thread_Address'] = blocked_thread_Address

        # !poaction
        cmd = f'!poaction'
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        result_dict['poaction_context'] = cmd_output

        # !thread blocked_thread_Address
        blocked_IRP_Address = thread_blocked_thread_Address(result_dict, blocked_thread_Address, current_step)
        if blocked_IRP_Address is not None:
            blocked_device_Address = irp_blocked_IRP_Address(result_dict, blocked_IRP_Address, current_step)

            blocked_device_Address = result_dict.get('blocked_device_Address', None)
            logger.info(f'blocked_device_Address: {blocked_device_Address}')
            # !devstack blocked_device_Address
            if blocked_device_Address:
                devstack_blocked_device_Address(result_dict, blocked_device_Address, current_step)
            powertriage(result_dict, current_step)
            return

        # .thread /p /r
        cmd = f".thread /p /r {blocked_thread_Address}"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

        # .frame /r nt!PopFxActivateDevice_frameNo
        frame_r_nt_PopFxActivateDevice_frameNo(result_dict, current_step)

        # dt _pop_fx_device {PopFxActivateDevice_address}
        dt_pop_fx_device_nt_PopFxActivateDevice_address(result_dict, current_step)

        blocked_device_Address = result_dict.get('blocked_device_Address', None)
        logger.info(f'blocked_device_Address: {blocked_device_Address}')
        # !devstack blocked_device_Address
        if blocked_device_Address:
            devstack_blocked_device_Address(result_dict, blocked_device_Address, current_step)

        # !irp blocked_IRP_Address
        blocked_IRP_Address = result_dict.get('blocked_IRP_Address', None)
        logger.info(f'blocked_IRP_Address: {blocked_IRP_Address}')
        if blocked_IRP_Address:
            blocked_device_Address = irp_blocked_IRP_Address(result_dict, blocked_IRP_Address, current_step)

        powertriage(result_dict, current_step)
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
