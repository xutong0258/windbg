import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'D:\0_LOG_VIP\8_NDIS\8.1_0x133_Realtek_WLAN_NDIS_OID'
    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
    log_file = os.path.join(path_dir, 'tmp.log')
    result_dict = {}

    # start
    if not windbg.start(target=dump_file):
        assert ('FAIL')

    analyze_v_run(result_dict, current_step)

    BUGCHECK_CODE = result_dict['BUGCHECK_CODE']
    BUGCHECK_P1 = result_dict['BUGCHECK_P1']

    logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
    logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')

    if  BUGCHECK_CODE == '133':
        BSOD_Supcious_Driver = result_dict['MODULE_NAME']
        result_dict['BSOD_Supcious_Driver'] = BSOD_Supcious_Driver
        # dpc_run(result_dict, current_step)

    BSOD_Supcious_Driver = result_dict.get('BSOD_Supcious_Driver', None)
    logger.info(f'BSOD_Supcious_Driver: {BSOD_Supcious_Driver}')
    # if True or BSOD_Supcious_Driver == 'NDIS Driver':
    ndis_run(result_dict, current_step)

    

    windbg.stop(path_dir)

    step_dict = {}
    
    dump_result_yaml(total_dict, debug_data_dict, path_dir)
    pass