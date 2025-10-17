import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\1. Automatic\1.2 0x1A_Call Stack MI'

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

        #default
        content_list = ['BSOD_Suspicious_Driver',
                        'BSOD_Suspicious_Device',
                        'CPU_Status_Abnormal',
                        'Memory_Status_Abnormal',
                        'Disk_Status_Abnormal',
                        'Current_Thread_Power_Status_Abnormal',
                        'Locked_Thread_Power_Status_Abnormal',
                        'ACPI_Status_Abnormal',
                        'NDIS_Status_Abnormal',]
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

    finally:
        windbg.stop(path_dir)

    step_dict_str = update_summary_report(sumarry_dict)
    debug_report_str = step_dict_str + '\n' + debug_report_str

    dump_result_yaml(total_dict, debug_data_str, path_dir, debug_report_str)

    pass