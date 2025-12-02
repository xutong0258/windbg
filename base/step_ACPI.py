import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *
from base.cell_command import *


class ACPI:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        # ACPI
        amli_lc_ACPI_Method_Address(result_dict, current_step)

        ACPI_Method_Status = result_dict['ACPI_Method_Status']

        ACPI_Status_Abnormal = 0
        if ACPI_Method_Status == 1:
            amli_r_ACPI_Method_Address(result_dict, current_step)
            ACPI_Status_Abnormal = 1
        result_dict['ACPI_Status_Abnormal'] = ACPI_Status_Abnormal
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
