import os
import requests
from bs4 import BeautifulSoup
import img2pdf
from PIL import Image
import shutil
import datetime
import json
from urllib.parse import urlparse

def saveimage(tag,attributes):
    url_cont = BeautifulSoup(requests.get(url).text, 'html.parser')   # url解析
    img_all = url_cont.find(tag, attrs=attributes)          # divタグ情報を取得
    img_all_2 = img_all.find_all("img")                                 # imgタグ情報を取得
    for d in img_all_2:
        if d is None:
            continue
        d = d.get("src")
        if d and d.startswith("http") and (d.endswith("jpg") or d.endswith("png")):
         img_list.append(d)  # srcの末尾が.jpgか.pngの場合リストに追加

    for img_data in img_list:  # 画像データをファイルに保存
        file_name = os.path.join("tmp", img_data.split('/')[-1])
        with open(file_name, 'wb') as f:
            f.write(requests.get(img_data).content)  # ファイル保存
        print(file_name)  # 保存ファイル名出力
    #print("サイトのタイトルは"+url_cont.title.string+"です")

def yes_no_input():
    while True:
        choice = input("Please respond with 'yes' or 'no' [y/N]: ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

"""def saveformat(tag_name,attr_name,attr_value):
    save_data = {
    \"domain\": {
        "tag_name": \"div\",
        "attr_name": \"id\",
        "attr_value": \"the-content\"
    }
}
    with open("./.json", mode="w") as json_file3:
        json.dump(save_data, json_file3, ensure_ascii=False, indent=4)
"""
if __name__ == "__main__":
    img_list = []



    # 現在のディレクトリを取得する
    current_dir = os.getcwd()

    # ファイル名とファイルパスを指定する
    file_name = ".json"
    file_path = os.path.join(current_dir, file_name)

    # ファイルが存在する場合はファイルを読み込む
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        # ファイルが存在しない場合は新しいファイルを作成する
        data = {}

    path = './tmp/'
    if not os.path.exists(path):
        os.makedirs(path)
    shutil.rmtree('tmp/')
    os.mkdir(path)



    url = input("URLを入力してください : ")
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")


    use_data = None

    if domain in data:
        print("フォーマットが見つかりました！")
        choice = input("フォーマットを利用しますか？ y/n : ")
        use_data = choice in ("y", "ye", "yes")
        if use_data:
            tag_name = data[domain]["tag_name"]
            attr_name = data[domain]["attr_name"]
            attr_value = data[domain]["attr_value"]
            saveimage(tag_name,{attr_name:attr_value})

    if not use_data:
        tag_name =input("要素名を入力 : ")
        attr_name =input("属性名を入力 : ")
        attr_value =input("属性値を入力 : ")
        saveimage(tag_name,{attr_name:attr_value})


    
    now = datetime.datetime.now()
    pdf_FileName = './output/' + now.strftime('%m%d_')+input("保存名を入力")+'.pdf' # 出力するPDFの名前
    png_Folder = "tmp\\"
    extension  = ".jpg"

    with open(pdf_FileName,"wb") as f:
        # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(img2pdf.convert([Image.open(png_Folder+j).filename for j in os.listdir(png_Folder)if j.endswith(extension)]))
        print("complete!!")
        shutil.rmtree('tmp/')

    """if not domain in data:
        if yes_no_input():
            saveformat(tag_name,attr_name,attr_value)
    """
