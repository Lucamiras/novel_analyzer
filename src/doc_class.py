import streamlit as st
from docx import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import matplotlib.pyplot as plt
import numpy as np


class DocumentAnalyzer:
    def __init__(self, path:str="", top_n:int=10):
        self.path = path
        self.top_n = top_n
        self.stopwords = {
            'english': stopwords.words('english'),
            'german': stopwords.words('german')
        }
        self.doc = Document(self.path)
        self.author = self.doc.core_properties.author
        self.data = [paragraph.text for paragraph in self.doc.paragraphs if paragraph.text != '']
        self.text = ' '.join(self.data)
        self.sent = sent_tokenize(self.text)
        self.word = [word for word in word_tokenize(self.text) if len(word) > 1]
        self.word_dict = self._generate_word_dict()
        self.len_text = len(self.text)
        self.len_text_without_spaces = len(self.text.replace(' ',''))
        self.num_sentences = len(self.sent)
        self.len_sentences = [len(sent) for sent in self.sent]
        self.num_words = len(self.word)
        self.len_words = [len(word) for word in self.word]
    
    def _generate_word_dict(self):
        words_lower = [word.lower() for word in self.word]
        word_dict = {}
        for word in words_lower:
            word_dict[word] = word_dict.get(word, 0) + 1
        word_dict_sorted = {
            key: value for key, value in sorted(word_dict.items(), key=lambda x: x[1], reverse=True) 
        }
        return word_dict_sorted
    
    def _generate_word_dict_without_stopwords(self):
        return {
            key: value for key, value in self.word_dict.items() if key not in self.stopwords['german']
        }
    
    def get_basic_stats(self):
        average_word_length = round(float(np.mean(self.len_words)),1)
        average_sent_length = round(float(np.mean(self.len_sentences)),1)
        average_para_length = round(float(np.mean([len(word_tokenize(para)) for para in self.data])))
        median_word_length = round(float(np.median(self.len_words)),1)
        median_sent_length = round(float(np.median(self.len_sentences)),1)
        median_para_length = round(float(np.median([len(word_tokenize(para)) for para in self.data])))
        return (
            average_word_length, 
            average_sent_length, 
            average_para_length, 
            median_word_length, 
            median_sent_length, 
            median_para_length
            )

    def get_top_n_most_and_least_used(self):
        word_dict_without_stopwords = self._generate_word_dict_without_stopwords()
        top_most_used = [
            key for key in word_dict_without_stopwords.items()
        ][:self.top_n]
        top_least_used = [
            key for key in word_dict_without_stopwords.items()
        ][-self.top_n:]
        return top_most_used, top_least_used