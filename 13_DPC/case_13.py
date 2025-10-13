import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\13. DPC 0x133\13.1 0x133 0 Disk IO'

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


    BUGCHECK_CODE = Automatic_dict['BUGCHECK_CODE']
    BUGCHECK_P1 = Automatic_dict['BUGCHECK_P1']

    logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
    logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')
    MODULE_NAME = Automatic_dict['MODULE_NAME']
    if BUGCHECK_CODE == '133':
        step_dict = {}
        step_dict['BSOD_Supcious_Driver'] = MODULE_NAME
        logger.info(f'13.dpc')
        dpc_run(step_dict, Automatic_dict, current_step=13)

        total_dict['dpc'] = step_dict

    windbg.stop(path_dir)

    dump_result_yaml(total_dict, debug_data_dict, path_dir)
    pass