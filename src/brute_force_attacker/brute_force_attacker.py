import worker_dispatcher
import string

def process_call(id: int, task, config):
    recursion(task, config['left_length'], config['char_map'], config)
    return True

def recursion(prefix: str, length: int, char_map: list, config):
    for char in char_map:
        char_string = "{}{}".format(prefix, char)
        if length <= 1:
            config['callback'](char_string);
        else:
            recursion(char_string, length - 1, char_map, config)
    return

def user_func_sample(char_string):
    print(char_string)
    return 

# Default configuration
default_config = {
    'length': 2,
    'char_map': string.digits + string.ascii_lowercase + string.ascii_uppercase,
    'callback': user_func_sample
}

# Start
def start(user_config: dict, debug: bool=False):
    global default_config
    config = {**default_config, **user_config}

    # Debug mode
    if debug:
        print("Configuration Dictionary:")
        print(config)

    length = config['length']
    char_map = config['char_map']

    # Callback check
    if not callable(config['callback']):
        exit("Callback function is invalied")

    # Use WorkerDispatcher while length > 3
    if length <= 2:
        recursion('', length, char_map)
        return
    
    task_list = []
    for char1 in char_map:
        for char2 in char_map:
            task_list.append("{}{}".format(char1, char2))

    # print(task_list)
    result = worker_dispatcher.start({
        'task': {
            'list': task_list,
            'callback': process_call,
            'config': {
                'callback': config['callback'],
                'char_map': char_map,
                'left_length': length - 2
            }
        },
        'worker': {
            'number': 1,
            'multiprocessing': True
        },
        'verbose': False
    })
    
    return
