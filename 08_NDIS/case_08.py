import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\8. NDIS\8.1 0x133 0 Realtek WLAN NDIS OID'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    log_file = os.path.join(path_dir, 'tmp.log')

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

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

    BUGCHECK_CODE = Automatic_dict['BUGCHECK_CODE']
    BUGCHECK_P1 = Automatic_dict['BUGCHECK_P1']

    logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
    logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')

    logger.info(f'8.NDIS')
    ndis_run(step_dict, current_step=8)
    total_dict['NDIS'] = step_dict

    step_dict_str = update_NDIS_dict(step_dict)
    debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

    windbg.stop(path_dir)

    step_dict = {}
    
    dump_result_yaml(total_dict, debug_data_dict_str, path_dir)
    pass