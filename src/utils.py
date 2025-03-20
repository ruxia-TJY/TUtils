import os
import numbers
import config
from config import COLOR_LIST
from rich.console import Console

console = Console()

bool_map = {
    "true":True,
    "True":True,
    "t":True,
    "false":False,
    "False":False,
    "f":False,
}

def modifyType(value:str, type:str):
    '''
    change the type from string
    :param value: value to modify
    :param type: target type
    :return: value
    '''
    if type == 'bool':
        return bool_map.get(value.lower(),None)
    if type == 'int':
        return int(value)
    if type == 'float':
        return float(value)
    if type == 'str':
        return str(value)
    return None

def parse(rules:dict,*cmds) -> dict:
    '''
    parse command for script
    :param rules: script rules
    :param cmds: script commands
    :return: parsed values
    '''
    cmds = cmds[0]
    cmdslen = len(cmds)
    cur_index = 0

    for i,rule in enumerate(rules.keys()):
        if rules[rule]['rules'] == '?':
            # ? 0/1
            if cur_index == cmdslen:
                continue
            else:
                rules[rule]['value'] = modifyType(cmds[cur_index],rules[rule]['type'])
                if rules[rule]['value'] is None:
                    raise Exception(f'Parser Error: Value for rule {rule} is None')
                cur_index += 1
            pass
        elif isinstance(rules[rule]['rules'],numbers.Number):
            # number
            n = int(rules[rule]['rules'])
            lst = []
            for i in range(n):
                value = modifyType(cmds[cur_index],rules[rule]['type'])
                if value is None:
                    raise Exception(f'Parser Error: Value for rule {rule} is None')
                else:
                    lst.append(modifyType(cmds[cur_index],rules[rule]['type']))
                    cur_index += 1
            rules[rule]['value'] = lst
        elif rules[rule]['rules'] == '*':
            # * null or more
            n = cmdslen - cur_index
            lst = []
            for i in range(n):
                value = modifyType(cmds[cur_index], rules[rule]['type'])
                if value is None:
                    raise Exception(f'Parser Error: Value for rule {rule} is None')
                else:
                    lst.append(modifyType(cmds[cur_index], rules[rule]['type']))
                    cur_index += 1
            rules[rule]['value'] = lst

    return rules

def readDataList() -> None:
    '''
        get script data list
    :return: None
    '''
    subdirs = [d for d in os.listdir(config.SCRIPT_DIR) if os.path.isdir(os.path.join(config.SCRIPT_DIR, d))]
    for dir in subdirs:
        config.SCRIPTDB[dir] = []
        for file in os.listdir(os.path.join(config.SCRIPT_DIR, dir)):
            if file.endswith(".py"):
                 config.SCRIPTDB[dir].append(file)

def findInScriptDB(name:str) -> list[str]:
    '''
        find scripts in db
    :param name: script name
    :return: list
    '''
    ret = []
    name = f'{name}.py'
    for key,value in config.SCRIPTDB.items():
        if name in value:
            ret.append(f'{key}.{name}')
    return ret

def find(name:str) -> None|str:
    '''
        find script in db,if not only 1,do select
    :param name: script name
    :return: None if not found, else path
    '''
    lst = findInScriptDB(name)
    if len(lst) == 0:
        return None
    elif len(lst) == 1:
        return lst[0]
    else:
        check = 0
        reselect = False
        selectList = [str(i) for i in range(len(lst))]
        for i,value in enumerate(lst):
            color = COLOR_LIST[i % len(COLOR_LIST)]
            console.print(f'{i}. {value[:-2]}',style=color)

        check = input('Not only 1,please select:')

        while check not in selectList:
            console.print(f'checked {check} not exist !', style='bold red')
            console.rule()
            for i,value in enumerate(lst):
                color = COLOR_LIST[i % len(COLOR_LIST)]
                console.print(f'{i}. {value[:-2]}',style=color)

            console.print(f'ReCheck :', style='bold red',end='')
            check = input('')

        return lst[int(check)]

def checkInScriptDB(path:str) -> None|str:
    '''
    check scripts is exist in db
    support such as file.getCount
    :param path: script path
    :return: None if not found, else path
    '''
    d,name = path.split('.')
    if d not in config.SCRIPTDB.keys():
        return None

    name = f'{name}.py'
    if name not in config.SCRIPTDB[d]:
        return None

    return f'{d}.{name}'