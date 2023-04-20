import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.read_csv('toxic-dataset.csv').loc[:,['comment_text','toxic']]

df_negative = df.loc[df['toxic'] == 1]
df_positive = df.loc[df['toxic'] == 0][0:df_negative.shape[0]]

df_selected = pd.concat([df_positive,df_negative])

X_train, X_test, y_train, y_test = train_test_split(df_selected['comment_text'], df_selected['toxic'], train_size=0.7)

classificador = Pipeline([
                        ('meu_vetorizador', CountVectorizer(stop_words='english')),
                        ('meu_classificador', LogisticRegression(penalty='l2', #l2 para minimizar pesos
                                                                 solver='saga', max_iter=10000))
                        ])

classificador.fit(X_train,y_train)

joblib.dump(classificador, 'aps3_model.joblib')