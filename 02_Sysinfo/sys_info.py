import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\2. Sysinfo\2.1 0x124_0_Machine Check Error'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    # tool_log_file = os.path.join(src_dir, 'hello.log')

    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    try:
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


        logger.info(f'2.Sysinfo')
        system_info_run(step_dict, current_step=2)
        total_dict['Sysinfo'] = step_dict

        step_dict_str = update_Sysinfo_dict_str(step_dict)
        debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'
        
    finally:
        windbg.stop(path_dir)

    dump_result_yaml(total_dict, debug_data_dict_str, path_dir)
    pass