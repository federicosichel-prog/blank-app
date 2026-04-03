import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Federico Health Coach", layout="centered")

with st.sidebar:
    st.title("⚙️ Setup")
    api_key = st.text_input("Inserisci OpenAI API Key", type="password")
    st.divider()
    st.markdown("### 📋 Parametri Medici\n- **Acido Urico:** 8.1\n- **LDL:** 205\n- **Proteine:** 120g")

if not api_key:
    st.warning("⚠️ Incolla la tua API Key nella barra laterale per iniziare.")
else:
    client = OpenAI(api_key=api_key)
    st.title("💪 Federico AI Coach")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "Sei il coach di Federico. Parametri: Acido Urico 8.1, LDL 205, Massa magra 66.5kg, Target Proteine 120g. No carne rossa. Se peso > 92kg no corsa per ginocchio."}]

    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Chiedi al coach..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            resp = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
            answer = resp.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
