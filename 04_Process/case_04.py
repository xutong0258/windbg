import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    src_dir = r'E:\BSOD_Debug_SOP_0911\4. Process\4.1 SW Hung 0xEF Locks rtux64w10'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    # tool_log_file = os.path.join(src_dir, 'hello.log')

    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    try:
        analyze_v_run(result_dict, current_step)

        process_vm_run(result_dict, current_step)

        

    finally:
        windbg.stop(path_dir)

    step_dict = {}
    
    dump_result_yaml(total_dict, debug_data_dict, path_dir)
    pass