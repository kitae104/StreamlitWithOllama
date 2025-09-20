import streamlit as st
import os, hashlib, io

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

# ✅ 최신 권장 임포트 경로
from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="PDF/TXT Q&A 챗봇")
st.title("📄 PDF/TXT 파일 Q&A 챗봇")
st.markdown("Ollama와 Streamlit을 이용한 RAG 챗봇")

# ---------------------------
# Ollama 설정
# ---------------------------
OLLAMA_URL = "http://127.0.0.1:11434"
LLM_MODEL = "exaone3.5:2.4b" # 또는 "gemma:2b"
EMB_MODEL = "bge-m3" # 또는 "nomic-embed-text"

llm = OllamaLLM(
    model=LLM_MODEL,
    base_url=OLLAMA_URL,
    streaming=True,
    # ↓ langchain_ollama는 아래를 그대로 전달합니다.
    model_kwargs={
        "num_predict": 256,     # 최대 생성 토큰 (필수)
        "num_ctx": 2048,        # 문서+프롬프트 총 길이 상한(필요 이상 키우지 않기)
        "temperature": 0.2,     # 낮을수록 일관/짧은 답변
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "keep_alive": "30m",    # 프로세스 유지(콜드스타트 방지)
        "num_thread": 0,      # 0=자동(코어수). CPU라면 명시적 설정도 고려
    }
)
embeddings = OllamaEmbeddings(model=EMB_MODEL, base_url=OLLAMA_URL)

# ---------------------------
# 유틸: 파일 해시 + 파라미터로 캐시 키 생성
# ---------------------------
def file_digest(file_bytes: bytes, extra: str) -> str:
    h = hashlib.sha256()
    h.update(file_bytes)
    h.update(extra.encode("utf-8"))
    return h.hexdigest()

# ---------------------------
# 캐시: 벡터스토어 로드/생성
# ---------------------------
@st.cache_resource(show_spinner=False)
def build_or_load_faiss(index_dir: str, docs, chunk_size: int, chunk_overlap: int):
    # docs -> splits -> FAISS
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = splitter.split_documents(docs)
    db = FAISS.from_documents(splits, embeddings)
    os.makedirs(index_dir, exist_ok=True)
    db.save_local(index_dir)
    return db

@st.cache_resource(show_spinner=False)
def load_faiss(index_dir: str):
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

# ---------------------------
# 파일 로드 함수
# ---------------------------
def load_docs_from_bytes(name: str, raw: bytes):
    ext = os.path.splitext(name)[1].lower()
    temp_dir = "./temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, name)
    with open(file_path, "wb") as f:
        f.write(raw)

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        st.error("지원하지 않는 파일 형식입니다. (PDF, TXT만 지원)")
        return None
    return loader.load()

# ---------------------------
# 사이드바: 업로드 & 인덱스 준비
# ---------------------------
with st.sidebar:
    st.header("파일 업로드")
    uploaded_file = st.file_uploader("PDF 또는 TXT 파일을 업로드하세요", type=["pdf", "txt"])

    # 인덱스 파라미터(변경 시 새 캐시 키가 생성되도록)
    chunk_size = st.number_input("chunk_size", 300, 4000, 500, 100)
    chunk_overlap = st.number_input("chunk_overlap", 0, 800, 100, 50)

    if uploaded_file:
        raw = uploaded_file.read()  # 중요: 바이트 읽고 아래에서 재사용
        st.success("파일 업로드 완료!")

        # 파일+설정+모델 조합으로 캐시 키 생성
        extra = f"{uploaded_file.name}|{chunk_size}|{chunk_overlap}|{LLM_MODEL}|{EMB_MODEL}"
        digest = file_digest(raw, extra)
        index_dir = f"./indexes/{digest}"

        # 세션에 현재 선택 파일의 digest 저장
        st.session_state["current_digest"] = digest

        # 이미 인덱스가 있으면 즉시 로드, 없으면 생성
        if os.path.isdir(index_dir) and os.path.exists(os.path.join(index_dir, "index.faiss")):
            with st.spinner("기존 인덱스 로드 중..."):
                db = load_faiss(index_dir)
        else:
            with st.spinner("문서 처리 및 벡터화 중... (최초 1회)"):
                docs = load_docs_from_bytes(uploaded_file.name, raw)
                if docs:
                    db = build_or_load_faiss(index_dir, docs, chunk_size, chunk_overlap)
                else:
                    db = None

        if db:
            st.session_state["db"] = db
            st.success("준비 완료! (캐시/인덱스 사용)")

# ---------------------------
# 채팅 상태
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------------------------
# 질의 (LCEL 방식으로 재구성)
# ---------------------------
prompt = st.chat_input("질문을 입력하세요")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("생각하는 중..."):
            db = st.session_state.get("db")
            if db is None:
                st.warning("먼저 왼쪽에서 PDF/TXT를 업로드하여 인덱스를 준비해 주세요.")
                st.stop()

            # 1. 리트리버 설정 (기존과 동일)
            # 💡 속도를 위해 k=2 정도로 낮게 유지하는 것이 좋습니다.
            retriever = db.as_retriever(search_kwargs={"k": 2})

            # 2. 프롬프트 템플릿 정의
            template = """
            당신은 질문에 답변하는 AI 어시스턴트입니다.
            주어진 문서를 바탕으로, 사용자의 질문에 대해 답변해 주세요.
            문서에서 답을 찾을 수 없다면 "문서에서 관련 정보를 찾을 수 없습니다."라고 답변하세요.

            문서:
            {context}

            질문:
            {question}
            """
            prompt_template = ChatPromptTemplate.from_template(template)

            # 3. 문서 포맷팅 함수 정의
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            # 4. LCEL 체인 구성
            chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt_template
                | llm
                | StrOutputParser()
            )

            # 5. 스트리밍 실행 및 출력
            # st.write_stream은 제너레이터를 인자로 받습니다.
            # chain.stream()은 각 토큰을 생성하는 제너레이터입니다.
            answer = st.write_stream(chain.stream(prompt))

            # --- 참고 문서 표시는 스트림이 끝난 후 처리 ---
            srcs = retriever.get_relevant_documents(prompt)
            if srcs:
                names = list({os.path.basename(s.metadata.get("source", "")) for s in srcs})
                if names:
                    ref_text = "\n\n---\n**참고 문서**: " + ", ".join(names)
                    st.markdown(ref_text)
                    full_answer = answer + ref_text
                else:
                    full_answer = answer
                st.session_state.messages.append({"role": "assistant", "content": full_answer})
            else:
                st.session_state.messages.append({"role": "assistant", "content": answer})
