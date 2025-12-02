import os
import sys

from base.AdvancedWinDbgInterface import windbg
from utils.logger_util import logger
from base.common import *


class Storage:
    def __init__(self):
        return

    def run(self, result_dict, Automatic_dict, clue_step, current_step):
        BUGCHECK_CODE = Automatic_dict.get('BUGCHECK_CODE', None)
        BUGCHECK_CODE = BUGCHECK_CODE.upper()

        cmd = ".load storagekd "
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        # time.sleep(TIME_OUT)

        cmd = "!storclass"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        # time.sleep(5)

        cmd_output_list = cmd_output.splitlines()
        parse_storclass(cmd_output_list, result_dict)

        Storclass_FDO1_address = result_dict.get('Storclass_FDO1_address', None)
        clue_step.append(f'command: !storclass, get: Storclass_FDO1_address:{Storclass_FDO1_address}')

        if Storclass_FDO1_address:
            cmd = f"!storagekd.storclass {Storclass_FDO1_address} 2"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

            cmd_output_list = cmd_output.splitlines()
            parse_storagekd_storclass(cmd_output_list, result_dict)

            clue_step.append(
                f'command: !storagekd.storclass {Storclass_FDO1_address} 2, get: Storclass_FDO1_Failed_Requests_Status')

        result_dict['Storclass_FDO2_Failed_Requests_Status'] = 0
        # todo Storclass_FDO2_address test case

        # storadapter
        cmd = "!storadapter"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        cmd_output_list = cmd_output.splitlines()

        for idx, line in enumerate(cmd_output_list):
            # logger.info(f'line: {line}')
            if 'Driver' in line and 'Object' in line:
                # logger.info(f'line: {line}')
                parse_storadapter_driver_and_address(cmd_output_list[idx + 2: idx + 4], result_dict)

        clue_step.append(
            f'command: !storadapter, get: storadapter_adapter1_address')

        # !storadapter storadapter_adapter1_address
        storadapter_adapter1_address = result_dict.get('storadapter_adapter1_address', None)
        logger.info(f'storadapter_adapter1_address: {storadapter_adapter1_address}')
        if storadapter_adapter1_address:
            cmd = f"!storadapter {storadapter_adapter1_address}"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

            cmd_output_list = cmd_output.splitlines()
            parse_storadapter_storadapter_adapter1_address(cmd_output_list, result_dict)

            clue_step.append(
                f'command: !storadapter {storadapter_adapter1_address}, get: storadapter_adapter1_SurpriseRemoval_Status')

        # !storadapter storadapter_adapter2_address
        result_dict['storadapter_adapter2_SurpriseRemoval_Status'] = 0
        storadapter_adapter2_address = result_dict.get('storadapter_adapter2_address', None)
        logger.info(f'storadapter_adapter2_address: {storadapter_adapter2_address}')
        if storadapter_adapter2_address:
            cmd = f"!storadapter {storadapter_adapter2_address}"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

            cmd_output_list = cmd_output.splitlines()
            parse_storadapter_storadapter_adapter2_address(cmd_output_list, result_dict)

            clue_step.append(
                f'command: !storadapter {storadapter_adapter2_address}, get: storadapter_adapter2_SurpriseRemoval_Status')

        storadapter_storunit1_address = result_dict.get('storadapter_storunit1_address', None)
        logger.info(f'storadapter_storunit1_address: {storadapter_storunit1_address}')
        storadapter_storunit1_Outstanding_IRP_Status = 0
        storadapter_storunit2_Outstanding_IRP_Status = 0

        if storadapter_storunit1_address:
            cmd = f"!storunit {storadapter_storunit1_address}"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
            result_dict['storadapter_storunit1_context'] = cmd_output

            cmd_output_list = cmd_output.splitlines()

            start_text = f'[Outstanding Requests]'
            end_text = '[Completed Requests]'
            result = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)

            # logger.info(f'result: {result}')

            first_index = get_list_text_line_first_index(result, 'ffff')

            # logger.info(f'first_index: {first_index}')
            if first_index:
                result_dict['storadapter_storunit1_Outstanding_IRP_Context'] = cmd_output_list[
                    first_index: first_index + 6]
                storadapter_storunit1_Outstanding_IRP_Status = 1

            clue_step.append(
                f'command: !storunit {storadapter_storunit1_address}, get: storadapter_storunit1_Outstanding_IRP_Context')

        result_dict['storadapter_storunit1_Outstanding_IRP_Status'] = storadapter_storunit1_Outstanding_IRP_Status
        logger.info(f'storadapter_storunit1_Outstanding_IRP_Status: {storadapter_storunit1_Outstanding_IRP_Status}')

        storadapter_storunit2_address = result_dict.get('storadapter_storunit2_address', None)
        logger.info(f'storadapter_storunit2_address: {storadapter_storunit2_address}')
        if storadapter_storunit2_address:
            cmd = f"!storunit {storadapter_storunit2_address}"
            logger.info(f'cmd: {cmd}')
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
            result_dict['storadapter_storunit2_context'] = cmd_output

            cmd_output_list = cmd_output.splitlines()

            start_text = f'[Outstanding Requests]'
            end_text = '[Completed Requests]'
            result = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)

            first_index = get_list_text_line_first_index(cmd_output_list, 'ffff')

            # logger.info(f'first_index: {first_index}')
            if first_index:
                result_dict['storadapter_storunit2_Outstanding_IRP_Context'] = cmd_output_list[
                    first_index: first_index + 6]
                storadapter_storunit2_Outstanding_IRP_Status = 1

            clue_step.append(
                f'command: !storunit {storadapter_storunit2_address}, get: storadapter_storunit2_Outstanding_IRP_Context')

        result_dict['storadapter_storunit2_Outstanding_IRP_Status'] = storadapter_storunit2_Outstanding_IRP_Status

        storadapter_adapter1_SurpriseRemoval_Status = result_dict.get('storadapter_adapter1_SurpriseRemoval_Status', 0)
        Storclass_FDO1_Failed_Requests_Status = result_dict.get('Storclass_FDO1_Failed_Requests_Status', 0)

        storadapter_adapter2_SurpriseRemoval_Status = result_dict.get('storadapter_adapter2_SurpriseRemoval_Status', 0)
        Storclass_FDO2_Failed_Requests_Status = result_dict.get('Storclass_FDO2_Failed_Requests_Status', 0)

        Disk1_Status_Abnormal = 0
        if storadapter_adapter1_SurpriseRemoval_Status == 1 or Storclass_FDO1_Failed_Requests_Status == 1 or storadapter_storunit1_Outstanding_IRP_Status == 1:
            Disk1_Status_Abnormal = 1
        result_dict['Disk1_Status_Abnormal'] = Disk1_Status_Abnormal
        logger.info(f'Disk1_Status_Abnormal:{Disk1_Status_Abnormal}')

        Disk2_Status_Abnormal = 0
        if storadapter_adapter2_SurpriseRemoval_Status == 1 or Storclass_FDO2_Failed_Requests_Status == 1 or storadapter_storunit2_Outstanding_IRP_Status == 1:
            Disk2_Status_Abnormal = 1
        result_dict['Disk2_Status_Abnormal'] = Disk2_Status_Abnormal
        logger.info(f'Disk2_Status_Abnormal:{Disk2_Status_Abnormal}')

        BSOD_Suspicious_Device = ''
        logger.info(f'BUGCHECK_CODE:{BUGCHECK_CODE}')
        if BUGCHECK_CODE == '7A' or BUGCHECK_CODE == 'EF' or BUGCHECK_CODE == '154' or BUGCHECK_CODE == '24' or BUGCHECK_CODE == 'E2':
            if Disk1_Status_Abnormal == 1:
                Storclass_FDO1_DeviceID = result_dict.get('Storclass_FDO1_DeviceID', None)
                BSOD_Suspicious_Device = Storclass_FDO1_DeviceID
            if Disk2_Status_Abnormal == 1:
                Storclass_FDO2_DeviceID = result_dict.get('Storclass_FDO2_DeviceID', None)
                BSOD_Suspicious_Device = Storclass_FDO2_DeviceID
        result_dict['BSOD_Suspicious_Device'] = BSOD_Suspicious_Device
        logger.info(f'BSOD_Suspicious_Device:{BSOD_Suspicious_Device}')
        return


# =========================
# 3. 示例调用
# =========================
if __name__ == "__main__":
    pass
