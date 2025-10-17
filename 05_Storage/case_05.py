import os
from base import fileOP
from base.common import *
from base.componet import *
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    src_dir = r'G:\BSOD_Debug_SOP_0911\5. Storage\5.1 Disk_0x7A_SurpriseRemoval'

    dump_file = os.path.join(src_dir, 'MEMORY.DMP')
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

        # 3. Current Thread
        step_dict = {}
        logger.info(f'3.Current Thread')
        current_thread_run(step_dict, current_step=3)
        total_dict['Current Thread'] = step_dict

        # 4. Process
        step_dict = {}
        logger.info(f'4.Process')
        process_vm_run(step_dict, current_step=4)
        total_dict['Process'] = step_dict

        # 5. Storage
        step_dict = {}
        logger.info(f'5.Storage')
        storage_run(step_dict, Automatic_dict, current_step=5)
        total_dict['Storage'] = step_dict

        step_dict_str = update_Storage_debug_data(step_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'

        step_dict_str = update_Storage_debug_report(step_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'

        # 6. PnP
        step_dict = {}
        logger.info(f'6.PnP')
        PnP_run(step_dict, current_step=6)
        total_dict['PnP'] = step_dict

        step_dict_str = update_PnP_debug_data(step_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'

        # 7. ACPI
        step_dict = {}
        # BSOD_Suspicious_Driver = Automatic_dict.get('BSOD_Suspicious_Driver', None)
        # logger.info(f'BSOD_Suspicious_Driver: {BSOD_Suspicious_Driver}')
        # if BUGCHECK_CODE == '9f' and BSOD_Suspicious_Driver and BSOD_Suspicious_Driver == 'ACPI' or MODULE_NAME == 'ACPI':
        logger.info(f'7.ACPI')
        ACPI_run(step_dict, current_step=7)
        total_dict['ACPI'] = step_dict

        step_dict_str = update_ACPI_debug_data(step_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'
        sumarry_dict['ACPI_Status_Abnormal'] = step_dict.get('ACPI_Status_Abnormal', '')

        step_dict_str = update_ACPI_debug_report(step_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'

        # 8. NDIS
        step_dict = {}
        # BSOD_Suspicious_Driver = result_dict.get('BSOD_Suspicious_Driver', None)
        # if BSOD_Suspicious_Driver == 'NDIS Driver':
        logger.info(f'8.NDIS')
        ndis_run(step_dict, current_step=8)
        total_dict['NDIS'] = step_dict

        step_dict_str = update_NDIS_debug_data(step_dict)
        debug_data_str = debug_data_str + step_dict_str + '\n'
        sumarry_dict['NDIS_Status_Abnormal'] = step_dict.get('NDIS_Status_Abnormal', '')

        step_dict_str = update_NDIS_debug_report(step_dict)
        debug_report_str = debug_report_str + step_dict_str + '\n'

        # 9. USB
        step_dict = {}
        # BSOD_Suspicious_Device = result_dict.get('BSOD_Suspicious_Device', None)
        # if BSOD_Suspicious_Device == 'USB':
        logger.info(f'9.USB')
        usb_run(step_dict, current_step=9)
        total_dict['USB'] = step_dict

        # 10. WHEA_0x124
        if BUGCHECK_CODE == '124':
            step_dict = {}
            logger.info(f'10.WHEA_0x124')
            WHEA_0x124_run(step_dict, BUGCHECK_P2, current_step=10)
            total_dict['WHEA_0x124'] = step_dict

            step_dict_str = update_WHEA_0x124_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'

            step_dict_str = update_WHEA_0x124_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 11. Power_0x9f_3
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '3':
            step_dict = {}
            logger.info(f'11.Power_0x9f_3')
            Power_0x9f_3_run(step_dict, Automatic_dict, current_step=11)
            total_dict['Power_0x9f_3'] = step_dict

            step_dict_str = update_Power_0x9f_3_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'
            sumarry_dict['BSOD_Suspicious_Driver'] = step_dict.get('BSOD_Suspicious_Driver', '')
            sumarry_dict['BSOD_Suspicious_Device'] = step_dict.get('BSOD_Suspicious_Device', '')

            step_dict_str = update_Power_0x9f_3_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 12. Power_0x9f_4
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '4':
            step_dict = {}
            logger.info(f'12.Power_0x9f_4')
            Power_0x9f_4_run(step_dict, Automatic_dict, current_step=12)
            total_dict['Power_0x9f_3'] = step_dict

            step_dict_str = update_Power_0x9f_4_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'
            sumarry_dict['BSOD_Suspicious_Driver'] = step_dict.get('BSOD_Suspicious_Driver', '')
            sumarry_dict['BSOD_Suspicious_Device'] = step_dict.get('BSOD_Suspicious_Device', '')

            step_dict_str = update_Power_0x9f_4_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'

        # 13. DPC_0x133
        if BUGCHECK_CODE == '133':
            step_dict = {}
            step_dict['BSOD_Suspicious_Driver'] = MODULE_NAME
            logger.info(f'13.dpc')
            dpc_run(step_dict, Automatic_dict, current_step=13)

            total_dict['dpc'] = step_dict
            sumarry_dict['BSOD_Suspicious_Driver'] = step_dict.get('BSOD_Suspicious_Driver', '')
            sumarry_dict['BSOD_Suspicious_Device'] = step_dict.get('BSOD_Suspicious_Device', '')

        # 14. locks_0xE2
        if BUGCHECK_CODE == 'e2':
            step_dict = {}
            logger.info(f'14.locks_0xE2')
            locks_run(step_dict, current_step=14)
            total_dict['locks_0xE2'] = step_dict

            step_dict_str = update_locks_0xE2_debug_data(step_dict)
            debug_data_str = debug_data_str + step_dict_str + '\n'
            sumarry_dict['BSOD_Suspicious_Driver'] = step_dict['BSOD_Suspicious_Driver']

            step_dict_str = update_locks_0xE2_debug_report(step_dict)
            debug_report_str = debug_report_str + step_dict_str + '\n'
    finally:
        windbg.stop(path_dir)

    step_dict_str = update_summary_report(sumarry_dict)
    debug_report_str = step_dict_str + '\n' + debug_report_str

    dump_result_yaml(total_dict, debug_data_str, path_dir, debug_report_str)
    pass