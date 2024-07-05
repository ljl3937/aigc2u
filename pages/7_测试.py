import streamlit as st
import pandas as pd

article = """
在这个充满不确定的时代，你是否也对自己的职业未来感到迷茫？从996ICU到内卷、躺平，一面尝着老板画的饼，一面自愿加班累如狗，社畜们面临着前所未有的职业挑战。一部分职场老油条开始转型，打工是不可能打工的，要么创业、要么自媒体，然而一顿操作猛如虎，一看战绩却像鼠。似乎当下的每个职场人都对自己的未来感到迷茫和困惑。但是，不要担心！我开发了一款很有用的职业规划神器！你可以用它来规划你目前职业的成长路径，也可以帮你定位职场转型，分析自身的优势和发展方向。只需输入你的职业，比如‘程序员’，我们的神器就能为你展示一条清晰的职业成长路径，并以思维导图的方式为您呈现。如果你担心AI的冲击太大，想要转型，又要保持程序员的优势，只需输入‘程序员跨界转型’，我们的神器将为你提供专门针对程序员的近乎完美的转型方案。怎么样？还是很不错的吧？快来试试吧！我是加加，一个专注于大模型开发的IT老兵。如果你喜欢这个神器，就点个赞吧！让我们一起，为你的职业未来，加油！
"""
sentences = article.split('。')
frm_data = []
for sentence in sentences:
    print(sentence.strip())
    frm_data.append({'sentence': sentence.strip(), 'rating': 0, 'is_widget': False})

df = pd.DataFrame(
    frm_data
)
edited_df = st.data_editor(df, num_rows="dynamic")

favorite_sentence = edited_df.loc[edited_df["rating"].idxmax()]["sentence"]
st.markdown(f"Your favorite sentence is **{favorite_sentence}** 🎈")