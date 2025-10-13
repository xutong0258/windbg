# coding=utf-8

import json
from base.common import *
from base import fileOP
from base.helper import *
from base.contants import *
from base.AdvancedWinDbgInterface import *
from base.cell_command import *

def dpc_run(result_dict, Automatic_dict, current_step):
    cmd = "!swd"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    update_context(cmd_output, result_dict, 'swd_DPCTimeout_Context')

    if cmd_output:
        cmd_output_list = cmd_output.splitlines()
        Bugcheck_P1 = Automatic_dict['BUGCHECK_P1']
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
    if swd_DPCTimeout_CPU:
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

def PnP_run(result_dict, current_step):
    # cmd = "!pnptriage"
    pnptriage(result_dict, current_step)

    blocked_IRP_Address = result_dict.get('blocked_IRP_Address', None)
    blocked_device_Address = None
    if blocked_IRP_Address:
        blocked_device_Address = irp_blocked_IRP_Address(result_dict, blocked_IRP_Address, current_step)

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

    blocked_IRP_Address_status = result_dict.get('blocked_IRP_Address_status', None)

    PnP_Status_Abnormal = 0
    if blocked_IRP_Address_status or Pending_Removal_Status:
        PnP_Status_Abnormal = 1

    result_dict['PnP_Status_Abnormal'] = PnP_Status_Abnormal
    return

def PnP_6_run(result_dict, current_step):
    cmd = "!pnptriage"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd = "!devnode 1"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    cmd_output_list = cmd_output.splitlines()
    count = get_list_text_count(cmd_output_list, 'Pending Removal')
    Pending_Removal_Status = 0
    if count:
        Pending_Removal_Status = 1
        result_dict['Pending_Removal_Context'] = cmd_output
    result_dict['pending_Removal_status'] = Pending_Removal_Status

    cmd = "!devnode 0 1"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    return

def storage_run(result_dict, current_step):
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
    if Storclass_FDO1_address:
        cmd = f"!storagekd.storclass {Storclass_FDO1_address} 2"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

        cmd_output_list = cmd_output.splitlines()
        parse_storagekd_storclass(cmd_output_list, result_dict)

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

    # !storadapter storadapter_adapter1_address
    storadapter_adapter1_address = result_dict.get('storadapter_adapter1_address', None)
    logger.info(f'storadapter_adapter1_address: {storadapter_adapter1_address}')
    if storadapter_adapter1_address:
        cmd = f"!storadapter {storadapter_adapter1_address}"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

        cmd_output_list = cmd_output.splitlines()
        parse_storadapter_storadapter_adapter1_address(cmd_output_list, result_dict)


    # !storadapter storadapter_adapter2_address
    storadapter_adapter2_address = result_dict.get('storadapter_adapter2_address', None)
    logger.info(f'storadapter_adapter2_address: {storadapter_adapter2_address}')
    if storadapter_adapter2_address:
        cmd = f"!storadapter {storadapter_adapter2_address}"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

        cmd_output_list = cmd_output.splitlines()
        parse_storadapter_storadapter_adapter2_address(cmd_output_list, result_dict)

    storadapter_storunit1_address = result_dict.get('storadapter_storunit1_address', None)
    logger.info(f'storadapter_storunit1_address: {storadapter_storunit1_address}')
    storadapter_storunit1_Outstanding_IRP_Status = 0

    if storadapter_storunit1_address:
        cmd = f"!storunit {storadapter_storunit1_address}"
        logger.info(f'cmd: {cmd}')
        cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
        result_dict['storadapter_storunit1_context'] = cmd_output

        cmd_output_list = cmd_output.splitlines()

        start_text = f'[Outstanding Requests]'
        end_text = '[Completed Requests]'
        result = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)

        first_index = get_list_text_line_first_index(cmd_output_list, 'ffff')

        # logger.info(f'first_index: {first_index}')
        if first_index:
            result_dict['storadapter_storunit1_Outstanding_IRP_Context'] = cmd_output_list[first_index: first_index + 6]
            storadapter_storunit1_Outstanding_IRP_Status = 1
        result_dict['storadapter_storunit1_Outstanding_IRP_Status'] = storadapter_storunit1_Outstanding_IRP_Status

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
        storadapter_storunit2_Outstanding_IRP_Status = 0
        # logger.info(f'first_index: {first_index}')
        if first_index:
            result_dict['storadapter_storunit2_Outstanding_IRP_Context'] = cmd_output_list[first_index: first_index + 6]
            storadapter_storunit2_Outstanding_IRP_Status = 1
        result_dict['storadapter_storunit2_Outstanding_IRP_Status'] = storadapter_storunit2_Outstanding_IRP_Status

    DISK_HARDWARE_ERROR_Status = result_dict.get('DISK_HARDWARE_ERROR_Status', None)
    storadapter_adapter1_SurpriseRemoval_Status = result_dict.get('storadapter_adapter1_SurpriseRemoval_Status', None)
    Storclass_FDO1_Failed_Requests_Status = result_dict.get('Storclass_FDO1_Failed_Requests_Status', None)

    check_point = False
    if DISK_HARDWARE_ERROR_Status and DISK_HARDWARE_ERROR_Status == 1:
        check_point = True
    if storadapter_adapter1_SurpriseRemoval_Status and storadapter_adapter1_SurpriseRemoval_Status == 1:
        check_point = True
    if Storclass_FDO1_Failed_Requests_Status and Storclass_FDO1_Failed_Requests_Status == 1:
        check_point = True
    if storadapter_storunit1_Outstanding_IRP_Status and storadapter_storunit1_Outstanding_IRP_Status == 1:
        check_point = True

    Disk_Status_Abnormal = 0
    if check_point:
        Disk_Status_Abnormal = 1
    result_dict['Disk_Status_Abnormal'] = Disk_Status_Abnormal
    return

def usb_run(result_dict, current_step):
    cmd = ".load usb3kd"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    # time.sleep(TIME_OUT)

    cmd = "!usb_tree"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    # time.sleep(TIME_OUT)

    update_context(cmd_output, result_dict, 'usb_tree_Context')
    return

def ndis_run(result_dict, current_step):
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

def ndis_run_power_4(result_dict, current_step):
    cmd = ".load ndiskd"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    cmd = "!ndiskd.oid"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)

    blocked_device_DevExta_address = result_dict.get('blocked_device_DevExta_address', None)

    cmd = f"!ndiskd.netadapter {blocked_device_DevExta_address}"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    return

def locks_run(result_dict, current_step):
    # !Locks
    blocked_thread_Address = locks(result_dict, current_step)
    logger.info(f'blocked_thread_Address: {blocked_thread_Address}')

    # !thread blocked_thread_Address
    blocked_IRP_Address = thread_blocked_thread_Address(result_dict, blocked_thread_Address, current_step)

    logger.info(f'blocked_IRP_Address: {blocked_IRP_Address}')

    blocked_device_Address = None
    blocked_IRP_Address_status = 0
    if blocked_IRP_Address:
        blocked_IRP_Address_status = 1
        # !irp blocked_IRP_Address
        blocked_device_Address = irp_blocked_IRP_Address(result_dict, blocked_IRP_Address, current_step)

        logger.info(f'blocked_device_Address: {blocked_device_Address}')

    result_dict['blocked_IRP_Address_status'] = blocked_IRP_Address_status

    # !devstack blocked_device_Address
    if blocked_device_Address:
        devstack_blocked_device_Address(result_dict, blocked_device_Address, current_step)

        blocked_IRP_driver = result_dict['blocked_IRP_driver']

    # !powertriage
    powertriage(result_dict, current_step)

    locks_thread_Status_Abnormal = 0

    PopFxActivateDevice_Status = result_dict.get('nt!PopFxActivateDevice_Status', None)
    if blocked_IRP_Address_status or PopFxActivateDevice_Status:
        locks_thread_Status_Abnormal = 1
    result_dict['locks_thread_Status_Abnormal'] = locks_thread_Status_Abnormal
    return
def process_vm_run(result_dict, current_step):
    cmd = "!VM"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    # time.sleep(15)

    result_dict['VM_Context'] = cmd_output

    return

def thread_run(result_dict, current_step):
    cmd = "!thread"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    # # time.sleep(15)
    result_dict['thread_Context'] = cmd_output

    cmd = "!running -it"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    # # time.sleep(15)

    result_dict['running_Context'] = cmd_output

    return

# Wait test case
def Current_Thread_run(result_dict, current_step):
    cmd = "!thread"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    # # time.sleep(15)
    result_dict['thread_Context'] = cmd_output
    return

def system_info_run(result_dict, current_step):
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

def WHEA_0x124_run(result_dict, current_step):
    WHEA_ERROR_RECORD_Address = result_dict['BUGCHECK_P2']

    # errrec WHEA_ERROR_RECORD_Address
    cmd = f"!errrec {WHEA_ERROR_RECORD_Address}"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    # logger.info(f'errrec cmd_output: {cmd_output}')

    result_dict['WHEA_ERROR_RECORD_Context'] = cmd_output

    cmd_output_list = cmd_output.splitlines()

    WHEA_ERROR_RECORD_Type = get_list_text_line(cmd_output_list, 'Notify Type')
    if WHEA_ERROR_RECORD_Type:
        WHEA_ERROR_RECORD_Type = WHEA_ERROR_RECORD_Type.replace('Notify Type', '').strip()
        WHEA_ERROR_RECORD_Type = WHEA_ERROR_RECORD_Type.replace(':', '').strip()
        logger.info(f'WHEA_ERROR_RECORD_Type: {WHEA_ERROR_RECORD_Type}')
        result_dict['WHEA_ERROR_RECORD_Type'] = WHEA_ERROR_RECORD_Type
        result_dict['BSOD_Supcious_Device'] = WHEA_ERROR_RECORD_Type

    # !WHEA
    cmd = f"!WHEA"
    logger.info(f'cmd: {cmd}')
    cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
    # logger.info(f'WHEA cmd_output: {cmd_output}')

    result_dict['WHEA_Context'] = cmd_output
    return

def Power_0x9f_3_run(result_dict, Automatic_dict, current_step):
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

def Power_0x9f_4_run(result_dict, Automatic_dict, current_step):
    result_dict['The_Power_Management_Status_Abnormal'] = 1

    Bugcheck_P3 = Automatic_dict['BUGCHECK_P3']
    blocked_thread_Address = Bugcheck_P3
    result_dict['blocked_thread_Address'] = blocked_thread_Address

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

def ACPI_run(result_dict, current_step):
    # ACPI
    amli_lc_ACPI_Method_Address(result_dict, current_step)

    ACPI_Method_Status = result_dict['ACPI_Method_Status']

    ACPI_Status_Abnormal = 0
    if ACPI_Method_Status == 1:
        amli_r_ACPI_Method_Address(result_dict, current_step)
        ACPI_Status_Abnormal = 1
    result_dict['ACPI_Status_Abnormal'] = ACPI_Status_Abnormal
    return


if __name__ == '__main__':
    pass
