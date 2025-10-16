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

if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\7. ACPI\7.2 DPC 0x133 1 ACPI\开发样本_DPC 0x133 1 ACPI'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    step_dict = {}
    Automatic_dict = {}
    total_dict = {}
    debug_data_dict = {}
    debug_data_dict_str = ''

    # 1. Automatic
    logger.info(f'1.Automatic')
    analyze_v_run(Automatic_dict, current_step=1)
    total_dict['Automatic Analysis'] = Automatic_dict

    step_dict_str = update_Automatic_dict_str(Automatic_dict)
    debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

    BUGCHECK_CODE = Automatic_dict['BUGCHECK_CODE']
    BUGCHECK_P1 = Automatic_dict['BUGCHECK_P1']
    MODULE_NAME = Automatic_dict['MODULE_NAME']

    logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
    logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')

    BSOD_Suspicious_Driver = Automatic_dict.get('BSOD_Suspicious_Driver', None)
    logger.info(f'BSOD_Suspicious_Driver: {BSOD_Suspicious_Driver}')
    # if BUGCHECK_CODE == '9f' and BSOD_Suspicious_Driver and BSOD_Suspicious_Driver == 'ACPI' or MODULE_NAME == 'ACPI':
    logger.info(f'7.ACPI')
    ACPI_run(step_dict, current_step=7)
    total_dict['ACPI'] = step_dict

    step_dict_str = update_ACPI_dict(step_dict)
    debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

    windbg.stop(path_dir)
    
    dump_result_yaml(total_dict, debug_data_dict_str, path_dir)
    pass