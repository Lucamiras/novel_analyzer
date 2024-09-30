import streamlit as st
from docx import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import matplotlib.pyplot as plt
import numpy as np


# Download the stopwords
nltk.download('stopwords')
nltk.download('punkt_tab')
german_stopwords = set(stopwords.words('german'))

def read_data(path):
    doc = Document(path)
    data = [paragraph.text for paragraph in doc.paragraphs]
    return data

def get_basic_stats(data):
    data_text = ''.join(data)
    len_with_spaces = len(data_text)
    len_without_spaces = len(data_text.replace(' ', ''))
    len_words = len([x for x in data_text.split(' ') if x != ' '])
    return len_with_spaces, len_without_spaces, len_words

def get_word_analysis(data):
    data_text = ''.join(data)
    data_text = [x.lower() for x in data_text.split(' ') if len(x) > 1 and x.lower()]
    data_dict = {}
    for word in data_text:
        data_dict[word] = data_dict.get(word, 0) + 1
    return {key:value for key, value in sorted(data_dict.items(), key=lambda item: item[1], reverse=True)}

def get_unique_words_ratio(data_dict):
    number_unique_words = len([value for value in data_dict.values() if value == 1])
    return np.round(number_unique_words / len(data_dict), 2)

def plot_word_frequency(data_dict, container, title):
    top_words = list(data_dict.items())[:10]
    words, frequencies = zip(*top_words)
    plt.figure(figsize=(5, 5))
    plt.bar(words, frequencies)
    plt.xlabel('Words')
    plt.ylabel('Frequencies')
    plt.title(title)
    plt.xticks(rotation=45)
    container.pyplot(plt)

def plot_sentence_length(X, container, title):
    plt.figure(figsize=(10, 5))
    plt.boxplot(X, vert=False)
    plt.xlabel('Sentence length')
    plt.title(title)
    container.pyplot(plt)

def get_sentence_length(data):
    sent_tokenizer = sent_tokenize(' '.join(data), language='german')
    sentences_by_length = sorted(sent_tokenizer, key=lambda x: len(word_tokenize(x)))
    sentence_lengths = [len(word_tokenize(sentence)) for sentence in sent_tokenizer]
    return sentence_lengths, (sentences_by_length[0], sentences_by_length[-1]), (sent_tokenizer[0], sent_tokenizer[-1])

data = read_data(path='data/aresin_doc.docx')
len_with_spaces, len_without_spaces, len_words = get_basic_stats(data)
data_dict = get_word_analysis(data)
data_dict_without_stopwords = {key: value for key, value in data_dict.items() if key not in german_stopwords}
unique_words_ratio = get_unique_words_ratio(data_dict)
sentence_length, (shortest, longest), (first, last) = get_sentence_length(data)

st.header("Text analyzer")
button = st.button('Analyze text')

if button:
    st.subheader("Basic statistics")
    basic_1, basic_2, basic_3 = st.columns(3)
    st.divider()
    plot_1, plot_2 = st.columns(2)
    plot_3 = st.container()
    sent_1 = st.container()
    st.divider()
    st.subheader("Advanced statistics")
    col4_1, col4_2 = st.columns(2)

    basic_1.metric("Character count with spaces", len_with_spaces)
    basic_2.metric("Character count without spaces", len_without_spaces)
    basic_3.metric("Word count", len_words)
    plot_word_frequency(data_dict, plot_1, "Word frequency")
    plot_word_frequency(data_dict_without_stopwords, plot_2, "Word frequency without stopwords")
    plot_sentence_length(sentence_length, plot_3, "Sentence length")
    sent_1.subheader("Shortest sentence")
    sent_1.write(shortest)
    sent_1.subheader("Longest sentence")
    sent_1.write(longest)
    sent_1.subheader("First sentence")
    sent_1.write(first)
    sent_1.subheader("Last sentence")
    sent_1.write(last)
    col4_1.metric("Lexical richness", unique_words_ratio)
    col4_1.write("The lexical richness is the ratio of unique words to the total number of words in the text. A ratio closer to 1.0 indicates a more diverse vocabulary.")