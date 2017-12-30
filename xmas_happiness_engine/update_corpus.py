# Modules paths
from xmas_happiness_engine.data_input.O.outloc import OUTLOC
from xmas_happiness_engine.tmp.outloc import TMPLOC
# Packages
import pickle
import gensim

# Loading token sentences from clean file
timely_message_df = pickle.load(open((OUTLOC+'/messages_tokenized.pd'), 'rb'))
token_sentences = timely_message_df['token']

# Loading model trained on the brown corpus
brown_model = gensim.models.Word2Vec.load(TMPLOC+'/brown_model.v2v')
brown_model.build_vocab(token_sentences, update=True)
brown_model.train(token_sentences, total_examples=len(token_sentences), epochs=brown_model.iter)
brown_model.save(TMPLOC+'/brown_model_trained.v2v')