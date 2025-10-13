import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


src_dir = r'E:\BSOD_Debug_SOP_0911\14. Locks_0xe2\14.3 开发样本_SW Hung 0xEF Locks NTFS Disk Retried Failed Request'

if __name__ == '__main__':
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')
    try:
        analyze_v_run(result_dict, current_step)

        BUGCHECK_CODE = result_dict['BUGCHECK_CODE']
        BUGCHECK_P1 = result_dict['BUGCHECK_P1']

        logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
        logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')

        if BUGCHECK_CODE == 'e2':
            locks_run(result_dict, current_step)

        

    finally:
        windbg.stop(path_dir)

    step_dict = {}
    
    dump_result_yaml(total_dict, debug_data_dict, path_dir)
    pass