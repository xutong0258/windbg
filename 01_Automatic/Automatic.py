import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\1. Automatic\1.2 0x1A_Call Stack MI'

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

        # 1. Automatic
        logger.info(f'1.Automatic')
        analyze_v_run(Automatic_dict, current_step=1)
        total_dict['Automatic Analysis'] = Automatic_dict

        debug_data_dict_str = update_Automatic_dict_str(Automatic_dict)


    finally:
        windbg.stop(path_dir)
    
    dump_result_yaml(total_dict, debug_data_dict_str, path_dir)

    pass