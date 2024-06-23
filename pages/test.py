import pandas as pd
import streamlit as st
import streamlit as st
from streamlit_option_menu import option_menu

# 使用streamlit-option-menu创建菜单
selected = option_menu(
    menu_title=None,  # 不显示菜单标题
    options=["Home", "Settings", "About"],
    icons=["house", "gear", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# 根据选择显示内容
if selected == "Home":
    st.write("Welcome to the Home page")
elif selected == "Settings":
    st.write("Here you can change settings")
elif selected == "About":
    st.write("This is the About page")

# 初始化数据
data_df = pd.DataFrame(
    {
        "apps": [
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/ef9a7627-13f2-47e5-8f65-3f69bb38a5c2/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/31b99099-8eae-4ff8-aa89-042895ed3843/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/6a399b09-241e-4ae7-a31f-7640dc1d181e/Home_Page.png",
        ],
    }
)

# 使用 session_state 来存储和更新数据
if "data_df" not in st.session_state:
    st.session_state.data_df = data_df

# 定义按钮点击事件
if st.button("更改第一个图片链接"):
    st.session_state.data_df.at[0, "apps"] = "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/6a399b09-241e-4ae7-a31f-7640dc1d181e/Home_Page.png"

# 显示数据编辑器
st.data_editor(
    st.session_state.data_df,
    column_config={
        "apps": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots"
        )
    },
    hide_index=True,
)

import streamlit as st
import pandas as pd

# 创建示例数据
data = {
    'Image': ['image1.jpg', 'image2.jpg', 'image3.jpg'],
    'Text': ['Text 1', 'Text 2', 'Text 3']
}
df = pd.DataFrame(data)

# 显示表格
for index, row in df.iterrows():
    uploaded_image = st.file_uploader(f"Upload Image for Row {index + 1}", type=['jpg', 'png'])
    if uploaded_image is not None:
        # 替换第一列图片
        row['Image'] = uploaded_image

# 显示更新后的表格
st.write(df)