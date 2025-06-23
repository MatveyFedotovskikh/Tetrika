def strict(func):
    def wrapper(*args, **kwargs):
        if len(args) + len(kwargs) == len(func.__annotations__)-1:
            annotations = func.__annotations__
            
            for num_args, name in enumerate(annotations.keys()):
                if num_args < len(args):
                    if not isinstance(args[num_args], annotations[name]):
                        raise TypeError(f"Argument '{name}' must be of type {annotations[name].__name__}, got {type(args[num_args]).__name__}")
                    num_args += 1
                elif name in kwargs:
                    if not isinstance(kwargs[name], annotations[name]):
                        raise TypeError(f"Argument '{name}' must be of type {annotations[name].__name__}, got {type(kwargs[name]).__name__}")
            
        return func(*args, **kwargs)
    return wrapper
