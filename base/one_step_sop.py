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

    step_dict = {}
    Automatic_dict = {}
    total_dict = {}
    debug_data_dict = {}
    try:
        # 1. Automatic
        logger.info(f'1.Automatic')
        analyze_v_run(Automatic_dict, current_step=1)
        total_dict['Automatic Analysis'] = Automatic_dict

        debug_dict = update_Automatic_dict(Automatic_dict)
        debug_data_dict['Automatic Analysis'] = debug_dict

        # 2. Sysinfo
        logger.info(f'2.Sysinfo')
        system_info_run(step_dict, current_step=2)
        total_dict['Sysinfo'] = step_dict
        # logger.info(f'total_dict:{total_dict}')

        Sysinfo_dict = update_Sysinfo_dict(step_dict)
        debug_data_dict['Sysinfo'] = Sysinfo_dict

        # 3. Current Thread
        step_dict = {}
        logger.info(f'3.Current Thread')
        Current_Thread_run(step_dict, current_step=3)
        total_dict['Current Thread'] = step_dict

        current_dict = update_current_thread_dict(step_dict)
        debug_data_dict['Current Thread'] = current_dict

        # 4. Process
        step_dict = {}
        logger.info(f'4.Process')
        process_vm_run(step_dict, current_step=4)
        total_dict['Process'] = step_dict

        # 5. Storage
        step_dict = {}
        logger.info(f'5.Storage')
        storage_run(step_dict, current_step=5)
        total_dict['Storage'] = step_dict

        Storage_dict = update_Storage_dict(step_dict)
        debug_data_dict['Storage'] = Storage_dict

        # 6. PnP
        step_dict = {}
        logger.info(f'6.PnP')
        PnP_run(step_dict, current_step=6)
        total_dict['PnP'] = step_dict

        PnP_dict = update_PnP_dict(step_dict)
        debug_data_dict['PnP'] = PnP_dict

        # 7. ACPI
        step_dict = {}
        BUGCHECK_CODE = Automatic_dict.get('BUGCHECK_CODE', None)
        BUGCHECK_P1 = Automatic_dict.get('BUGCHECK_P1', None)
        MODULE_NAME = Automatic_dict.get('MODULE_NAME', None)

        logger.info(f'BUGCHECK_CODE: {BUGCHECK_CODE}')
        logger.info(f'BUGCHECK_P1: {BUGCHECK_P1}')
        logger.info(f'MODULE_NAME: {MODULE_NAME}')

        # BSOD_Supcious_Driver = Automatic_dict.get('BSOD_Supcious_Driver', None)
        # logger.info(f'BSOD_Supcious_Driver: {BSOD_Supcious_Driver}')
        # if BUGCHECK_CODE == '9f' and BSOD_Supcious_Driver and BSOD_Supcious_Driver == 'ACPI' or MODULE_NAME == 'ACPI':
        logger.info(f'7.ACPI')
        ACPI_run(step_dict, current_step=7)
        total_dict['ACPI'] = step_dict

        ACPI_dict = update_ACPI_dict(step_dict)
        debug_data_dict['ACPI'] = ACPI_dict

        # 8. NDIS
        step_dict = {}
        # BSOD_Supcious_Driver = result_dict.get('BSOD_Supcious_Driver', None)
        # if BSOD_Supcious_Driver == 'NDIS Driver':
        logger.info(f'8.NDIS')
        ndis_run(step_dict, current_step=8)

        total_dict['NDIS'] = step_dict
        NDIS_dict = update_NDIS_dict(step_dict)
        debug_data_dict['NDIS'] = NDIS_dict

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
            WHEA_0x124_run(step_dict, current_step=10)

            total_dict['WHEA_0x124'] = step_dict
            WHEA_dict = update_WHEA_0x124_dict(step_dict)
            debug_data_dict['WHEA_0x124'] = WHEA_dict

        # 11. Power_0x9f_3
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '3':
            step_dict = {}
            logger.info(f'11.Power_0x9f_3')
            Power_0x9f_3_run(step_dict, current_step=11)

            total_dict['Power_0x9f_3'] = step_dict
            tmp_dict = update_Power_0x9f_3_dict(step_dict)
            debug_data_dict['Power_0x9f_3'] = tmp_dict

        # 12. Power_0x9f_4
        if BUGCHECK_CODE == '9f' and BUGCHECK_P1 == '4':
            step_dict = {}
            logger.info(f'12.Power_0x9f_4')
            Power_0x9f_4_run(step_dict, Automatic_dict, current_step=12)

            total_dict['Power_0x9f_3'] = step_dict
            tmp_dict = update_Power_0x9f_4_dict(step_dict)
            debug_data_dict['Power_0x9f_4'] = tmp_dict

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
            tmp_dict = update_locks_0xE2_dict(step_dict)
            debug_data_dict['locks_0xE2'] = tmp_dict

    finally:
        windbg.stop(path_dir)

    dump_result_yaml(total_dict, debug_data_dict, path_dir)
    return