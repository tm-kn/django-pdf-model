def flatten_list(value):
    final_list = []
    for item in value:
        if isinstance(item, list):
            final_list += flatten_list(item)
        else:
            final_list.append(item)
    return final_list
