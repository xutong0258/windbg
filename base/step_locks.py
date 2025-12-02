import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class Locks:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        # !Locks
        blocked_thread_Address = locks(result_dict, current_step)
        logger.info(f'blocked_thread_Address: {blocked_thread_Address}')
        clue_step.append(f'command: !Locks, get: blocked_thread_Address: {blocked_thread_Address}')

        # !thread blocked_thread_Address
        blocked_IRP_Address = thread_blocked_thread_Address(result_dict, blocked_thread_Address, current_step)
        logger.info(f'blocked_IRP_Address: {blocked_IRP_Address}')

        clue_step.append(f'command: !thread {blocked_thread_Address}, get: blocked_IRP_Address: {blocked_IRP_Address}')

        blocked_device_Address = None
        blocked_IRP_address_status = 0
        if blocked_IRP_Address:
            blocked_IRP_address_status = 1
            # !irp blocked_IRP_Address
            blocked_device_Address = irp_blocked_IRP_Address(result_dict, blocked_IRP_Address, current_step)
            logger.info(f'blocked_device_Address: {blocked_device_Address}')

            clue_step.append(
                f'command: !irp {blocked_IRP_Address}, get: blocked_device_Address: {blocked_device_Address}')

        result_dict['blocked_IRP_address_status'] = blocked_IRP_address_status

        # !devstack blocked_device_Address
        if blocked_device_Address:
            devstack_blocked_device_Address(result_dict, blocked_device_Address, current_step)

        # !powertriage
        powertriage(result_dict, current_step)

        locks_thread_Status_Abnormal = 0

        PopFxActivateDevice_Status = result_dict.get('nt!PopFxActivateDevice_Status', None)
        if blocked_IRP_address_status or PopFxActivateDevice_Status:
            locks_thread_Status_Abnormal = 1
        result_dict['locks_thread_Status_Abnormal'] = locks_thread_Status_Abnormal

        BSOD_Suspicious_Driver = result_dict.get('BSOD_Suspicious_Driver', None)
        clue_step.append(
            f'BSOD_Suspicious_Driver = blocked_IRP_Driver; BSOD_Suspicious_Driver = {BSOD_Suspicious_Driver}')
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
