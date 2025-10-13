# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re

from base.helper import *
from base import fileOP
from base.contants import *

def update_Automatic_dict(result_dict):
    Automatic = {}
    content_list = ['BUGCHECK_CODE',
                    'BUGCHECK_P1',
                    'BUGCHECK_P2',
                    'BUGCHECK_P3',
                    'BUGCHECK_P4',
                    'FAILURE_BUCKET_ID',
                    'DISK_HARDWARE_ERROR_Status',
                    'MODULE_NAME',
                    'Context_Memory_Corruption_Status',
                    'Stack_Memory_Operation_Status',
                    'Disk_Status_Abnormal',
                    'Memory_Status_Abnormal',
                    ]
    for content in content_list:
        Automatic[content] = result_dict.get(content, '')
    return Automatic

def update_Sysinfo_dict(result_dict):
    Sysinfo_dict = {}
    Sysinfo_dict['OS_Version_ID'] = result_dict.get('OS_Version_ID')
    Sysinfo_dict['CPUID'] = result_dict.get('CPUID')
    return Sysinfo_dict

def update_current_thread_dict(result_dict):
    current_dict = {}
    # current_dict['OS_Version_ID'] = result_dict.get('OS_Version_ID')
    return current_dict

def update_Storage_dict(result_dict):
    Storage_dict = {}
    content_list = ['Storclass_FDO1_DeviceID',
                    'Storclass_FDO2_DeviceID',
                    'Storclass_FDO1_Failed_Requests_Status',
                    'Storclass_FDO2_Failed_Requests_Status',
                    'storadapter_adapter1_SurpriseRemoval_Status',
                    'storadapter_adapter2_SurpriseRemoval_Status',
                    'storadapter_storunit1_Outstanding_IRP_Status',
                    'storadapter_storunit2_Outstanding_IRP_Status',
                    'Disk_Status_Abnormal',
                    ]
    for content in content_list:
        Storage_dict[content] = result_dict.get(content, '')
    return Storage_dict

def update_PnP_dict(result_dict):
    PnP_dict = {}
    content_list = ['blocked_IRP_Address_status',
                    'pending_Removal_status',
                    'PnP_Status_Abnormal']
    for content in content_list:
        PnP_dict[content] = result_dict.get(content, '')
    return PnP_dict

def update_ACPI_dict(result_dict):
    ACPI_dict = {}
    content_list = ['ACPI_Method_Object',
                    'ACPI_Method_Status',
                    'ACPI_Method_AMLPointer']
    for content in content_list:
        ACPI_dict[content] = result_dict.get(content, '')
    return ACPI_dict

def update_NDIS_dict(result_dict):
    NDIS_dict = {}
    content_list = ['NDIS_OID_Pending_Status',
                    'Ndis_netadapter1_name',
                    'Ndis_netadapter2_name',
                    'NDIS_Status_Abnormal',]
    for content in content_list:
        NDIS_dict[content] = result_dict.get(content, '')
    return NDIS_dict

def update_WHEA_0x124_dict(result_dict):
    WHEA_dict = {}
    content_list = ['WHEA_ERROR_RECORD_Type',
                    'BSOD_Supcious_Device',
                    'WHEA_Status_Abnormal',
                    ]
    for content in content_list:
        WHEA_dict[content] = result_dict.get(content, '')
    return WHEA_dict

def update_Power_0x9f_3_dict(result_dict):
    tmp_dict = {}
    content_list = ['blocked_device_ServiceName',
                    'blocked_device_DeviceInst',
                    'blocked_irp_Driver',
                    'System_State_Context',
                    'Device_State_Context'
                    'BSOD_Supcious_Driver',
                    'BSOD_Supcious_Device',
                    'The_Power_Management_Status_Abnormal'
                    ]
    for content in content_list:
        tmp_dict[content] = result_dict.get(content, '')
    return tmp_dict

def update_Power_0x9f_4_dict(result_dict):
    tmp_dict = {}
    content_list = ['blocked_IRP_Address_status',
                    'nt!PopFxActivateDevice_Status',
                    'blocked_irp_Driver',
                    'blocked_device_ServiceName',
                    'blocked_device_DeviceInst'
                    'System_State_Context',
                    'Device_State_Context',
                    'BSOD_Supcious_Driver',
                    'BSOD_Supcious_Device',
                    'The_Power_Management_Status_Abnormal'
                    ]
    for content in content_list:
        tmp_dict[content] = result_dict.get(content, '')
    return tmp_dict

def update_locks_0xE2_dict(result_dict):
    tmp_dict = {}
    content_list = ['blocked_IRP_Address_status',
                    'locks_thread_Status_Abnormal',
                    'nt!PopFxActivateDevice_Status',
                    'blocked_irp_Driver',
                    'blocked_device_ServiceName'
                    'blocked_device_DeviceInst',
                    'System_State_Context',
                    'Device_State_Context',
                    'BSOD_Supcious_Driver',
                    'BSOD_Supcious_Device'
                    ]
    for content in content_list:
        tmp_dict[content] = result_dict.get(content, '')
    return tmp_dict

def update_final_dict(result_dict):
    debug_data_dict = {}
    Automatic = update_Automatic_dict(result_dict, current_step)
    debug_data_dict['Automatic Analysis'] = Automatic

    Sysinfo_dict = update_Sysinfo_dict(result_dict, current_step)
    debug_data_dict['Sysinfo'] = Sysinfo_dict

    current_dict = update_current_thread_dict(result_dict, current_step)
    debug_data_dict['Current Thread'] = current_dict

    Storage_dict = update_Storage_dict(result_dict, current_step)
    debug_data_dict['Storage'] = Storage_dict

    PnP_dict = update_PnP_dict(result_dict, current_step)
    debug_data_dict['PnP'] = PnP_dict

    ACPI_dict = update_ACPI_dict(result_dict, current_step)
    debug_data_dict['ACPI'] = ACPI_dict

    NDIS_dict = update_NDIS_dict(result_dict, current_step)
    debug_data_dict['NDIS'] = NDIS_dict

    WHEA_0x124_run = step_dict.get('WHEA_0x124_run', None)
    if WHEA_0x124_run:
        WHEA_dict = update_WHEA_0x124_dict(result_dict, current_step)
        debug_data_dict['WHEA_0x124'] = WHEA_dict

    Power_0x9f_3_run = step_dict.get('Power_0x9f_3_run', None)
    if Power_0x9f_3_run:
        tmp_dict = update_Power_0x9f_3_dict(result_dict, current_step)
        debug_data_dict['Power_0x9f_3'] = tmp_dict

    Power_0x9f_4_run = step_dict.get('Power_0x9f_4_run', None)
    if Power_0x9f_4_run:
        tmp_dict = update_Power_0x9f_4_dict(result_dict, current_step)
        debug_data_dict['Power_0x9f_4'] = tmp_dict

    locks_run = step_dict.get('locks_run', None)
    if locks_run:
        tmp_dict = update_locks_0xE2_dict(result_dict, current_step)
        debug_data_dict['locks_0xE2'] = tmp_dict

    return debug_data_dict

def dump_result_yaml(result_dict, BSOD_Debug_Data, dir_name):
    # last dump
    result_yaml_file = 'result.yaml'
    result_yaml_file = os.path.join(dir_name, result_yaml_file)
    fileOP.dump_file(result_yaml_file, result_dict)

    result_yaml_file = 'BSOD_Debug_Data.yaml'
    result_yaml_file = os.path.join(dir_name, result_yaml_file)
    fileOP.dump_file(result_yaml_file, BSOD_Debug_Data)

    # # command list
    # result_yaml_file = 'command_list.yaml'
    # result_yaml_file = os.path.join(dir_name, result_yaml_file)
    # fileOP.dump_file(result_yaml_file, command_his)
    #
    # # command
    # result_yaml_file = 'command_dict.yaml'
    # result_yaml_file = os.path.join(dir_name, result_yaml_file)
    # fileOP.dump_file(result_yaml_file, command_dict)
    return

def parse_blocked_IRP_Address(cmd_output_list, result_dict):
    blocked_device_Address = None
    # logger.info(f'cmd_output_list: {cmd_output_list}')
    if cmd_output_list:
        result_str = '\n' + '\n'.join(cmd_output_list)
        result_dict['blocked_irp_context'] = result_str

        index = get_stack_begin_index(cmd_output_list)
        if index is not None:
            # 偏移3行
            blocked_IRP_driver = cmd_output_list[index+2].strip()
            # logger.info(f'blocked_IRP_driver: {blocked_IRP_driver}')
            split_list = blocked_IRP_driver.split('\t')
            blocked_IRP_driver = split_list[0]
            # logger.info(f'blocked_IRP_driver: {blocked_IRP_driver}')
            last_index = get_list_text_line_last_index(blocked_IRP_driver, '\\')
            blocked_IRP_driver = blocked_IRP_driver[last_index+1:]
            logger.info(f'blocked_IRP_driver: {blocked_IRP_driver}')
            result_dict['blocked_IRP_driver'] = blocked_IRP_driver

            # 偏移2行
            blocked_device_Address = cmd_output_list[index+1].strip()
            logger.info(f'blocked_device_Address: {blocked_device_Address}')
            split_list = blocked_device_Address.split(' ')
            # logger.info(f'split_list: {split_list}')
            blocked_device_Address = get_address_by_list(split_list)

            logger.info(f'blocked_device_Address: {blocked_device_Address}')
            result_dict['blocked_device_Address'] = blocked_device_Address

    return blocked_device_Address

def get_blocked_IRP_Address_thread(cmd_output_list, result_dict):
    blocked_IRP_Address = None
    blocked_IRP_Address_status = 0
    if cmd_output_list:
        result_str = '\n' + '\n'.join(cmd_output_list)
        result_dict['Locks_thread_context'] = result_str

        for idx, line in enumerate(cmd_output_list):
            line = line.strip()
            if 'IRP List' in line:
                logger.info(f'IRP List: {cmd_output_list[idx + 1]}')
                blocked_IRP_Address = cmd_output_list[idx + 1].split(':')[0]
                logger.info(f'blocked_IRP_Address: {blocked_IRP_Address}')
                result_dict['blocked_IRP_Address'] = blocked_IRP_Address
                blocked_IRP_Address_status = 1

    result_dict['blocked_IRP_Address_status'] = blocked_IRP_Address_status

    return blocked_IRP_Address

def get_blocked_IRP_Address_pnp(cmd_output_list, result_dict):
    blocked_IRP_Address = None
    if cmd_output_list:
        result_str = '\n' + '\n'.join(cmd_output_list)
        result_dict['Locks_thread_context'] = result_str

        blocked_IRP_Address_status = 0
        for idx, line in enumerate(cmd_output_list):
            line = line.strip()
            if 'IRP List' in line:
                logger.info(f'IRP List: {cmd_output_list[idx + 1]}')
                blocked_IRP_Address = cmd_output_list[idx + 1].split(':')[0]
                logger.info(f'blocked_IRP_Address: {blocked_IRP_Address}')
                result_dict['blocked_IRP_Address'] = blocked_IRP_Address
                blocked_IRP_Address_status = 1

    result_dict['blocked_IRP_Address_status'] = blocked_IRP_Address_status

    return blocked_IRP_Address

def parse_locks_info(cmd_output_list, result_dict):
    new_result = get_list_strip(cmd_output_list)
    result_dict['Locks_Context'] = new_result

    # 执行解析
    # logger.info(f'file_content_new: {file_content_new}')
    thread_contention_pairs,Locks_thread_Address = fileOP.parse_locks_content(new_result)
    logger.info(f'thread_contention_pairs: {thread_contention_pairs}')
    Locks_thread_Address = Locks_thread_Address.replace('-01<*>', '').strip()
    logger.info(f'Locks_thread_Address: {Locks_thread_Address}')

    result_dict['Locks_thread_Address'] = Locks_thread_Address
    result_dict['blocked_thread_Address'] = Locks_thread_Address

    if Locks_thread_Address:
        result_dict['Locks_thread_Status'] = 1
    else:
        result_dict['Locks_thread_Status'] = 0

    return Locks_thread_Address


def parse_vertarget(cmd_output, result_dict):
    result_dict['vertarget_Context'] = cmd_output

    cmd_output_list = cmd_output.splitlines()
    OS_Version_ID = None
    if cmd_output_list:
        OS_Version_ID = get_list_text_line(cmd_output_list, 'Edition build lab')

        match = re.search(r'\d+\.\d+', OS_Version_ID)

        if match:
            OS_Version_ID = match.group()
            logger.info(f"OS_Version_ID：{OS_Version_ID}")  # 输出：9600.17238

        else:
            logger.info("未找到OS_Version_ID")

    if OS_Version_ID:
        result_dict['OS_Version_ID'] = float(OS_Version_ID)
    else:
        result_dict['OS_Version_ID'] = OS_Version_ID
    return

def parse_sysinfo_cpuspeed(cmd_output, result_dict):
    result_dict['cpuspeed_context'] = cmd_output

    cmd_output_list = cmd_output.splitlines()
    CPUID = None
    if cmd_output_list:
        CPUID = get_list_text_line(cmd_output_list, 'CPUID:')
        # logger.info(f'CPUID: {CPUID}')
        match = re.search(r'CPUID:(.*)', CPUID)
        if match:
            CPUID = match.group()
            # logger.info(f"CPUID：{CPUID}")
        else:
            logger.info("未找到数字部分")
        CPUID = CPUID.replace('CPUID:', '')
        CPUID = CPUID.replace('"', '').strip()
        logger.info(f'CPUID: {CPUID}')

    result_dict['CPUID'] = CPUID
    return

def parse_amli_r(cmd_output_list, result_dict):
    ACPI_Method_AMLPointer = ''
    # new_result = get_list_strip(cmd_output_list)
    # # logger.info(f'new_result: {new_result}')
    # result_dict['ACPI_Method_Context'] = new_result

    ACPI_Method_AMLPointer = get_list_text_line(cmd_output_list, 'Next AML Pointer:')

    # 使用正则表达式匹配 [ 和 + 之间的内容
    match = re.search(r'\[(.*?)\+', ACPI_Method_AMLPointer)

    if match:
        ACPI_Method_AMLPointer = match.group(1)
    else:
        logger.info(f'can\'t find ACPI_Method_AMLPointer')

    result_dict['ACPI_Method_AMLPointer'] = ACPI_Method_AMLPointer
    logger.info(f'ACPI_Method_AMLPointer: {ACPI_Method_AMLPointer}')
    return

def parse_ndiskd_oid(cmd_output_list, result_dict):
    Ndis_netadapter1_address = None
    Ndis_netadapter2_address = None
    NDIS_OID_Pending_Status = 0

    text_lines = get_list_text_lines(cmd_output_list, 'NetAdapter')
    if text_lines:
        # logger.info(f'NetAdapter text_lines: {text_lines}')
        NDIS_OID_Pending_Status = 1
        Ndis_netadapter1_name = None
        text_line = text_lines[0].replace('NetAdapter', '').strip()

        match = re.search(r' - (.*)', text_line)
        if match:
            Ndis_netadapter1_name = match.group()
            # logger.info(f"Ndis_netadapter1_name：{Ndis_netadapter1_name}")
            Ndis_netadapter1_name = Ndis_netadapter1_name.replace(' - ', '').strip()
            # logger.info(f"Ndis_netadapter1_name：{Ndis_netadapter1_name}")
        else:
            logger.info("未找到: Ndis_netadapter1_name")

        temp_list = text_line.split('-')
        Ndis_netadapter1_address = temp_list[0].strip()
        # Ndis_netadapter1_name = temp_list[1].strip() # NG

        logger.info(f'NDIS_netadapter1_address: {Ndis_netadapter1_address}')
        logger.info(f'Ndis_netadapter1_name: {Ndis_netadapter1_name}')

        result_dict['Ndis_netadapter1_address'] = Ndis_netadapter1_address
        result_dict['Ndis_netadapter1_name'] = Ndis_netadapter1_name

    if len(text_lines)>=2:
        text_line = text_lines[1].replace('NetAdapter', '').strip()
        temp_list = text_line.split('-')
        Ndis_netadapter2_address = temp_list[0].strip()
        # Ndis_netadapter2_name = temp_list[1].strip() # NG

        match = re.search(r' - (.*)', text_line)
        if match:
            Ndis_netadapter2_name = match.group()
            # logger.info(f"Ndis_netadapter2_name：{Ndis_netadapter2_name}")
            Ndis_netadapter2_name = Ndis_netadapter2_name.replace(' - ', '').strip()
            # logger.info(f"Ndis_netadapter2_name：{Ndis_netadapter2_name}")
        else:
            logger.info("未找到: Ndis_netadapter2_name")

        logger.info(f'Ndis_netadapter2_address: {Ndis_netadapter2_address}')
        logger.info(f'Ndis_netadapter2_name: {Ndis_netadapter2_name}')

        result_dict['Ndis_netadapter2_address'] = Ndis_netadapter2_address
        result_dict['Ndis_netadapter2_name'] = f'{Ndis_netadapter2_name}'


    result_dict['NDIS_OID_Pending_Status'] = NDIS_OID_Pending_Status

    return Ndis_netadapter1_address, Ndis_netadapter2_address

def parse_analyze_v(cmd_output, result_dict):
    cmd_output_list = cmd_output.splitlines()

    start_text = f'***************************'
    end_text = 'Debugging Details:'

    result_list = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)
    new_list = remove_list_text_with_target_text(result_list, '*', 'Bugcheck Analysis')

    # remove Debugging Details:
    new_list = new_list[:-1]

    result_str = '\n' + '\n'.join(new_list)
    result_dict['Bugcheck_Analysis'] = result_str

    item_list = ['BUGCHECK_CODE', 'BUGCHECK_P1', 'BUGCHECK_P2', 'BUGCHECK_P3', 'BUGCHECK_P4', 'FAILURE_BUCKET_ID', 'MODULE_NAME']

    update_dict_by_parse(cmd_output_list, item_list, result_dict)

    count = get_list_text_count(cmd_output_list, 'DISK_HARDWARE_ERROR')
    if count:
        result_dict['DISK_HARDWARE_ERROR_Status'] = 1
    else:
        result_dict['DISK_HARDWARE_ERROR_Status'] = 0

    # Trap_Frame_Context
    update_Trap_Frame_Context(cmd_output_list, result_dict)

    # STACK_TEXT
    start_text = f'STACK_TEXT:'
    end_text = 'SYMBOL_NAME:'
    result = fileOP.get_text_with_start_and_end(cmd_output_list, start_text, end_text)
    update_context_with_list(result, result_dict, 'STACK_TEXT')

    Stack_Memory_Operation_Status = 0
    if result:
        Stack_Memory_Operation_Status = get_Stack_Memory_Operation_Status(result)

    logger.info(f'Stack_Memory_Operation_Status: {Stack_Memory_Operation_Status}')
    result_dict['Stack_Memory_Operation_Status'] = Stack_Memory_Operation_Status

    Memory_Status_Abnormal = 0
    Context_Memory_Corruption_Status = result_dict.get('Context_Memory_Corruption_Status')
    if Context_Memory_Corruption_Status or Stack_Memory_Operation_Status:
        Memory_Status_Abnormal = 1

    result_dict['Memory_Status_Abnormal'] = Memory_Status_Abnormal

    return

def get_driver(input_str):
    # 定义要匹配的前缀
    prefix = '\\Driver\\'

    # 检查字符串是否包含目标前缀
    if prefix in input_str:
        # 找到前缀结束的位置
        prefix_end_index = input_str.find(prefix) + len(prefix)

        # 从 prefix 结束位置开始，截取到制表符(\t)出现的位置
        # 因为原字符串中 igfx 后面是制表符分隔
        tab_index = input_str.find('\t', prefix_end_index)

        # 提取目标字段
        if tab_index != -1:
            target_field = input_str[prefix_end_index:tab_index]
            # logger.info(f"提取到的字段: {target_field}")  # 输出: igfx
        else:
            # 如果没有制表符，直接取剩余全部内容
            target_field = input_str[prefix_end_index:]
            # logger.info(f"提取到的字段: {target_field}")
    else:
        logger.info(f"字符串中不包含前缀: {prefix}")

    return target_field

def parse_amli_lc(cmd_output_list, result_dict):
    ACPI_Method_Address = ''
    ACPI_Method_Object = ''
    ACPI_Method_Status = 0
    for item in cmd_output_list:
        # logger.info(f"item: {item}")
        if 'Ctxt=' in item:
            ACPI_Method_Address = re.findall(r'Ctxt=(.*?),', item)
            ACPI_Method_Address = ACPI_Method_Address[0]
            ACPI_Method_Status = 1
        if 'Obj=' in item:
            prefix = "Obj="
            # 查找前缀在字符串中的位置
            prefix_index = item.find(prefix)
            if prefix_index != -1:
                # 提取前缀后面的所有内容（从prefix结束位置开始截取）
                ACPI_Method_Object = item[prefix_index + len(prefix):]
                ACPI_Method_Object = ACPI_Method_Object.strip()
                logger.info(f"提取到的Obj字段值: {ACPI_Method_Object}")  # 输出: _SB,hello
            else:
                logger.info(f"字符串中未找到 '{prefix}'")
            ACPI_Method_Status = 1

    result_dict['ACPI_Method_Status'] = ACPI_Method_Status
    result_dict['ACPI_Method_Address'] = ACPI_Method_Address
    result_dict['ACPI_Method_Object'] = ACPI_Method_Object

    logger.info(f"ACPI_Method_Address: {ACPI_Method_Address}")
    logger.info(f"ACPI_Method_Object: {ACPI_Method_Object}")
    logger.info(f"ACPI_Method_Status: {ACPI_Method_Status}")
    return


def parse_storadapter_storadapter_adapter_address1_sub(cmd_output_list, result_dict):
    first_index = get_list_text_line_first_index(cmd_output_list, 'Product')
    if first_index:
        target_line = cmd_output_list[first_index + 3]
        # logger.info(f'target_line:{target_line}')

        split_list = target_line.split(' ')
        # logger.info(f'split_list:{split_list}')
        storadapter_storunit1_address = get_list_first_valide_adress(split_list)
        # logger.info(f'storadapter_storunit1_address: {storadapter_storunit1_address}')
        if storadapter_storunit1_address:
            result_dict['storadapter_storunit1_address'] = storadapter_storunit1_address
            logger.info(f'storadapter_storunit1_address: {storadapter_storunit1_address}')

    last_index = get_list_text_line_last_index(cmd_output_list, 'Product')
    if last_index and last_index != first_index:
        target_line = cmd_output_list[last_index + 3]
        # logger.info(f'target_line:{target_line}')

        split_list = target_line.split(' ')
        # logger.info(f'split_list:{split_list}')
        storadapter_storunit2_address = get_list_first_valide_adress(split_list)
        if storadapter_storunit2_address:
            result_dict['storadapter_storunit2_address'] = storadapter_storunit2_address
            logger.info(f'storadapter_storunit2_address: {storadapter_storunit2_address}')
    return

def parse_storadapter_storadapter_adapter_address2_sub(cmd_output_list, result_dict):
    first_index = get_list_text_line_first_index(cmd_output_list, 'Product')
    if first_index:
        target_line = cmd_output_list[first_index + 3]
        # logger.info(f'target_line:{target_line}')

        split_list = target_line.split(' ')
        # logger.info(f'split_list:{split_list}')
        storadapter_storunit1_address = get_list_first_valide_value(split_list)
        result_dict['storadapter_storunit1_address'] = storadapter_storunit1_address
    return

def parse_storadapter_storadapter_adapter1_address(cmd_output_list, result_dict):
    result_str = '\n' + '\n'.join(cmd_output_list)
    result_dict['storadapter_adapter1_Context'] = result_str

    count = get_list_text_count(cmd_output_list, 'SurpriseRemoval')
    if count:
        storadapter_adapter1_SurpriseRemoval_Status = 1
    else:
        storadapter_adapter1_SurpriseRemoval_Status = 0
    result_dict['storadapter_adapter1_SurpriseRemoval_Status'] = storadapter_adapter1_SurpriseRemoval_Status

    parse_storadapter_storadapter_adapter_address1_sub(cmd_output_list, result_dict)

    return

def parse_storadapter_storadapter_adapter2_address(cmd_output_list, result_dict):
    result_str = '\n' + '\n'.join(cmd_output_list)
    result_dict['storadapter_adapter2_Context'] = result_str

    count = get_list_text_count(cmd_output_list, 'SurpriseRemoval')
    if count:
        storadapter_adapter2_SurpriseRemoval_Status = 1
    else:
        storadapter_adapter2_SurpriseRemoval_Status = 0
    result_dict['storadapter_adapter2_SurpriseRemoval_Status'] = storadapter_adapter2_SurpriseRemoval_Status

    parse_storadapter_storadapter_adapter_address2_sub(cmd_output_list, result_dict)
    return

def parse_storadapter(cmd_output_list, result_dict):
    for idx, line in enumerate(cmd_output_list):
        # logger.info(f'line: {line}')

        if 'Driver' in line and 'Object' in line:
            parse_storadapter_driver_and_address(cmd_output_list[idx + 2], result_dict)
    return

def parse_storagekd_storclass(cmd_output_list, result_dict):
    result_str = '\n' + '\n'.join(cmd_output_list)
    result_dict['Storclass_FDO1_Context'] = result_str
    # need logic
    count = get_list_text_count(cmd_output_list, 'Retried')
    if count > 4:
        Storclass_FDO1_Failed_Requests_Status = 1
    else:
        Storclass_FDO1_Failed_Requests_Status = 0

    result_dict['Storclass_FDO1_Failed_Requests_Status'] = Storclass_FDO1_Failed_Requests_Status

    return

def parse_storclass(result_list, result_dict):
    for idx, line in enumerate(result_list):
        if 'FDO' in line and '# Device ID' in line:
            Storclass_FDO1_address = result_list[idx + 2]
            # logger.info(f'Storclass_FDO1: {Storclass_FDO1_address}')
            split_list = Storclass_FDO1_address.split(' ')
            # logger.info(f'split_list: {split_list}')

            Storclass_FDO1_address = split_list[0]
            Storclass_FDO1_DeviceID = f'{split_list[5]} {split_list[6]}'

            # logger.info(f'Storclass_FDO1_DeviceID: {Storclass_FDO1_DeviceID}')
            # logger.info(f'Storclass_FDO1_address: {Storclass_FDO1_address}')

            result_dict['Storclass_FDO1_address'] = Storclass_FDO1_address
            result_dict['Storclass_FDO1_DeviceID'] = Storclass_FDO1_DeviceID

    # result_dict['NDIS_OID_Context'] = result

    return


def parse_powertriage(cmd_output_list, result_dict):
    # logger.info(f'result_dict type: {type(result_dict, current_step)}')
    # System_State_Context
    index = get_list_text_line_first_index(cmd_output_list, 'Power Action:')
    start_idx = index + 1
    end_idx = start_idx + 6
    System_State_Context = cmd_output_list[start_idx: end_idx]
    System_State_Context = '\n'.join(System_State_Context).strip()
    result_dict['System_State_Context'] = System_State_Context
    logger.info(f'System_State_Context: {System_State_Context}')

    # logger.info(f'cmd_output_list: {cmd_output_list}')
    index = get_list_text_line_first_index(cmd_output_list, '+')
    start_idx = index + 1
    end_idx = start_idx + 3
    Device_State_Context = cmd_output_list[start_idx: end_idx]
    Device_State_Context = '\n'.join(Device_State_Context).strip()
    result_dict['Device_State_Context'] = Device_State_Context
    # logger.info(f'Device_State_Context: {Device_State_Context}')
    return

def parse_devstack(cmd_output_list, result_dict):
    result_str = '\n' + '\n'.join(cmd_output_list)
    result_dict['blocked_device_Context'] = result_str

    line = get_list_text_line(cmd_output_list, 'ServiceName is')
    if line:
        line = line.replace('ServiceName is', '')
        line = line.replace('"', '').strip()
        result_dict['blocked_device_ServiceName'] = line

    line = get_list_text_line(cmd_output_list, 'DeviceInst is')
    if line:
        line = line.replace('DeviceInst is', '')
        line = line.replace('"', '').strip()
        result_dict['blocked_device_DeviceInst'] = line

    line = get_list_text_line(cmd_output_list[1:], '>')
    # logger.info(f'line: {line}')
    if line:
         split_list = line.split(' ')
         # logger.info(f'split_list: {split_list}')

         new_list = get_list_strip(split_list)
         # logger.info(f'new_list: {new_list}')

         blocked_device_DevExta_address = new_list[3]
         logger.info(f'blocked_device_DevExta_address: {blocked_device_DevExta_address}')
         result_dict['blocked_device_DevExta_address'] = blocked_device_DevExta_address
    return



if __name__ == '__main__':
    logger.info('common hello')
    pass
