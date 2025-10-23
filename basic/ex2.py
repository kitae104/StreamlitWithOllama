import streamlit as st

st.set_page_config(page_title="메뉴가 있는 홈페이지", page_icon="🧭", layout="wide")

st.title("👋 안녕하세요, Streamlit입니다!")
st.write("이 페이지는 **Streamlit**으로 만든 아주 기본적인 홈페이지 예시입니다.")

if st.button("버튼 눌러보기"):
    st.success("버튼이 잘 동작하네요! 🎉")
    
# --- 사이드바: 라디오 메뉴 ---
with st.sidebar:
    st.header("🧭 메뉴")
    page = st.radio("페이지 이동", ["Home", "About"], index=0)

# --- 본문: 페이지별 콘텐츠 ---
if page == "Home":
    st.title("🏠 Home")
    st.write("여기는 홈입니다. 간단한 안내 문구를 보여줄 수 있어요.")
    st.success("사이드바에서 다른 페이지로 이동해보세요!")

elif page == "About":
    st.title("ℹ️ About")
    st.write("이 사이트는 Streamlit으로 만들었습니다.")
    st.write("- 목적: 초보자용 실습")
    st.write("- 특징: **코드를 저장하면 곧바로 반영**돼요.")