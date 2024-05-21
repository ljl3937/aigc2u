import streamlit as st
import requests
import datetime
import os
import concurrent.futures
import time


with st.sidebar:
    if os.environ.get("SD_API_KEY") is None:
        sd_api_key = st.text_input("SD API Key", type="password")
        "[Get an Stability.ai API key](https://platform.stability.ai/account/keys)"
    else: 
        sd_api_key = os.environ.get("DEEPSEEK_API_KEY")
def generate_image(prompt, model, mode, aspect_ratio, output_format, image_path=None, strength=None):
    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    headers = {
        "Authorization": f"Bearer {sd_api_key}",
        "Accept": "image/*"
    }
    
    files = {
        "prompt": (None, prompt),
        "model": (None, model),
        "mode": (None, mode),
        "output_format": (None, output_format)
    }
    
    if mode == '文生图':
        files["aspect_ratio"] = (None, aspect_ratio)
    elif mode == '图生图':
        if image_path:
            # Ensure the image is read as binary
            files['image'] = (image_path.name, image_path.getvalue(), 'image/png')
        if strength is not None:
            files['strength'] = (None, str(strength))

    # Log the files dictionary for debugging
    st.write("Sending the following data to the API:")
    st.write(files)

    try:
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # Will raise an HTTPError for bad requests (4XX or 5XX)
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to make request: {e}")
        return None

def main1():
    # 设置应用的标题
    st.title("SD3 图像生成器应用 ⚡️")
    
    # 用户输入提示词，用于生成图像
    prompt = st.text_input("输入你的提示词：")

    # 用户选择生成模式，"text-to-image" 或 "image-to-image"
    mode = st.selectbox("选择模式：", ["文生图", "图生图"])
    
    # 对于 "图生图" 模式，用户可以上传图片并选择变换强度
    image_file = None
    strength = None
    if mode == '图生图':
        image_file = st.file_uploader("上传你的图片：", type=['png', 'jpg', 'jpeg'])
        strength = st.slider("选择强度 (0.0 到 1.0)：", 0.0, 1.0, 0.5)
    
    # 用户可以选择输出图像的宽高比和格式
    aspect_ratio = st.selectbox("选择宽高比：", ['1:1', '16:9', '4:3'])
    output_format = st.selectbox("选择输出格式：", ['png', 'jpeg'])

    # 用户选择想要使用的SD3模型
    models = ['sd3', 'sd3-turbo']
    selected_models = st.multiselect("选择模型：", models, default=models)

    # 生成图像的按钮
    if st.button("生成图片"):
        # 如果用户没有输入提示词，则显示错误信息
        if not prompt:
            st.error("请输入提示词。")
        else:
            # 使用Spinner显示加载状态
            with st.spinner("正在生成图像..."):
                # 创建线程池来并行生成多个模型的图像
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # 对于每个选择的模型，启动一个生成图像的任务
                    futures = [executor.submit(generate_image, prompt, model, mode, aspect_ratio, output_format, image_path=image_file, strength=strength) for model in selected_models]
                    # 等待所有任务完成并获取结果
                    results = [future.result() for future in futures]
                    
                    # 创建输出文件夹，如果不存在的话
                    output_folder = './outputs'
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    
                    # 遍历结果，保存图像并显示在界面上
                    for result, model in zip(results, selected_models):
                        if result.status_code == 200:
                            # 如果请求成功，保存图像并展示
                            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S").lower()
                            model_prefix = 'sd3' if model == 'sd3' else 'sd3_turbo'
                            output_image_path = f"{output_folder}/{model_prefix}_output_{current_time}.{output_format}"
                            with open(output_image_path, 'wb') as file:
                                file.write(result.content)
                            st.image(output_image_path, caption=f"使用 {model} 生成")
                        else:
                            # 如果请求失败，显示错误信息
                            st.error(f"使用 {model} 生成失败：{result.status_code} - {result.text}")


def main():
    # 设置应用的标题
    st.title("SD3图片生成器 ⚡️")
    
    # 用户输入提示词，用于生成图像
    prompt = st.text_input("输入提示词:")

    # 用户选择生成模式，"文生图" 或 "图生图"
    mode = st.selectbox("选择模式:", ["文生图", "图生图"])
    
    # 对于 "图生图" 模式，用户可以上传图片并选择变换强度
    image_file = None
    strength = None
    if mode == '图生图':
        image_file = st.file_uploader("上传图片:", type=['png', 'jpg', 'jpeg'])
        strength = st.slider("选择强度 (0.0 to 1.0):", 0.0, 1.0, 0.5)
    
    aspect_ratio = '1:1'
    output_format = 'png'
    models = ['sd3', 'sd3-turbo']
    
    if st.button("生成图片"):
        # 如果用户没有输入提示词，则显示错误信息
        if not prompt:
            st.error("请输入提示词。")
        else:
            # 使用Spinner显示加载状态
            with st.spinner("正在生成图片..."):
                # 创建线程池来并行生成多个模型的图像
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # 对于每个选择的模型，启动一个生成图像的任务
                    futures = [executor.submit(generate_image, prompt, model, mode, aspect_ratio, output_format, image_file, strength) for model in models]
                    # 等待所有任务完成并获取结果
                    results = [future.result() for future in futures]
                    
                    # 创建输出文件夹，如果不存在的话
                    output_folder = './outputs'
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    
                    # 遍历结果，保存图像并显示在界面上
                    for result, model in zip(results, models):
                        if result.status_code == 200:
                            # 如果请求成功，保存图像并展示
                            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S").lower()
                            model_prefix = 'sd3' if model == 'sd3' else 'sd3_turbo'
                            output_image_path = f"{output_folder}/{model_prefix}_output_{current_time}.{output_format}"
                            with open(output_image_path, 'wb') as file:
                                file.write(result.content)
                            st.image(output_image_path, caption=f"通过{model}模式生成图片")
                        else:
                            # 如果请求失败，显示错误信息
                            st.error(f"使用 {model} 生成失败：{result.status_code} - {result.text}")

if __name__ == "__main__":
    main()
