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

if __name__ == '__main__':
    src_dir = r'D:\0_LOG_VIP\5_Storage\5.1_Disk_0x7A_SurpriseRemoval'

    src_dir = r'E:\BSOD_Debug_SOP_0911\5. Storage\5.2 Disk_0xEF_Retried Failed Request 4'
    src_dir = r'E:\BSOD_Debug_SOP_0911\5. Storage\5.1 Disk_0x7A_SurpriseRemoval'
    src_dir = r'E:\BSOD_Debug_SOP_0911\5. Storage\5.3 SW Hung 0xEF Locks NTFS Disk Retried Failed Request'

    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    # tool_log_file = os.path.join(src_dir, 'hello.log')

    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')
    try:
        analyze_v_run(result_dict, current_step)

        storage_run(result_dict, current_step)

        
    finally:
        windbg.stop(path_dir)

    step_dict = {}
    
    dump_result_yaml(total_dict, debug_data_dict, path_dir)
    pass