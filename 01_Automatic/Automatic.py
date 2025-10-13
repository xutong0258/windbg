import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\1. Automatic\1.1 0x3b_Context Memory Corruption'

    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    # tool_log_file = os.path.join(src_dir, 'hello.log')

    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}


    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    try:
        analyze_v_run(result_dict, current_step)

        # 
    finally:
        windbg.stop(path_dir)

    step_dict = {}
    
    dump_result_yaml(result_dict,debug_data_dict, path_dir)

    pass