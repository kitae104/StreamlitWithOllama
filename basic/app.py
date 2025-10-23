import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Streamlit 미니 홈페이지", page_icon="🌟", layout="wide")

# --- 간단 스타일(CSS) ---
st.markdown("""
<style>
.main .block-container { max-width: 1100px; }
.card {
  padding: 18px; border-radius: 14px;
  background: #ffffff; border: 1px solid #eef1f6;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  margin-bottom: 16px;
}
.footer {
  margin-top: 36px; padding: 12px 0; color: #6b7280; font-size: 13px; text-align: center;
  border-top: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# --- 사이드바 ---
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=140)
    st.header("🧭 메뉴")
    page = st.radio("페이지 이동", ["Home", "Data", "About"], index=0)
    st.write("---")
    st.caption("💡 코드를 저장하면 바로 반영됩니다.")

# --- 상단 배너(공통) ---
st.markdown(
    """
    <div class="card" style="background: linear-gradient(90deg, #f8fbff, #f2f6ff);">
      <h2 style="margin:0;">🌟 Streamlit 미니 홈페이지</h2>
      <p style="margin:6px 0 0 0; color:#333;">메뉴/이미지/데이터 분석을 점층적으로 추가한 예제</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")

# --- 페이지 본문 ---
if page == "Home":
    st.title("🏠 Home")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("이 사이트에서 할 수 있는 것")
        st.markdown(
            """
            - 좌측 **사이드바 메뉴**로 페이지 이동  
            - **CSV 업로드** 또는 **샘플 데이터**로 표/차트 보기  
            - **레이아웃/이미지**로 홈페이지 꾸미기
            """
        )
        st.success("Streamlit은 '데이터 + UI'를 빠르게 만들 수 있어요.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image(
            "https://images.unsplash.com/photo-1504639725590-34d0984388bd?q=80&w=1200&auto=format&fit=crop",
            caption="홈 대표 이미지",
            use_column_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "About":
    st.title("ℹ️ About")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(
        """
        이 프로젝트는 **완전 초보자**도 Streamlit으로  
        - 홈페이지 구조 만들기  
        - 메뉴로 페이지 분리  
        - 간단 데이터 분석 페이지까지  
        완성하는 과정을 보여줍니다.
        """
    )
    st.info("수정 → 저장 → 새로고침으로 빠르게 반복 개발!")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Data":
    st.title("📊 Data — 간단 분석")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    file = st.file_uploader("CSV 업로드(선택)", type=["csv"])
    if file is not None:
        df = pd.read_csv(file)
        st.success("CSV 로드 성공!")
    else:
        np.random.seed(42)
        df = pd.DataFrame({
            "day": pd.date_range("2025-01-01", periods=150, freq="D"),
            "value": (np.random.randn(150).cumsum() + 5).round(2)
        })
        st.info("파일이 없어서 샘플 데이터를 사용 중입니다.")

    st.write("### 표 보기")
    rows = st.slider("표시할 행 수", 5, len(df), min(30, len(df)))
    st.dataframe(df.head(rows), use_container_width=True)

    st.write("### 차트")
    chart_type = st.selectbox("차트 선택", ["line_chart", "bar_chart"], index=0)
    if chart_type == "line_chart":
        st.line_chart(df.set_index("day")["value"])
    else:
        st.bar_chart(df.set_index("day")["value"])
   
    st.markdown('</div>', unsafe_allow_html=True)

# --- 공통 푸터 ---
st.markdown('<div class="footer">© 2025 기태의 홈페이지 · 문의: kkt@inhatc.ac.kr</div>', unsafe_allow_html=True)