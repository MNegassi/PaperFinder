

def dig_dictionary(dictionary, *keys, fill_value=None, fail=False):

    current_level = dictionary
    for key in keys:
        print(current_level, type(current_level))
        try:
            current_level = current_level[key]
        except (KeyError, IndexError) as error:
            if fail:
                raise error
            return fill_value
    return current_level
