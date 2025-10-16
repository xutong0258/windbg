import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\5. Storage\5.1 Disk_0x7A_SurpriseRemoval'

    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    # tool_log_file = os.path.join(src_dir, 'hello.log')

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

        # 5. Storage
        step_dict = {}
        logger.info(f'5.Storage')
        storage_run(step_dict, Automatic_dict, current_step=5)
        total_dict['Storage'] = step_dict

        step_dict_str = update_Storage_dict_str(step_dict)
        debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'
    finally:
        windbg.stop(path_dir)
    
    dump_result_yaml(total_dict, debug_data_dict_str, path_dir)
    pass