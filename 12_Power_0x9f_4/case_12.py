import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\12. Power_0x9f_4\12.1 0x9f_4_IRP\开发样本_0x9f_4_IRP_Intel WLAN'
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

    # 12. Power_0x9f_4
    if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '4':
        step_dict = {}
        logger.info(f'12.Power_0x9f_4')
        Power_0x9f_4_run(step_dict, Automatic_dict, current_step=12)

        total_dict['Power_0x9f_3'] = step_dict
        tmp_dict = update_Power_0x9f_4_dict(step_dict)
        debug_data_dict['Power_0x9f_4'] = tmp_dict

    windbg.stop(path_dir)

    step_dict = {}

    dump_result_yaml(total_dict, debug_data_dict, path_dir)
    pass