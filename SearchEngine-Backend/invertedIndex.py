import re
from functools import reduce

import nltk
nltk.download('wordnet')
from nltk.stem.snowball import SnowballStemmer
lemma = nltk.wordnet.WordNetLemmatizer()

_STOP_WORDS = frozenset([
'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although',
'always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another',
'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',
'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been',
'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can',
'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even',
'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',
'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here',
'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc',
'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last',
'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me',
'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some',
'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their',
'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
'yourselves', 'the'])


def stopwords_stemming(words):
    stemmer = SnowballStemmer("english")

    new_words = []
    index = 0
    for word in words:
        if  len(word) > 2 and word not in _STOP_WORDS:
            new_words.append((index,stemmer.stem(lemma.lemmatize(word))))
            index+=1
    return new_words

def normalize(words):
    normalizedList = []
    for index, word in words:
        normalizedWord = word.lower()
        normalizedList.append((index,normalizedWord))
    return normalizedList


def words_preprocess(Paragraph):
    words = re.split("\W+", Paragraph)
    words = stopwords_stemming(words)
    words = normalize(words)
    return words

def inverted_index(text):
    inverted = {}
    for index, word in words_preprocess(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)
    return inverted

def inverted_index_add(inverted, doc_id, doc_index):
    for word, locations in doc_index.items():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted

def search(inverted, query):
    words = [word for _, word in words_preprocess(query) if word in inverted]
    results = [set(inverted[word].keys()) for word in words]
    return reduce(lambda x, y: x & y, results) if results else []


if __name__ == "__main__":
    document_1 = "I love watching movies when it's cold outside"
    document_2 = "Toy Story is the best animation movie ever, I love it!"
    document_3 = "Watching horror movies alone at night is really scary"
    document_4 = "He loves to watch films filled with suspense and unexpected plot twists"
    document_5 = "My mom loves to watch movies. My dad hates movie theaters. My brothers like any kind of movie. And I haven't watched a single movie since I got into college"
    inverted = {}
    inverted_documents = {0: document_1, 1: document_2,2: document_3,3: document_4, 4: document_5}
    for doc_id, text in inverted_documents.items():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

    # Print Inverted-Index
    for word, doc_locations in inverted.items():
        print (word, doc_locations)


    # Search something and print results

    result_docs = search(inverted, "single")
    print (list(result_docs)[0])
    print(type(result_docs))
