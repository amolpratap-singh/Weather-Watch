
def call_function(target_func, func_vars):
    flattened_dict = {k: v for k, v in func_vars.items() if k!= 'kwargs'}
    flattened_dict.update(func_vars.get('kwargs', {}))
    # Call the target_func with the provided func_vars
    return target_func(**flattened_dict)