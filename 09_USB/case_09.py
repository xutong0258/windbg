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
    src_dir = r'G:\BSOD_Debug_SOP_0911\1. Automatic\1.2 0x1A_Call Stack MI'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    step_dict = {}
    Automatic_dict = {}
    total_dict = {}
    debug_data_dict = {}

    # 1. Automatic
    logger.info(f'1.Automatic')
    analyze_v_run(Automatic_dict, current_step=1)
    total_dict['Automatic Analysis'] = Automatic_dict

    debug_dict = update_Automatic_dict(Automatic_dict)
    debug_data_dict['Automatic Analysis'] = debug_dict

    # 9. USB
    step_dict = {}
    # BSOD_Suspicious_Device = result_dict.get('BSOD_Suspicious_Device', None)
    # if BSOD_Suspicious_Device == 'USB':
    logger.info(f'9.USB')
    usb_run(step_dict, current_step=9)
    total_dict['USB'] = step_dict

    windbg.stop(path_dir)
    
    dump_result_yaml(total_dict, debug_data_dict_str, path_dir)
    pass