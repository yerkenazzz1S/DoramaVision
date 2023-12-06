import nltk
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DoramaVision.settings")
django.setup()
from nltk.stem import WordNetLemmatizer
from pandas import read_csv
import joblib
from django.conf import settings
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('wordnet')
nltk.download('omw-1.4')

csv_file_path = os.path.join(settings.BASE_DIR, 'dorama_info.csv')  # Replace with the path to your dataset
df = read_csv(csv_file_path)

df['Combined Text'] = df['name'] + ' ' + df['desc'] + ' ' + df['actors'] + ' ' + df['genre'] + ' ' + df['translate']


def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(w) for w in words])


df['Lemmatized Text'] = df['Combined Text'].apply(lemmatize_text)

count_vectorizer = CountVectorizer(stop_words='english')

count_matrix = count_vectorizer.fit_transform(df['Lemmatized Text'])

joblib.dump(count_vectorizer, 'pkl/count_vectorizer_model.pkl')
joblib.dump(count_matrix, 'pkl/count_matrix_model.pkl')
