""" Streamlit을 사용해 파일을 업로드하고 내용을 확인하는 파이썬 코드입니다. 
이 코드는 .txt, .csv, .pdf 파일을 처리하며, 파일 내용과 상세 정보를 웹페이지에 표시합니다. """
import streamlit as st
import os
import PyPDF2

st.title("파일 업로드 및 내용 확인")

# 파일 업로드 위젯
uploaded_file = st.file_uploader("파일을 선택하세요", type=["txt", "csv", "pdf"])

if uploaded_file is not None:
    # 파일 정보 출력
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
    st.write(file_details)

    # 파일 확장자 확인
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    if file_extension in [".txt", ".csv"]:
        # 텍스트 파일인 경우 내용 디코딩 및 표시
        content = uploaded_file.read().decode("utf-8")
        st.text_area("파일 내용", content, height=300)

    elif file_extension == ".pdf":
        try:
            
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            num_pages = len(pdf_reader.pages)
            st.write(f"PDF 파일입니다. 총 {num_pages} 페이지.")
            
            full_text = ""
            for page in range(num_pages):
                page_obj = pdf_reader.pages[page]
                full_text += page_obj.extract_text() or ""
            st.text_area("PDF 내용", full_text, height=300)

        except ImportError:
            st.error("PyPDF2 라이브러리가 설치되어 있지 않습니다. `pip install PyPDF2` 를 실행하여 설치해 주세요.")
            
    else:
        st.warning("지원하지 않는 파일 형식입니다.")