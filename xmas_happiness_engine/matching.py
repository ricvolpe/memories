# Modules paths
from xmas_happiness_engine.data_input.O.outloc import OUTLOC
from xmas_happiness_engine.tmp.outloc import TMPLOC
from xmas_happiness_engine.nltk_data.outloc import NLTKLOC
# Packages
import pickle
import gensim
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Changing nltk data_path
nltk.data.path = [NLTKLOC]
stop_words = set(stopwords.words("english"))

# Loading components
timely_message_df = pickle.load(open((OUTLOC+'/messages_tokenized.pd'), 'rb'))
brown_model = gensim.models.Word2Vec.load(TMPLOC+'/brown_model_trained.v2v')

def sentence_similarity(sent_a, sent_b, model):

    sents_similarity = 0
    no_matches = 0
    for word_a in sent_a:
        for word_b in sent_b:
            sents_similarity += model.similarity(word_a, word_b)
            no_matches += 1

    if no_matches > 0: similarity = sents_similarity / no_matches
    else: similarity = 0

    return similarity

def most_similar_sentence(user_input, sentences_df, model):

    user_sentence = word_tokenize(user_input)
    user_sentence = [word.lower() for word in user_sentence if word and word.isalpha() and word not in stop_words]
    model.build_vocab([user_sentence], update=True)
    model.train([user_sentence], total_examples=1, epochs=brown_model.iter)

    similarities = []
    for index, row in sentences_df.iterrows():

        sent = row['token']
        common = [w for w in set(sent + user_sentence) if w in sent and w in user_sentence]

        if len(sent) > 1 and row['eng'] == 1:
            score = sentence_similarity(user_sentence, sent, model)
        else:
            score = 0

        similarity = len(common) + score
        similarities.append((index, similarity))

    similarities.sort(key=lambda tup: tup[1], reverse=True)  # sorts in place

    return similarities[0][0]

def tought_to_memory(user_sentence):

    match = most_similar_sentence(user_sentence, timely_message_df, brown_model)
    chosen_clock = timely_message_df.loc[match,'clock']
    memory = timely_message_df[timely_message_df['clock']==chosen_clock]

    return memory