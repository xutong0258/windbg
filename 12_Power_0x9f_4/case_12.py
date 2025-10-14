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

        # 12. Power_0x9f_4
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '4':
            step_dict = {}
            logger.info(f'12.Power_0x9f_4')
            Power_0x9f_4_run(step_dict, Automatic_dict, current_step=12)
            total_dict['Power_0x9f_3'] = step_dict

            step_dict_str = update_Power_0x9f_4_dict(step_dict)
            debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'
    finally:
        windbg.stop(path_dir)

    dump_result_yaml(total_dict, debug_data_dict_str, path_dir)