import streamlit as st
from ai_tools.mp_tools.do_db import *
from ai_tools.mp_tools.mp_his import Mp_his

st.title("公众号情报")

# if "script_runs" not in st.session_state:
#     st.session_state.script_runs = 0
#     st.session_state.fragment_runs = 0

@st.experimental_fragment
def crew():
    mp_his = Mp_his()
    if st.button("抓取公众号文章"):
        try:
            mp_his.get_mp_qrcode()
            st.write("请扫描二维码，并授权登录\n\n![登陆二维码](https://jjbiji-pic.oss-cn-beijing.aliyuncs.com/mp_qrcode.png)")
            mp_his.get_his()
        except Exception as e:
            st.write(f"出现错误：{e}")
        st.write("抓取完成")

@st.experimental_fragment
def fragment():
    articles = get_articles_from_mysql()
    if st.button("获取对标公众号文章"):
        for article in articles:
            st.write(f"""
    - **[{article[1]}]({article[4]})**

    作者：{article[2]}

    发布时间：{article[3]}

    摘要：{article[5]}
                    """)

# st.session_state.script_runs += 1
crew()
fragment()
# st.button("Rerun full script")
# st.write(f"Full script says it ran {st.session_state.script_runs} times.")
# st.write(f"Full script sees that fragment ran {st.session_state.fragment_runs} times.")