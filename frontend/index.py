import uuid
import requests
import streamlit as st


st.set_page_config(
    page_title="ClauseGuard: Legal PDF Auditor & Risk Agent",
    page_icon="⚖️",
    layout="wide"
)

url = "http://3.238.80.219:8000"

st.title("⚖️ ClauseGuard: Legal PDF Auditor & Risk Agent")
st.markdown(
    "Upload a legal document and let ClauseGuard identify key clauses, potential risks, and relevant provisions using AI-powered document analysis."
)


if "thread_id" not in st.session_state or st.session_state.thread_id is None:
    st.session_state.thread_id = str(uuid.uuid4())

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    document = st.file_uploader(
        "Upload your Legal Document (PDF Only)",
        type=['pdf']
    )
    if document:
        if st.button("Analyze Document", use_container_width=True):
            st.session_state.uploaded_file_name = document.name
            
            with st.spinner("Processing PDF on server..."):
                try:
                    response = requests.post(
                        f"{url}/document",
                        files={
                            "file": (
                                document.name,
                                document.getvalue(),
                                "application/pdf"
                            )
                        },
                        data={
                            "thread_id": st.session_state.thread_id
                        }
                    )
                    if response.status_code == 200:
                        st.success("Uploaded & Processed Successfully!")
                    else:
                        st.error(f"Upload failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {str(e)}")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask ClauseGuard..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{url}/invoke",
                    json={
                        "user_msg": prompt,
                        "thread_id": st.session_state.thread_id
                    }
                )

                if response.status_code == 200:
                    answer = response.json().get("message", "No response content received.")
                else:
                    answer = f"Backend Error ({response.status_code}): {response.text}"

            except Exception as e:
                answer = f"Connection Error: {str(e)}"

            st.markdown(answer)

    
    st.session_state.messages.append({"role": "assistant", "content": answer})