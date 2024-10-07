import streamlit as st
from src.parse import DocumentLoader, TextParser
from src.stats import TextStats
from src.llm import LiteraryCritic, prompt
from langchain import PromptTemplate


# CONFIG
st.set_page_config(
    page_title="Novelizer",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="expanded")

# Initialize the session state.
# This is important because the script reruns each time a button is clicked or a selection is made.
# This code allows the app to remember the state of the variables.
st.session_state.is_loaded = st.session_state.get('is_loaded', False)
st.session_state['chapters_and_text'] = st.session_state.get('chapters_and_text', None)
st.session_state['exclusion_list'] = st.session_state.get('exclusion_list', [])
st.session_state['top_n'] = st.session_state.get('top_n', 10)

# APP HEADER
st.title("Novel analyzer")
button = st.button("Start uploader")
select_box = st.empty()
tab_container = st.empty()

# SIDEBAR
sidebar = st.sidebar

# APP LOGIC
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
        text_stats = TextStats(parser, st.session_state['top_n'])
        stats, quality, content = tab_container.tabs(["Text statistics", "Lexical analysis", "Deep content analysis"])
        
        # STATS TAB
        statcol1, statcol2, statcol3 = stats.columns(3)
        statcol4, statcol5, statcol6 = stats.columns(3)
        stats_container = stats.container()
        plot_col1, plot_col2 = stats.columns(2)
        sent_stats_container = stats.container()
        word_freq_container = stats.empty()
        statcol1.metric("Number of sentences", parser.num_sentences)
        statcol2.metric("Number of words", parser.num_words)
        statcol3.metric("Number of characters (no spaces)", parser.chars_no_spaces)
        statcol4.metric("Average sentence length (in words)", text_stats.get_basic_stats()[1])
        statcol5.metric("Average word length (in chars)", text_stats.get_basic_stats()[0])
        text_stats.plot_word_frequency(plot_col1, title="Most frequent words", reverse=False)
        text_stats.plot_word_frequency(plot_col2, title="Least frequent words", reverse=True)
        stats_container.write("## Word frequency")
        
        longest_word, shortest_word = text_stats.get_longest_shortest_word()
        longest_sent, shortest_sent = text_stats.get_longest_shortest_sentence()
        sent_stats_container.markdown(f"**Longest word**: {longest_word}")
        sent_stats_container.markdown(f"**Shortest word**: {shortest_word}")
        sent_stats_container.markdown(f"**Longest sentence**: {longest_sent}")
        sent_stats_container.markdown(f"**Shortest sentence**: {shortest_sent}")
        word_freq_container.dataframe(parser.word_dict_without_stopwords)
        
        # QUALITY TAB
        quality.metric("Lexical richness", text_stats.lexical_richness)
        quality.progress(int(text_stats.lexical_richness*100))
        quality.metric("Flesch-Kincaid score", text_stats.flesch_kincaid)
        quality.progress(int(text_stats.flesch_kincaid))
        quality.markdown(f"**Flesch-Kincaid grade**: {text_stats.flesch_kincaid_grade}")
        quality.markdown(f"**Flesch-Kincaid description**: {text_stats.flesch_kincaid_desc}")

        # content tab
        content.write("Literary Agent C. Odradek is analyzing the text. Please wait...")
        lit_ag = LiteraryCritic()
        message = prompt[1][1].format(text=parser.full_text)
        response = lit_ag.llm.invoke(message)
        content.markdown(response.content)

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
        
