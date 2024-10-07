import numpy as np
import plotly.express as px
from src.input.parse import TextParser
from nltk.tokenize import word_tokenize, sent_tokenize
import streamlit as st


class TextStats:
    def __init__(self, parser:TextParser, top_n:int=10):
        self.parser = parser
        self.top_n = top_n
        self.length_of_words = [len(word) for word in self.parser.words]
        self.length_of_sentences = [len(word_tokenize(sent)) for sent in self.parser.sentences]
        self.length_of_paragraphs = [len(word_tokenize(para)) for para in self.parser.text]
        self.top_used, self.least_used = self.get_top_n_most_and_least_used()

    def get_basic_stats(self):
        average_word_length = round(float(np.mean(self.length_of_words)),1)
        average_sent_length = round(float(np.mean(self.length_of_sentences)),1)
        average_para_length = round(float(np.mean(self.length_of_paragraphs)),1)
        median_word_length = round(float(np.median(self.length_of_words)),1)
        median_sent_length = round(float(np.median(self.length_of_sentences)),1)
        median_para_length = round(float(np.median(self.length_of_paragraphs)),1)
        return (
            average_word_length, 
            average_sent_length, 
            average_para_length, 
            median_word_length, 
            median_sent_length, 
            median_para_length
            )

    def get_top_n_most_and_least_used(self):
        word_dict_without_stopwords = self.parser.word_dict_without_stopwords
        top_most_used = [
            key for key, _ in word_dict_without_stopwords.items()
        ][:self.top_n]
        top_least_used = [
            key for key, _ in word_dict_without_stopwords.items()
        ][-self.top_n:]
        return top_most_used, top_least_used
    
    def plot_word_frequency(self, streamlit_container, title, reverse=False):
        sorted_word_freq = self.parser.word_dict_without_stopwords
        words = list(sorted_word_freq.keys())
        frequencies = list(sorted_word_freq.values())
        top_frequency = max(frequencies)
        if reverse:
            words = words[::-1][:self.top_n]
            frequencies = frequencies[::-1][:self.top_n]
        else:
            words = words[:self.top_n]
            frequencies = frequencies[:self.top_n]
        fig = px.bar(
            x=words, 
            y=frequencies, 
            labels={'x': 'Words', 'y': 'Frequency'}, 
            title=title,
            )
        fig.update_yaxes(range=[0, top_frequency])
        streamlit_container.plotly_chart(fig)
        
