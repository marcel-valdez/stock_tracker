
def get_key(options, key, default):
    if key in options:
        return options[key]
    else:
        return default
