import streamlit as st
from src.input.parse import DocumentLoader, TextParser

st.title("Novel analyzer")
st.write("Hello world!")
button = st.button("Start uploader")
selectbox = st.empty()

# Initialize the session state.
# This is important because the script reruns each time a button is clicked or a selection is made.
# This code allows the app to remember the state of the variables.
st.session_state.is_loaded = st.session_state.get('is_loaded', False)
st.session_state['chapter_names'] = st.session_state.get('chapter_names', None)
st.session_state['chapters'] = st.session_state.get('chapters', None)

if button:
    with st.spinner("Loading document..."):
        doc = DocumentLoader("data/aresin_doc.docx")
    st.session_state['chapters'] = doc.chapters
    st.session_state['chapter_names'] = doc.chapter_names
    st.session_state.is_loaded = True # Setting this to True means it will only run once, unless the button is clicked again.

if st.session_state.is_loaded:
    option = selectbox.selectbox("Select a chapter", st.session_state['chapter_names'])
    st.write(option)
    st.write(st.session_state['chapters'][option])

