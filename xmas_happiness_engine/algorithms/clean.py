# Modules paths
import datetime
import logging
import re

import nltk
# Packages
import pandas as pd
from xmas_happiness_engine.algorithms.lang import detect_language
from xmas_happiness_engine.data_input.O.outloc import OUTLOC
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer

from xmas_happiness_engine.nltk_data.outloc import NLTKLOC

# Changing nltk data_path
nltk.data.path = [NLTKLOC]
stop_words = set(stopwords.words("english"))
punctuation = RegexpTokenizer(r'\w+')

# Logging configurations
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Reading dataframes
message_df = pd.read_pickle((OUTLOC+'/messages.pd'))

def remove_special_charaters(text):
    faces = "☺️😊😁😂😝😓😳☺️😌😌☺️☺️😘🌞😊😚😉😝😒😈😱😅💩😔😀🤔😶😐😑😯😦😧😮😲😵💛😍🏋😢😝😝😝😝🐱😴💗🙃💭🤓😳😚❤️😝😗😏"
    for char in text:
        if ord(char) not in [ord(face) for face in faces] and ord(char) > 127:
            text = text.replace(char,'')
    return text

message_df['message'] = message_df['message'].apply(remove_special_charaters)

timely_message_df = message_df.sort_values(by=['date'], ascending=True)
clock, clocks = 0, []
for index, row in timely_message_df.iterrows():
    try:
        timegap = message_df.loc[index,'date'] - message_df.loc[index - 1,'date']
    except:
        timegap = datetime.timedelta(seconds=0)
    if timegap > datetime.timedelta(minutes=30):
        clock += 1
    clocks.append(clock)
timely_message_df['clock'] = clocks

# memories = []
# Memory = namedtuple('Memory', 'date messages')
# for clock in set(clocks):
#     moment_df = timely_message_df[timely_message_df['clock'] == clock]
#     if len(set(moment_df['author'])) > 1:
#         date = list(moment_df.loc[:,'date'])[0]
#         messages = []
#         position = 0
#         for index, row in moment_df.iterrows():
#             if len(row['message']) > 2 and not row['message'].isspace() and row['message'][:5] != 'Image':
#                 messages.append({'author':row['author'],'message':row['message'], 'position': position})
#                 position += 1
#         memories.append(Memory(date, messages))
#
# for memory in memories[:]:
#     if len(memory.messages) < 2:
#         memories.remove(memory)
#         continue
#     elif sum([len(word_tokenize(msg['message'])) for msg in memory.messages]) / len(memory.messages) < 3:
#         memories.remove(memory)
#         continue

# Convert text to lower-case and strip punctuation/symbols from words
def normalize_text(text):
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    norm_text = text.lower()
    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')
    # Pad punctuation with spaces on both sides
    for char in ['.', '"', ',', '(', ')', '!', '?', ';', ':']:
        norm_text = norm_text.replace(char, ' ' + char + ' ')
    return norm_text


# NLTK preprocessing
tokenized_messages = []
for message in timely_message_df.message:
    temp_text = normalize_text(message)
    tokens = word_tokenize(temp_text)
    words = [word for word in tokens if word not in stop_words and word.isalpha()]
    tokenized_messages.append(words)

timely_message_df['token'] = tokenized_messages
empty = []
langs = []
for index, row in timely_message_df.iterrows():
    lang = detect_language(row['message'])
    if lang == 'english': langs.append(1)
    else: langs.append(0)
    if len(row['token']) == 0:
        empty.append(1)
    else:
        empty.append(0)
timely_message_df['empty'] = empty
timely_message_df['eng'] = langs
timely_message_df = timely_message_df[timely_message_df['empty']==0]
print(timely_message_df.head())
timely_message_df.to_pickle((OUTLOC+'/messages_tokenized.pd'))

# Dumping into Pickle
#with open((OUTLOC + '/memories.pd'), 'wb') as outfile:
#    pickle.dump(memories, outfile)