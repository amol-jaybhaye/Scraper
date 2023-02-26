from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import validators
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import itertools
#nltk imports
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string


@login_required(login_url='signin')
def Index(request):
     return render(request, 'index.html')

@login_required(login_url='signin')
def Result(request):
     context = {}
     url = request.POST.get("url")

     if validators.url(str(url)):
          data = requests.get(str(url))
          soup = BeautifulSoup(data.text, 'html.parser')
          gi_obj = Get_Insides(soup.get_text())
          context = {
               'do_url' : url[:50],
               'do_total_world' : gi_obj.words_total(),
               'do_word_count' : gi_obj.word_count()
               }
     else:
          context = {'do_url' : "Please enter correct url"}
     return render(request, 'result.html', context)

class Get_Insides:
     web_text = ""
     def __init__(self, wt):
          self.web_text = wt
     
     def words_total(self):
          total = len(re.findall(r'\w+', str(self.web_text.split())))
          return total
     
     def word_count(self):
          #creating a dictionary
          w_count = dict()

          #Remove all articles, connector words, etc.
          # r_word = re.sub('(\s+)(a|an|and|the|)(\s+)', '\1\3', self.web_text)
          # w_word = re.findall(r'\w+', str(r_word.split()))

          #tokenizatons
          tokens = word_tokenize(self.web_text.lower())

          #remove stopwords
          stop_words = set(stopwords.words('english'))
          updated_tokens = [token for token in tokens if token not in stop_words]

          # Remove punctuation
          filtered_tokens = [token.translate(str.maketrans('', '', string.punctuation)) for token in updated_tokens]
     
          #adding items in dictionary
          for w in filtered_tokens:
               if w in w_count:
                    w_count[w] += 1
               else:
                    w_count[w] = 1
          
          #creating two different list for keys and values
          w_count_keys = list(w_count.keys())
          w_count_values = list(w_count.values())

          #get index of sorted w_count_values
          sorted_count_index = np.argsort(w_count_values)

          #sorted w_count
          sorted_w_count = {w_count_keys[i]: w_count_values[i] for i in sorted_count_index[::-1]}

          #return top 20 words
          sorted_w_count_tp = dict(itertools.islice(sorted_w_count.items(), 100))

          return sorted_w_count_tp
