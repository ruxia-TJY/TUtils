from PIL import Image
import os
from rich.console import Console

console = Console()

rules = {
    "path":{
        "type":"str",
        "rules":1,
        "value":None
    },
    "outputpath":{
        "type":"str",
        "rules":1,
        "value":None
    },
    "size":{
        "type":"str",
        "rules":"?",
        "value":"64,128"
    }
}

SUPPORT_LIST = ["jpg","jpeg","png","bmp","webp"]

ICO_SUPPORT_SIZES = [(16,16),(32,32),(64,64),(128,128),(256,256)]

def get_name_and_ext(path):
    basename = os.path.basename(path)
    name,ext = os.path.splitext(basename)
    return name,ext

def convert_to_ico(file_path, ico_path, sizes):
    global SUPPORT_LIST, ICO_SUPPORT_SIZES

    name, ext = get_name_and_ext(file_path)
    ext = ext[1:]

    if ext not in SUPPORT_LIST:
        return

    try:
        img = Image.open(file_path)
    except Exception as e:
        console.print(f"Error: {e}",style='bold red')
        return

    for size in sizes:
        if size not in ICO_SUPPORT_SIZES:
            console.print(f"Error: Invalid size '{size}'",style="bold red")
            continue

        new_img = img.resize((size[0],size[1]),Image.LANCZOS)
        output_path = os.path.join(ico_path,f'{name}_{ext}_{size[0]}x{size[1]}.ico')

        new_img.save(output_path,format='ico',size=size)
        console.print(f'Success: {file_path} -> {output_path}', style='bold green')



def main(cmd:dict):
    input_path= cmd["path"]["value"][0]
    output_path = cmd["outputpath"]["value"][0]
    sizes = cmd["size"]["value"].split(",")

    size_list = []
    for size in sizes:
        w,h = int(size),int(size)
        size_list.append((w,h))

    if os.path.isfile(input_path):
        name, ext = get_name_and_ext(input_path)
        ext = ext[1:]
        if ext not in SUPPORT_LIST:
            console.print(f"Error: file format {ext} not in support ",style='bold red')
        convert_to_ico(input_path,output_path,size_list)
    else:
        for file in os.listdir(input_path):
            _,ext = os.path.splitext(file)
            file_path = os.path.abspath(file)
            convert_to_ico(file_path,output_path,size_list)