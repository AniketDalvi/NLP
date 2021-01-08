import numpy as np
import gensim

def lda(vocabulary, beta, alpha, xi, printFlag = True):
    num_words = np.random.poisson(xi)
    dirichlet = np.random.dirichlet(alpha)
    num_topics = len(alpha)
    if (printFlag):
        print("Num of Words: {}".format(num_words))
        print("Topic Distribution: {}".format(dirichlet))
    document = []
    for _ in range(num_words):
        topic = np.random.choice(num_topics, p=dirichlet)
        word_dist = beta[topic]
        word = np.random.choice(vocabulary, p=word_dist)
        document.append(word)
    return document

vocabulary = ['bass', 'pike', 'deep', 'tuba', 'horn', 'catapult']
beta = np.array([
[0.4, 0.4, 0.2, 0.0, 0.0, 0.0],
[0.0, 0.3, 0.1, 0.0, 0.3, 0.3],
[0.3, 0.0, 0.2, 0.3, 0.2, 0.0]
])
alpha = np.array([1, 3, 8])
xi = 50
document = lda(vocabulary, beta, alpha, xi)
print("Document for Q1: " + (" ".join(document)).strip())