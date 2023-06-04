import spacy
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
from nltk.corpus import wordnet

class NLProcessor():
    def __init__(self):
        self.data=pd.read_csv("articles3_reduced.csv").head(100)

    def main_task(self):
        #tokenization
        my_docs_and_tokens=[]

        nlp = spacy.load('en_core_web_sm')
        for index, row in self.data.iterrows():
            content = row['content']

            tokenized=nlp(content.lower())
            # Delete stop-words and lemmatize tokens
            filtered_tokens = [token for token in tokenized if not token.is_stop and re.match(r'\w+', token.text)]
            lemmatized_tokens = [token.lemma_ for token in filtered_tokens]

            my_docs_and_tokens.append(lemmatized_tokens)

        lemmas=pd.DataFrame()
        lemmas['id']=self.data['id']
        lemmas['title'] = self.data['title']
        lemmas['lemmas']=[" ".join(doc_lemmas) for doc_lemmas in my_docs_and_tokens]
        lemmas.to_csv('lemmas.csv',index=False)

        #generate bag of words

        #extract all tokens
        all_tokens=[item for sublist in my_docs_and_tokens for item in sublist]

        vectorizer = CountVectorizer()
        bag_of_words = vectorizer.fit_transform(all_tokens)

        BoW_df=pd.DataFrame()
        BoW_df["word"]=vectorizer.get_feature_names()
        BoW_df["fequencies"]=bag_of_words.toarray().sum(axis=0)
        print(BoW_df.nlargest(10,['fequencies']))
        BoW_df.to_csv("my_BoW.csv",index=False)

        #calculate td-if
        my_docs=[' '.join([token for token in tokens]) for tokens in my_docs_and_tokens]

        top_words_and_tf_idf = {}

        tfidfvectorizer=TfidfVectorizer()
        tfidf_matrix = tfidfvectorizer.fit_transform(my_docs)

        for word in BoW_df.nlargest(10,['fequencies'])['word']:
            word_index = vectorizer.get_feature_names().index(word)
            tfidf_score = tfidf_matrix[:, word_index].toarray().sum()
            top_words_and_tf_idf[word] = tfidf_score

        print('\nTF-IDF metric for top-10 most occuring words:')
        for key,value in top_words_and_tf_idf.items():
            print(f"{key} - {round(value,3)}")

    def doyle_and_poe_comparison(self):
        """additional task number 2"""
        nlp = spacy.load('en_core_web_sm')

        #process doyle text
        stemmer=PorterStemmer()
        doyle=""
        with open("PoAndDoyle/doyle.txt", 'r') as file:
            doyle+=file.read()

        with open("PoAndDoyle/doyle-2.txt", 'r') as file:
            doyle+=file.read()

        print("Finished reading doyle data")
        tokenized_doyle = nlp(doyle.lower())
        print("Finished tokenizating doyle data")

        # Delete stop-words and stem tokens
        stemmed_doyle_tokens = [stemmer.stem(token.text) for token in tokenized_doyle if not token.is_stop and re.match(r'\w+', token.text)]
        print("Finished stemming doyle data")

        # process poe text
        poe = ""
        with open("PoAndDoyle/poe.txt", 'r') as file:
            poe += file.read()

        with open("PoAndDoyle/poe-2.txt", 'r') as file:
            poe += file.read()
        print("Finished reading poe data")

        tokenized_poe = nlp(poe.lower())
        print("Finished tokenizing poe data")

        # Delete stop-words and stem tokens
        stemmed_poe_tokens = [stemmer.stem(token.text) for token in tokenized_poe if
                                not token.is_stop and re.match(r'\w+', token.text)]
        print("Finished stemming poe data")


        # Generate word cloud for doyle
        wordcloud=WordCloud(background_color="white", width=3000, height=3000)
        doyle = wordcloud.generate(" ".join(stemmed_doyle_tokens))

        # Display the word cloud
        plt.imshow(doyle, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        # Generate word cloud for poe
        poe = wordcloud.generate(" ".join(stemmed_poe_tokens))

        # Display the word cloud
        plt.imshow(poe, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        #comaring their gloominess

        def calculate_gloomy_words_occurences(tokens):
            gloomy_synsets = ['despair.n.01',
                              'gloom.n.01',
                              'sadness.n.01',
                              'melancholy.n.01',
                              'depression.n.01',
                              'sorrow.n.01',
                              'desolation.n.01',
                              'misery.n.01',
                              'grief.n.01',
                              'forlornness.n.01',
                              'darkness.n.01',
                              'somberness.n.01',
                              'bleakness.n.01',
                              'despondency.n.01',
                              'dreariness.n.01',
                              'despondence.n.01',
                              'despond.n.01',
                              'moroseness.n.01',
                              'dourness.n.01',
                              'dispiritedness.n.01',
                              'disheartenment.n.01',
                              'disconsolateness.n.01',
                              'desolateness.n.01',
                              'desponding.n.01',
                              'hopelessness.n.01',
                              'lugubriousness.n.01',
                              'glumness.n.01',
                              'downheartedness.n.01',
                              'cheerlessness.n.01',
                              'funerealness.n.01',
                              'solemnity.n.01',
                              'wretchedness.n.01',
                              'low-spiritedness.n.01',
                              'despondingly.n.01',
                              'pensiveness.n.01',
                              'mournfulness.n.01',
                              'dolorousness.n.01',
                              'sorrowfulness.n.01',
                              'despondently.n.01',
                              'downcastness.n.01',
                              'unhappiness.n.01',
                              'disheartenment.n.01',
                              'discouragement.n.01',
                              'gloomily.n.01',
                              'drearily.n.01',
                              'dishearteningness.n.01',
                              'sombreness.n.01',
                              'pessimism.n.01',
                              'lugubriousness.n.01',
                              'joylessness.n.01',
                              'downheartedness.n.01',
                              'dispiritedness.n.01',
                              'dreariness.n.01',
                              'forlornness.n.01',
                              'dejectedness.n.01',
                              'bleakness.n.01',
                              'unhappiness.n.01',
                              'heavyheartedness.n.01',
                              'mournfulness.n.01',
                              'melancholy.n.01',
                              'solemnity.n.01',
                              'dark.n.01',
                              'sadness.n.01',
                              'depression.n.01',
                              'sorrow.n.01',
                              'anguish.n.01',
                              'disconsolation.n.01',
                              'desolation.n.01',
                              'misery.n.01',
                              'grief.n.01',
                              'down.n.01',
                              'darkness.n.01',
                              'somber.n.01',
                              'glum.n.01',
                              'pensive.n.01',
                              'moody.n.01',
                              'desolate.n.01',
                              'downhearted.n.01',
                              'wretched.n.01',
                              'low-spirited.n.01',
                              'melancholic.n.01',
                              'sad.n.01',
                              'blue.n.01',
                              'sombre.n.01',
                              'dreary.n.01',
                              'lugubrious.n.01',
                              'cheerless.n.01',
                              'despondent.n.01',
                              'dejected.n.01',
                              'glumly.n.01',
                              'forlorn.n.01',
                              'mournful.n.01',
                              'somberly.n.01',
                              'joyless.n.01',
                              'dispirited.n.01',
                              'downcast.n.01',
                              'disheartened.n.01',
                              'despairing.n.01',
                              'sorrowful.n.01',
                              'desolate.n.01',
                              'morose.n.01',
                              'bleak.n.01',
                              'morosely.n.01',
                              'mournfully.n.01',
                              'piteously.n.01',
                              'disconsolately.n.01',
                              'inconsolable.n.01',
                              'heartbroken.n.01',
                              'crestfallen.n.01',
                              'disheartened.n.01']  # related to gloominess i guess

            occurences = 0

            for word in tokens:
                if isinstance(word.text, str):
                    synsets = wordnet.synsets(word.text)
                    for synset in synsets:
                        if synset.name() in gloomy_synsets:
                            occurences += 1
                            continue
            return occurences

        doyle_gloominess=calculate_gloomy_words_occurences(tokenized_doyle)
        poe_gloominess=calculate_gloomy_words_occurences(tokenized_poe)
        print(f"\nDoyle gloomy words occurences:\n\t{doyle_gloominess}\nPoe gloomy words occurences:\n\t{poe_gloominess}")
        print('\nThe gloomiest of the two:')
        if(poe_gloominess>doyle_gloominess):
            print("Poe")
        else:
            print("Doyle")