import requests
import json
import os
import yaml
import time
import uuid
from pathlib import Path
from graiax import silkcoder

# 设置基础路径为当前文件夹的上一级
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))




def generate_audio(text, language):
    url_ref = "http://127.0.0.1:9880"
    data_ref = {"text":text, "text_language": language}

    response = requests.post(url = url_ref, json=data_ref)

    #if response:
    # 设置基础路径为当前文件夹的上一级
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # 在基础路径下创建audio_temp文件夹
    base_path = os.path.join(base_path, "audio_temp")
    #print(base_path)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    # 提取文件名，.wav字符前的八个字符为文件名
    #file_name = audio_url.split('/')[-1].split('.')[0][:8]
    # 拼接文件路径
    unique_id = uuid.uuid4()
    save_path = os.path.join(base_path, 'output'+str(unique_id)+'.wav')
    #if not os.path.exists(save_path):
    #    os.makedirs(save_path)
    #print(save_path)
        # 检查请求是否成功
    if response.status_code == 200:
        # 将响应内容写入文件
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("音频文件已成功保存为 'output'"+str(unique_id)+".wav")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        #if download_audio(audio_url, save_path):
           
            # 转换为silk格式
    silk_path = convert_to_silk(save_path, base_path)



            # 删除wav文件
    #os.remove(save_path)
    return silk_path
 

    # 转换为silk
def convert_to_silk(wav_path: str, temp_folder: str) -> str:
    silk_path = os.path.join(temp_folder, Path(wav_path).stem + '.silk')
    if os.path.exists(silk_path):
        os.remove(silk_path)
        time.sleep(0.1)
    silkcoder.encode(wav_path, silk_path)

    # print(f"已将 WAV 文件 {wav_path} 转换为 SILK 文件 {silk_path}")
    return silk_path


if __name__ == "__main__":
    # get_character_list()

    # 测试生成语音
    text = "你好"
    #character = "430"
    generate_audio(text)
