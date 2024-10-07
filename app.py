import streamlit as st
from src.doc import DocumentAnalyzer


headline = st.title("Prose analyzer")
uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])
updloaded_file_content = uploaded_file.read()
button = st.button("Analyze")
progress_bar = st.progress(0)

if button:
    da = DocumentAnalyzer("data/aresin_doc.docx", top_n=10)
    (
        average_word_length, 
        average_sent_length, 
        average_para_length, 
        median_word_length, 
        median_sent_length, 
        median_para_length
    ) = da.get_basic_stats()
    progress_bar.progress(30)

    top_most_used, top_least_used = da.get_top_n_most_and_least_used()
    progress_bar.progress(50)
    shortest_sentence, longest_sentence, shortest_word, longest_word = da.get_outliers()
    progress_bar.progress(80)
    fk_grade, fk_description = da._get_flesch_kincaid_eval()
    progress_bar.progress(100)

    metadata_tab, stats_tab, dist_tab, text_tab, quality_tab, content_tab = st.tabs([
        "Metadata",
        "Basic Statistics",
        "Distributions",
        "Text Insights",
        "Text Quality",
        "Content"
    ])

    with metadata_tab:
        author = st.container()

    with stats_tab:
        num_col_1, num_col_2, num_col_3, num_col_4, num_col_5 = st.columns(5)
        num_col_6, num_col_7, num_col_8 = st.columns(3)
        num_col_9, num_col_10, num_col_11 = st.columns(3)

    with dist_tab:
        word_plot_col_1, word_plot_col_2 = st.columns(2)
        sent_plot = st.container()

    with text_tab:
        text_col = st.container()

    with quality_tab:
        lexical_col = st.container()
        st.divider()
        flesh_kincaid_col = st.container()

    with content_tab:
        content_col = st.container()

    author.metric("Author", da.author)
    num_col_1.metric("Characters", da.len_text)
    num_col_2.metric("Characters (no spaces)", da.len_text_without_spaces)
    num_col_3.metric("Words", da.num_words)
    num_col_4.metric("Sentences", da.num_sentences)
    num_col_5.metric("Paragraphs", len(da.data))
    num_col_6.metric("Mean word length", average_word_length)
    num_col_7.metric("Mean sentence length", average_sent_length)
    num_col_8.metric("Mean paragraph length", average_para_length)
    num_col_9.metric("Median word length", median_word_length)
    num_col_10.metric("Median sentence length", median_sent_length)
    num_col_11.metric("Median paragraph length", median_para_length)

    da.plot_word_frequency(word_plot_col_1, title="Most used words without stopwords", stopwords_removed=True, reverse=False)
    da.plot_word_frequency(word_plot_col_2, title="Least used words", stopwords_removed=True, reverse=True)
    da.plot_sentence_length(da.len_sentences, sent_plot, title="Sentence length analysis", xlabel="Sentence length distribution")
    da.plot_sentence_length(da.len_words, sent_plot, title="Word length", xlabel="Word length distribution")

    text_col.subheader("Shortest sentence")
    text_col.write(shortest_sentence)
    text_col.subheader("Longest sentence")
    text_col.write(longest_sentence)
    text_col.subheader("Shortest word")
    text_col.write(shortest_word)
    text_col.subheader("Longest word")
    text_col.write(longest_word)

    lexical_col.metric("Lexical richness", da.lexical_richness)
    lexical_col.write("Lexical richness measures the number of unique words compared to the number of all words. A value closer to 1.0 indicates high lexical variety.")
    flesh_kincaid_col.metric("Flesch-Kincaid score", da.flesch_kincaid)
    flesh_kincaid_col.markdown(f"**{fk_grade}**: {fk_description}")
    flesh_kincaid_col.latex(r'''\text{Flesch-Kincaid Score} = 206.835 - 1.015 \left( \frac{\text{total words}}{\text{total sentences}} \right) - 84.6 \left( \frac{\text{total syllables}}{\text{total words}} \right)''')
    
    content_col.write(f"{len(da.chapters_dict)} chapters.")
    for chapter, length in zip(list(da.chapters_dict.keys()), list(da.chapters_len.values())):
        content_col.markdown(f"- {chapter} ({length} words)")
