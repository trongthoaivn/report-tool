import subprocess
import sys
import time
import os
import base64
from flask import Flask, render_template, session
from flask_session import Session
from bs4 import BeautifulSoup as bs

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

def convert_to_pdf(input_file_path:str , output_folder:str):
    """_summary_

    Args:
        input_file_path (str): _description_
        output_folder (str): _description_
    """
    os_name = sys.platform
    if os_name == "win32":
        libreoffice_app = 'start "" "C:\\Program Files\\LibreOffice\\program\\soffice.com"'
        command = libreoffice_app + " --nologo --convert-to pdf "+ input_file_path +" --outdir " + output_folder
        result = subprocess.run(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        print(result)
    else:
        command = "libreoffice --convert-to pdf "+ input_file_path +" --outdir " + output_folder
        result = subprocess.run(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        print(result)


def create_file_name():
    """_summary_

    Returns:
        _type_: _description_
    """
    file_name = str(time.strftime("%Y%m%d-%H%M%S")) + ".xml"
    return file_name

def create_pdf_file(data:dict, config:dict = None , template_path:str = "", remove_file:int = 0):
    """_summary_

    Args:
        data (dict): _description_
        config (dict): _description_
        template_path (str): _description_

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    try: 
        out_put_path = os.path.join("pdf-output/"+ create_file_name()) 
        if not os.path.exists("templates/"+template_path):
            raise Exception("not exist template!")
        xml_str = render_template(template_path, data = data)
        format_style(xml_str)
        file_xml = open(out_put_path, "w",encoding="utf-8")
        file_xml.write(xml_str)
        file_xml.close()
        if not os.path.exists(out_put_path):
            raise Exception("convert template fail")
        convert_to_pdf(out_put_path,"pdf-output")
        pdf_file_path = str(out_put_path).replace("xml","pdf")
        file_pdf = open(pdf_file_path, "rb")
        encoded_string = base64.b64encode(file_pdf.read())
        file_pdf.close()
        if remove_file == 0:
            os.remove(out_put_path)
            os.remove(pdf_file_path)
        if remove_file == 1:
            os.remove(out_put_path)
        return{
            "code" : "success",
            "data" : {
                "file_path" : pdf_file_path,
                "base64_str" : encoded_string
            }
        }
  
    except Exception as ex:
        print(ex)
        return {
            "code" : "fail",
            "message" : str(ex)
        } 


def format_style(xml_str:str, config:dict={}):
    config = {
        "rules":{
            "color_red": True
        },
        "setting":{
            "color_red": {
                "text-properties":{
                    "fo:color": "#c9211e"
                }
            }
        }

    }
    bs_obj = bs(xml_str, "xml")
    namespace =  get_namespace(xml_str)
    for key, value in config["rules"].items():
        p_tags = list(filter(lambda x: str(x.string).find(key) != -1
                                    and value, bs_obj.find_all("p"))) 
        if len(p_tags) > 0:
            for index, p in enumerate(p_tags):
                style_name = p.parent.attrs.get("table:style-name")
                style_tag = bs_obj.find_all("style:style",{"style:name": style_name})[0]
                setting = config.get("setting")
                if setting.get(key) is not None:
                    for format_key, format_value in setting.get(key).items():
                        format = style_tag.find_all(format_key)[0]
                        for setting_key, setting_value in format_value.items():
                            format.attrs[setting_key] = setting_value
    return str(bs_obj)


def get_namespace(xml_str:str):
    bs_obj = bs(xml_str, "xml")
    attrs = bs_obj.find("office:document").attrs
    namespace = '<tag ' + " ".join(attrs) +" >"
    return namespace
