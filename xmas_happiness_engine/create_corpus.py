# Modules paths
from xmas_happiness_engine.tmp.outloc import TMPLOC
from xmas_happiness_engine.nltk_data.outloc import NLTKLOC
# Packages
import gensim
import nltk
from nltk.corpus import brown

# Changing nltk data_path
nltk.data.path = [NLTKLOC]

# Training v2v on the brown corpus
sentences = brown.sents()
model = gensim.models.Word2Vec(sentences, min_count=1, size=100, workers=4) # words with freq < min_count are ignored / size of the NN layers / workers for training parallelization
model.save(TMPLOC+'/brown_model.v2v')