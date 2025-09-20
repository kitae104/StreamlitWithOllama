##########################################################
# 1단계: Streamlit 기본 UI 및 Ollama 연동 챗봇 만들기
##########################################################

import streamlit as st
from langchain_community.llms import Ollama

# Ollama 모델 초기화
llm = Ollama(model="exaone3.5:2.4b")

st.title("기본 챗봇")

# 대화 기록(session_state) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("무엇이든 물어보세요"):
    # 사용자 메시지 표시 및 기록
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ollama를 사용하여 응답 생성
    with st.spinner("생각하는 중..."):
        response = llm.invoke(prompt)
    
    # 챗봇 응답 표시 및 기록
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)