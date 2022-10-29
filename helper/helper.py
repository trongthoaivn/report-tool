from flask import Flask,render_template,session
from flask_session import Session

def  find_item_by_key_value(data:dict ,key:str, value):
    """_summary_

    Args:
        data (dict): _description_
        key (str): _description_
        value (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    try:
        filter_data = list(filter(lambda i: i[key] == value, data )) 
        if len(list(filter_data)) > 0:
            return filter_data[0]
        else:
            raise Exception("item not exist!")
    except Exception:
        return None

def delete_item(data:dict, item, key_data):
    """_summary_

    Args:
        data (dict): _description_
        key (str): _description_
        value (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    try:
        data = list(filter(lambda i: i != item, data))
        session[key_data] = data
        return True
    except Exception:
        return False
