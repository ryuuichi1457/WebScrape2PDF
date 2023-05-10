import datetime
import img2pdf
import json
import os
import requests
import shutil
import time


from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import urlparse


def saveimage(tag,attributes):
    url_cont = BeautifulSoup(requests.get(url).text, 'html.parser')   # url解析
    img_all = url_cont.find(tag, attrs=attributes)
    img_list = []

    if img_all is None:
        pass
    else:
        found_img = img_all.find_all("img")
        for d in found_img:
            if d is None:
                continue
            d = d.get("src")
            # 画像URLの処理
            if d and d.startswith("http") and d.endswith(("jpg", "jpeg", "png", "bmp")):
                img_list.append(d)  # srcの末尾が.jpgか.pngの場合リストに追加

    for img_data in img_list:  # 画像データをファイルに保存
        json_name = os.path.join("tmp", img_data.split('/')[-1])
        with open(json_name, 'wb') as f:
            f.write(requests.get(img_data).content)
            time.sleep(0.5)
        print(json_name)


def yes_no_input(content):
    while True:
        choice = input(f"{content} y/n : ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False


def saveformat(domain,tag_name,attr_name,attr_value,):
    with open('.json', 'r') as f:
        data = json.load(f)
    new_data = {
        domain: {
            "tag_name": tag_name,
            "attr_name": attr_name,
            "attr_value": attr_value
        }
    }
    data.update(new_data)
    with open('.json', 'w') as f:
        json.dump(data, f, indent=4)



if __name__ == "__main__":
    img_list = []
    tmp_path = './tmp/'
    output_path = "./output/"

    # 現在のディレクトリを取得する
    current_dir = os.getcwd()

    # ファイル名とファイルパスを指定する
    json_name = ".json"
    json_path = os.path.join(current_dir, json_name)

    data = {}

    if os.path.exists(json_path):
        # ファイルが存在する場合はファイルを読み込む
        with open(json_path, "r") as f:
            data = json.load(f)

    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    url = input("URLを入力してください : ")
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")
    use_format = yes_no_input("フォーマットを利用しますか？")

    if domain in data and use_format:
        print("フォーマットが見つかりました！")
        tag_name = data[domain]["tag_name"]
        attr_name = data[domain]["attr_name"]
        attr_value = data[domain]["attr_value"]
    else:
        tag_name = input("要素名を入力 : ")
        attr_name = input("属性名を入力 : ")
        attr_value = input("属性値を入力 : ")
    saveimage(tag_name,{attr_name:attr_value})
    
    now = datetime.datetime.now()
    pdf_filename = output_path + now.strftime('%m%d_%H%M') + input("保存名を入力 : ") + '.pdf'
    allowed_extensions = [".jpg", ".jpeg", ".png", ".bmp"]  # 許可する拡張子のリスト

    # 画像フォルダの中にある許可された拡張子を持つファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
    with open(pdf_filename,"wb") as f:
        f.write(img2pdf.convert([os.path.join(tmp_path, j) for j in os.listdir(tmp_path) if os.path.splitext(j)[1] in allowed_extensions]))
        print("complete!!")
    shutil.rmtree(tmp_path)
    saveformat(domain,tag_name,attr_name,attr_value)