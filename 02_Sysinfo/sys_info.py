import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\2. Sysinfo\2.1 0x124_0_Machine Check Error'
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
        debug_data_str = ''
        sumarry_dict = {}

        debug_report_str = ''

        # default
        content_list = ['BSOD_Suspicious_Driver',
                        'BSOD_Suspicious_Device',
                        'CPU_Status_Abnormal',
                        'Memory_Status_Abnormal',
                        'Disk_Status_Abnormal',
                        'Current_Thread_Power_Status_Abnormal',
                        'Locked_Thread_Power_Status_Abnormal',
                        'ACPI_Status_Abnormal',
                        'NDIS_Status_Abnormal', ]
        for item in content_list:
            sumarry_dict[item] = ''

        # 1. Automatic
        logger.info(f'1.Automatic')
        analyze_v_run(Automatic_dict, current_step=1)
        total_dict['Automatic Analysis'] = Automatic_dict

        step_dict_str = update_Automatic_debug_data(Automatic_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'

        sumarry_dict['Memory_Status_Abnormal'] = Automatic_dict.get('Memory_Status_Abnormal', '')
        sumarry_dict['Disk_Status_Abnormal'] = Automatic_dict.get('Disk_Status_Abnormal', '')

        step_dict_str = update_Automatic_debug_report(Automatic_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'

        BUGCHECK_CODE = Automatic_dict.get('BUGCHECK_CODE', None)
        BUGCHECK_P1 = Automatic_dict.get('BUGCHECK_P1', None)
        BUGCHECK_P2 = Automatic_dict.get('BUGCHECK_P2', None)
        MODULE_NAME = Automatic_dict.get('MODULE_NAME', None)

        # logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
        # logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')
        # logger.info(f'MODULE_NAME: {MODULE_NAME}')

        # 2. Sysinfo
        logger.info(f'2.Sysinfo')
        system_info_run(step_dict, current_step=2)
        total_dict['Sysinfo'] = step_dict
        # logger.info(f'total_dict:{total_dict}')

        step_dict_str = update_Sysinfo_debug_data(step_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'

        step_dict_str = update_Sysinfo_debug_report(step_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'
    finally:
        windbg.stop(path_dir)

    step_dict_str = update_summary_report(sumarry_dict)
    debug_report_str = step_dict_str + '\n' + debug_report_str

    dump_result_yaml(total_dict, debug_data_str, path_dir, debug_report_str)
    pass