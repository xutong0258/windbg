import json
from base.common import *
from base import fileOP
from base.helper import *
from base.componet import *
from base.AdvancedWinDbgInterface import *
from base.cell_command import *


def one_process_run(dump_file, path_dir):
    # start
    if not windbg.start(target=dump_file):
        return

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

        # logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
        # logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')
        # logger.info(f'MODULE_NAME: {MODULE_NAME}')

        # 2. Sysinfo
        logger.info(f'2.Sysinfo')
        system_info_run(step_dict, current_step=2)
        total_dict['Sysinfo'] = step_dict
        # logger.info(f'total_dict:{total_dict}')

        step_dict_str = update_Sysinfo_dict_str(step_dict)
        debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

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

        step_dict_str = update_Storage_dict_str(step_dict)
        debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

        # 6. PnP
        step_dict = {}
        logger.info(f'6.PnP')
        PnP_run(step_dict, current_step=6)
        total_dict['PnP'] = step_dict

        step_dict_str = update_PnP_dict_str(step_dict)
        debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

        # 7. ACPI
        step_dict = {}
        # BSOD_Supcious_Driver = Automatic_dict.get('BSOD_Supcious_Driver', None)
        # logger.info(f'BSOD_Supcious_Driver: {BSOD_Supcious_Driver}')
        # if BUGCHECK_CODE == '9f' and BSOD_Supcious_Driver and BSOD_Supcious_Driver == 'ACPI' or MODULE_NAME == 'ACPI':
        logger.info(f'7.ACPI')
        ACPI_run(step_dict, current_step=7)
        total_dict['ACPI'] = step_dict

        step_dict_str = update_ACPI_dict(step_dict)
        debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

        # 8. NDIS
        step_dict = {}
        # BSOD_Supcious_Driver = result_dict.get('BSOD_Supcious_Driver', None)
        # if BSOD_Supcious_Driver == 'NDIS Driver':
        logger.info(f'8.NDIS')
        ndis_run(step_dict, current_step=8)
        total_dict['NDIS'] = step_dict

        step_dict_str = update_NDIS_dict(step_dict)
        debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

        # 9. USB
        step_dict = {}
        # BSOD_Supcious_Device = result_dict.get('BSOD_Supcious_Device', None)
        # if BSOD_Supcious_Device == 'USB':
        logger.info(f'9.USB')
        usb_run(step_dict, current_step=9)
        total_dict['USB'] = step_dict


        # 10. WHEA_0x124
        if BUGCHECK_CODE == '124':
            step_dict = {}
            logger.info(f'10.WHEA_0x124')
            WHEA_0x124_run(step_dict, BUGCHECK_CODE, current_step=10)
            total_dict['WHEA_0x124'] = step_dict

            step_dict_str = update_WHEA_0x124_dict(step_dict)
            debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

        # 11. Power_0x9f_3
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '3':
            step_dict = {}
            logger.info(f'11.Power_0x9f_3')
            Power_0x9f_3_run(step_dict, Automatic_dict,current_step=11)
            total_dict['Power_0x9f_3'] = step_dict

            step_dict_str = update_Power_0x9f_3_dict(step_dict)
            debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

        # 12. Power_0x9f_4
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '4':
            step_dict = {}
            logger.info(f'12.Power_0x9f_4')
            Power_0x9f_4_run(step_dict, Automatic_dict, current_step=12)
            total_dict['Power_0x9f_3'] = step_dict

            step_dict_str = update_Power_0x9f_4_dict(step_dict)
            debug_data_dict_str = debug_data_dict_str + step_dict_str + '\n'

        # 13. DPC_0x133
        if BUGCHECK_CODE == '133':
            step_dict = {}
            step_dict['BSOD_Supcious_Driver'] = MODULE_NAME
            logger.info(f'13.dpc')
            dpc_run(step_dict, Automatic_dict, current_step=13)

            total_dict['dpc'] = step_dict

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
    return