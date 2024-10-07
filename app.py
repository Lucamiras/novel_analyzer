import streamlit as st
from src.input.parse import DocumentLoader, TextParser
from src.analyze.stats import TextStats

# Config
st.set_page_config(
    page_title="Novelizer",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Initialize the session state.
# This is important because the script reruns each time a button is clicked or a selection is made.
# This code allows the app to remember the state of the variables.
st.session_state.is_loaded = st.session_state.get('is_loaded', False)
st.session_state['chapters_and_text'] = st.session_state.get('chapters_and_text', None)
st.session_state['exclusion_list'] = st.session_state.get('exclusion_list', [])
st.session_state['top_n'] = st.session_state.get('top_n', 10)

# Basic structure of the app
st.title("Novel analyzer")
button = st.button("Start uploader")
select_box = st.empty()
tab_container = st.empty()

# SIDEBAR
sidebar = st.sidebar

# Logic for the app
if button:
    with st.spinner("Loading document..."):
        doc = DocumentLoader("data/aresin_doc.docx")
    chapters_and_text = doc.chapters
    chapters_and_text['Full text'] = doc.text
    st.session_state['chapters_and_text'] = chapters_and_text
    st.session_state.is_loaded = True # Setting this to True means it will only run once, unless the button is clicked again.

if st.session_state.is_loaded:
    option = select_box.selectbox("Select a chapter", list(st.session_state['chapters_and_text'].keys()))
    if option:
        parser = TextParser(st.session_state['chapters_and_text'][option], st.session_state['exclusion_list'])
        print(list(parser.word_dict_without_stopwords.keys())[:10])
        print(st.session_state['exclusion_list'])
        text_stats = TextStats(parser, st.session_state['top_n'])
        stats, quality, content = tab_container.tabs(["Stats", "Quality", "Content"])
        
        # STATS TAB
        statcol1, statcol2, statcol3 = stats.columns(3)
        statcol4, statcol5, statcol6 = stats.columns(3)
        stats_container = stats.container()
        plot_col1, plot_col2 = stats.columns(2)
        word_freq_container = stats.empty()
        statcol1.metric("Number of sentences", parser.num_sentences)
        statcol2.metric("Number of words", parser.num_words)
        statcol3.metric("Number of characters (no spaces)", parser.chars_no_spaces)
        statcol4.metric("Average sentence length (in words)", text_stats.get_basic_stats()[1])
        statcol5.metric("Average word length (in chars)", text_stats.get_basic_stats()[0])
        text_stats.plot_word_frequency(plot_col1, title="Most frequent words", reverse=False)
        text_stats.plot_word_frequency(plot_col2, title="Least frequent words", reverse=True)
        stats_container.write("## Word frequency")
        word_freq_container.dataframe(parser.word_dict_without_stopwords)
        # quality tab

        # content tab


with sidebar:
    sidebar.header("Settings")
    if st.session_state.is_loaded:
        
        # EXCLUDE
        sidebar.subheader("Exclude words")
        exclusion_text = sidebar.text_area("Add words, separated by commas, to exclude from the analysis.", placeholder="e.g. the, and, but")
        
        # TOP N
        sidebar.subheader("Number of words to plot")
        top_n_input = sidebar.number_input("Number of words to display in the frequency plots", min_value=1, max_value=100, value=10)
        
        # BUTTONS
        sidebar.divider()
        button_col1, button_col2 = sidebar.columns(2)
        update_button = button_col1.button("Update")
        reset_button = button_col2.button("Reset")
        
        # LOGIC
        if update_button:
            st.session_state['exclusion_list'] = [word.lower().strip() for word in exclusion_text.split(',')]
            st.session_state['top_n'] = top_n_input
            st.rerun()
        if reset_button:
            st.session_state['exclusion_list'] = []
            st.session_state['top_n'] = 10
            st.rerun()
    else:
        sidebar.write("Please load a document first.")
        
