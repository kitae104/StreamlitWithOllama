#########################################################
# 2단계: PDF 파일 업로드 및 문서 로딩 기능 추가
#########################################################

import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
import os

# Ollama 모델 초기화
llm = Ollama(model="exaone3.5:2.4b")

# ===================================================================
# 파일 업로드 핸들러
def handle_file_upload(uploaded_file):
    temp_dir = "./temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    loader = PyPDFLoader(file_path)
    return loader.load()
# ===================================================================

st.title("PDF 파일 로딩 챗봇")
st.markdown("왼쪽 사이드바에서 PDF 파일을 업로드하세요.")

# ===================================================================
# 사이드바에 파일 업로드 위젯 추가
with st.sidebar:
    st.header("파일 업로드")
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

    if uploaded_file:
        st.success("파일 업로드 완료!")
        docs = handle_file_upload(uploaded_file)
        st.session_state.docs = docs
        st.write("로드된 문서의 첫 100자:")
        st.text(docs[0].page_content[:100] + "...")
        st.success("문서 로딩 완료!")
# ===================================================================

# 챗봇 UI (1단계와 동일)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("무엇이든 물어보세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("생각하는 중..."):
        response = llm.invoke(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)