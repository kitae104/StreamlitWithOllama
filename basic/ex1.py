import streamlit as st

# st.set_page_config(page_title="나의 첫 Streamlit", page_icon="👋", layout="centered")

st.title("👋 안녕하세요, Streamlit입니다!")
st.write("이 페이지는 **Streamlit**으로 만든 아주 기본적인 홈페이지 예시입니다.")

if st.button("버튼 눌러보기"):
    st.success("버튼이 잘 동작하네요! 🎉")