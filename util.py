def filter_dict(old_dict, callback):
    new_dict = dict()
    for (key, value) in old_dict.items():
        if callback((key, value)):
            new_dict[key] = value
    return new_dict