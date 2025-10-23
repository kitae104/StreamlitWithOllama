import streamlit as st

st.set_page_config(page_title="메뉴가 있는 홈페이지", page_icon="🧭", layout="wide")

# st.title("👋 안녕하세요, Streamlit입니다!")
# st.write("이 페이지는 **Streamlit**으로 만든 아주 기본적인 홈페이지 예시입니다.")

# if st.button("버튼 눌러보기"):
#     st.success("버튼이 잘 동작하네요! 🎉")
    
# --- 상단 배너(공통) ---
st.markdown(
    """
    <div style="padding: 16px; border-radius: 12px; background: linear-gradient(90deg, #f6f9ff, #eef3ff);">
        <h2 style="margin:0;">🎨 Streamlit 미니 홈페이지</h2>
        <p style="margin:6px 0 0 0; color:#333;">단계별로 기능을 추가하며 완성해봅시다!</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")

# --- 사이드바: 라디오 메뉴 ---
with st.sidebar:
    st.header("🧭 메뉴")
    page = st.radio("페이지 이동", ["Home", "About"], index=0)

# --- 본문: 페이지별 콘텐츠 ---
if page == "Home":
    st.title("🏠 Home")
    # st.write("여기는 홈입니다. 간단한 안내 문구를 보여줄 수 있어요.")
    # st.success("사이드바에서 다른 페이지로 이동해보세요!")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("간단 소개")
        st.write(
            """
            - 이 사이트는 **Streamlit**으로 만든 연습용 홈페이지입니다.  
            - 좌측 메뉴로 페이지를 이동할 수 있습니다.  
            - 오른쪽에 이미지를 넣어 '홈' 느낌을 살려볼게요.
            """
        )
        st.success("컬럼으로 정보와 이미지를 나란히 배치했습니다.")

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1529101091764-c3526daf38fe?q=80&w=1200&auto=format&fit=crop",
            caption="Unsplash 예시 이미지",
            use_column_width=True,
        )
    
elif page == "About":
    st.title("ℹ️ About")
    st.write("이 사이트는 Streamlit으로 만들었습니다.")
    st.write("- 목적: 초보자용 실습")
    st.write("- 특징: **코드를 저장하면 곧바로 반영**돼요.")
    
elif page == "Data":
    st.title("📊 Data — 간단 분석")

    st.write("**1) CSV 업로드** (없으면 샘플 데이터 사용)")
    file = st.file_uploader("CSV 파일 선택", type=["csv"])

    if file is not None:
        df = pd.read_csv(file)
        st.success("CSV 로드 성공!")
    else:
        np.random.seed(0)
        df = pd.DataFrame({
            "day": pd.date_range("2025-01-01", periods=100, freq="D"),
            "value": np.random.randn(100).cumsum() + 10
        })
        st.info("샘플 데이터 사용 중입니다. (업로드 시 자동 대체)")

    max_rows = st.slider("표시할 최대 행 수", 5, len(df), min(20, len(df)))
    st.dataframe(df.head(max_rows), use_container_width=True)

    chart_type = st.selectbox("차트 유형", ["line_chart", "bar_chart"], index=0)
    st.write("**2) 차트**")
    if chart_type == "line_chart":
        st.line_chart(df.set_index("day")["value"])
    else:
        st.bar_chart(df.set_index("day")["value"])