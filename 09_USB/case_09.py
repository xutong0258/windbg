import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)

# OK
src_dir = r'D:\0_LOG_VIP\1_Automatic\1.1_0x3b_Context_Memory_Corruption'
src_dir = r'D:\0_LOG_VIP\2_Sysinfo\2.1_0x124_0_Machine_Check_Error'
src_dir = r'D:\0_LOG_VIP\4_Process\4.1_SW Hung_0xEF_Locks_rtux64w10'
src_dir = r'D:\0_LOG_VIP\5_Storage\5.1_Disk_0x7A_SurpriseRemoval'
src_dir = r'D:\0_LOG_VIP\6_PnP\6.1_SW_Hung_0xEF_Locks_NTFS_Disk_Retried_Failed_Request'
src_dir = r'D:\0_LOG_VIP\7_ACPI\7.1_0x9f_3_ACPI\1_0x9f_3_ACPI_cdrom'
# Wait confirm
src_dir = r'D:\0_LOG_VIP\8_NDIS\8.1_0x133_Realtek_WLAN_NDIS_OID'

if __name__ == '__main__':
    src_dir = r'D:\0_LOG_VIP\9_USB\9.1_0x9f_3_USB\0x9f_3_USB_usbccgp_Disk_IO_Exception'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    analyze_v_run(result_dict, current_step)

    BUGCHECK_CODE = result_dict['BUGCHECK_CODE']
    BUGCHECK_P1 = result_dict['BUGCHECK_P1']

    logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
    logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')

    if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '3':
        Power_0x9f_3_run(result_dict, current_step)
        pass

    BSOD_Supcious_Device = result_dict.get('BSOD_Supcious_Device', None)

    # if 'USB' in BSOD_Supcious_Device:
    usb_run(result_dict, current_step)

    

    windbg.stop(path_dir)

    step_dict = {}
    
    dump_result_yaml(total_dict, debug_data_dict, path_dir)
    pass