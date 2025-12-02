import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class Power_0x9f_3:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        # Power_0x9f_3
        result_dict['The_Power_Management_Status_Abnormal'] = 1
        blocked_device_Address = Automatic_dict['BUGCHECK_P2']
        blocked_IRP_Address = Automatic_dict['BUGCHECK_P4']

        devstack_blocked_device_Address(result_dict, blocked_device_Address, current_step)

        # !irp blocked_IRP_Address
        blocked_device_Address = irp_blocked_IRP_Address(result_dict, blocked_IRP_Address, current_step)

        # !powertriage
        powertriage(result_dict, current_step)
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
