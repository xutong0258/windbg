import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\14. Locks_0xe2\14.1 SW Hung 0xEF Locks rtux64w10'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    try:
        step_dict = {}
        Automatic_dict = {}
        total_dict = {}
        debug_data_dict_str = ''

        # 1. Automatic
        logger.info(f'1.Automatic')
        analyze_v_run(Automatic_dict, current_step=1)
        total_dict['Automatic Analysis'] = Automatic_dict

        step_dict_str = update_Automatic_dict_str(Automatic_dict)
        debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

        BUGCHECK_CODE = Automatic_dict.get('BUGCHECK_CODE', None)
        BUGCHECK_P1 = Automatic_dict.get('BUGCHECK_P1', None)
        BUGCHECK_P2 = Automatic_dict.get('BUGCHECK_P2', None)
        MODULE_NAME = Automatic_dict.get('MODULE_NAME', None)

        # 14. locks_0xE2
        if BUGCHECK_CODE == 'e2':
            step_dict = {}
            logger.info(f'14.locks_0xE2')
            locks_run(step_dict, current_step=14)
            total_dict['locks_0xE2'] = step_dict

            step_dict_str = update_locks_0xE2_dict(step_dict)
            debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'
    finally:
        windbg.stop(path_dir)

    dump_result_yaml(total_dict, debug_data_dict_str, path_dir)