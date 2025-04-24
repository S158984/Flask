import os
import streamlit as st
import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import classification_report

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')

#removing Not , nor, no like words from stopwords
custom_stopwords = set(stopwords.words('english')) - {'not', "n't", 'no', 'nor', 'never'}

# Custom tokenizer classes
class LemmaTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.stop_words = set(custom_stopwords)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self._lemmatize_text)

    def _lemmatize_text(self, text):
        tokens = nltk.wordpunct_tokenize(re.sub(r"[^a-zA-Z]", " ", text.lower()))
        review = [self.wnl.lemmatize(token) for token in tokens if token not in self.stop_words]
        return ' '.join(review)

class StemTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self._stem_text)

    def _stem_text(self, text):
        tokens = wordpunct_tokenize(re.sub(r"[^a-zA-Z]", " ", text.lower()))
        review = [self.stemmer.stem(token) for token in tokens if token not in self.stop_words]
        return ' '.join(review)

# Sample data for sentiment analysis
data = {
    'feedback': [
        'The service was excellent and quick!',
        'I am not happy with the delay.',
        'It was okay, nothing special.',
        'Terrible experience, I want a refund!',
        'I love how friendly the staff were.',
        'Customer support was unhelpful and rude.',
        'I had a great experience with the service.',
        'Mediocre service, could be better.',
        'The staff were indifferent.',
        'Everything went smoothly, very satisfied.'
    ],
    'label': ['Positive', 'Negative', 'Neutral', 'Negative', 'Positive', 'Negative', 'Positive', 'Neutral', 'Neutral', 'Positive']
}
os.getcwd()
os.chdir('f:\\MLProject\\Flask\\')
Airline=pd.read_csv('BA_AirlineReviews.csv')
print('df length is', len(Airline))
#df = pd.DataFrame(data)
df=Airline[['ReviewBody']]
print(df.head())
y=Airline['Recommended']
# Sidebar for tokenizer choice
use_stemming = st.sidebar.radio("Choose preprocessing method:", ["Lemmatization", "Stemming"])

preprocessor = StemTokenizer() if use_stemming == "Stemming" else LemmaTokenizer()
print('df length is', len(df))
print('df shape is', df.shape)
df['processed_feedback'] = preprocessor.transform(df['ReviewBody'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['processed_feedback'], y, test_size=0.2, random_state=42)

# Pipeline with TF-IDF and Logistic Regression
model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', LogisticRegression(solver='liblinear'))
])

model.fit(X_train, y_train)

# Streamlit UI
st.title("Sentiment Analysis App")
print(("Classify customer feedback as Positive, Negative, or Neutral."))
st.write("Classify customer feedback as Positive, Negative, or Neutral.")

user_input = st.text_area("Feedback Input", "Type here...")

if st.button("Classify"):
    processed_input = preprocessor._stem_text(user_input) if use_stemming == "Stemming" else preprocessor._lemmatize_text(user_input)
    prediction = model.predict([processed_input])[0]
    st.subheader("Prediction:")
    st.write(f"**{prediction}**")

# Show sample data
if st.checkbox("Show sample training data"):
    st.dataframe(df[['feedback', 'label']])

# Show model performance
if st.checkbox("Show model performance on test data"):
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=False)
    print('model is prepared')
    st.text("Classification Report:")
    st.text(report)
