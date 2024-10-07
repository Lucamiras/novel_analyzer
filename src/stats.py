import numpy as np
import plotly.express as px
from src.parse import TextParser
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
        self.lexical_richness = self.get_lexical_richness()
        self.flesch_kincaid = self.get_flesch_kincaid_score()
        self.flesch_kincaid_grade, self.flesch_kincaid_desc = self.get_flesch_kincaid_eval()

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
        
    def get_longest_shortest_word(self):
        longest_word = max(self.parser.word_dict_without_stopwords, key=len)
        shortest_word = min(self.parser.word_dict_without_stopwords, key=len)
        return longest_word, shortest_word
    
    def get_longest_shortest_sentence(self):
        longest_sentence = max(self.parser.sentences, key=lambda x: len(word_tokenize(x)))
        shortest_sentence = min(self.parser.sentences, key=lambda x: len(word_tokenize(x)))
        return longest_sentence, shortest_sentence
    
    def get_lexical_richness(self):
        num_unique_words = len([value for value in self.parser.word_dict.values() if value == 1])
        num_total_words = len(self.parser.word_dict)
        return np.round(num_unique_words/num_total_words,2)
    
    def get_flesch_kincaid_score(self):
        return float(
            np.round(
                206.835 - (1.015 * (self.parser.num_words / self.parser.num_sentences)) - (84.6 * (self.parser.num_syllables / self.parser.num_words)),
                1)
            )
    
    def get_flesch_kincaid_eval(self):
        scale = [
            (range(90, 101), "5th grade", "Very easy to read. Easily understood by an average 11-year-old student."),
            (range(80, 90), "6th grade", "Easy to read. Conversational English for consumers."),
            (range(70, 80), "7th grade", "Fairly easy to read."),
            (range(60, 70), "8th & 9th grade", "Plain English. Easily understood by 13- to 15-year-old students."),
            (range(50, 60), "10th to 12th", "Fairly difficult to read."),
            (range(30, 50), "College", "Difficult to read."),
            (range(10, 30), "College graduate", "Very difficult to read. Best understood by university graduates."),
            (range(0, 10), "Professional", "Extremely difficult to read. Best understood by university graduates.")
        ]
        score = int(np.round(self.flesch_kincaid, 0))
        for sub_range, grade, description in scale:
            if score in sub_range:
                return grade, description
