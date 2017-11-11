def dig_dictionary(dictionary, *keys, fill_value=None, fail=False):
    """ Sequentially perform accesses on `dictionary` using `keys`.
        If `fail` is set to `True` missing keys raise an IndexError or KeyError.
        If `fail` is `False` and we encounter a missing key, we return `fill_value`.

    Parameters
    ----------
    dictionary : dict
        Dictionary to dig into.

    *keys : tuple
        Keys to access for each level of digging.
        Also supports integer access for levels that are tuples or lists.

    fill_value : Any, optional
        Value to return if an access on any level during digging fails
        (and `fail` is set to `False`).
        Defaults to `None`.

    fail : bool, optional
        Specifies whether a failing key access on any level should raise an error.
        Defaults to `False`.

    Returns
    ----------
    digged_value : Any
        Value that results from
        `dictionary.get(key1, fill_value).get(key2, fill_value).get(key3, fill_value)`
        etc.

    Examples
    ----------

    Simple digging behaves properly:

    >>> d = {"a": {"b" : 0}}
    >>> dig_dictionary(d, "a", "b")
    0

    We can also dig into more complex objects:

    >>> d = {"a": {3: [1, 2, 3]}}
    >>> dig_dictionary(d, "a", 3, 0)  # last key is index access to list
    1

    Failing accesses return `fill_value`, by default that is `None`, but it
    can be adapted:

    >>> d = {"a": 3}
    >>> dig_dictionary(d, "b", fill_value="fill_value")
    'fill_value'

    If `fail` is set to `True` failing accesses raise the appropriate error:

    >>> d = {"a": 3}
    >>> dig_dictionary(d, "b", fail=True)
    Traceback (most recent call last):
    ...
    KeyError: 'b'

    """

    current_level = dictionary
    for key in keys:
        try:
            current_level = current_level[key]
        except (KeyError, IndexError) as error:
            if fail:
                raise error
            return fill_value
    return current_level
