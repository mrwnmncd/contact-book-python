    
def required_input(message: str, **config) -> str:
    user_input = input(message)
    if config.get("default_value", False) and len(user_input) == 0:
        return config.get("default_value")
    while len(user_input) == 0:
        if config.get("throw_exception", True):
            raise ValueError("Input is required.")
        else: 
            print("Input is required.")
        user_input = input(message)
    return user_input