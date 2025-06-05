import openai
import streamlit as st
from textblob import TextBlob
import pandas as pd
import cleantext
from deepface import DeepFace
import os

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

st.header('Sentiment Analysis App')

#analyze text
with st.expander('Analyze Text'):
    text = st.text_input('Enter your text to analyze: ')
    if text:
        try:
            # Use GPT-3 for sentiment analysis
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Sentiment analysis of the following text: '{text}'\n\nSentiment score: ",
                temperature=0,
                max_tokens=10
            )
            sentiment = response.choices[0].text.strip()
        except Exception as e:
            st.error(f"Error during OpenAI API call: {str(e)}")
            sentiment = "Error"

        # Use TextBlob for polarity and subjectivity analysis
        blob = TextBlob(text)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        # Determine the emoji based on sentiment
        if sentiment == "Positive":
            emoji = '😊'
        elif sentiment == "Negative":
            emoji = '😔'
        else:
            emoji = '😐'
        
        st.write('Sentiment: ', sentiment)
        st.write('Polarity: ', polarity)
        st.write('Subjectivity: ', subjectivity)
        st.write('Emoji: ', emoji)

    pre = st.text_input('Enter your text for cleaning: ')
    if pre:
        st.write(cleantext.clean(pre, clean_all=False, extra_spaces=True,
                                 stopwords=True, lowercase=True, numbers=True, punct=True))


def analyze_sentiment(x):

    blob = TextBlob(x)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)

    if polarity >= 0.5:
        sentiment = 'Positive'
        emoji = '😊'
    elif polarity <= -0.5:
        sentiment = 'Negative'
        emoji = '😔'
    else:
        sentiment = 'Neutral'
        emoji = '😐'
    return polarity, subjectivity, sentiment, emoji







#analyze csv
with st.expander('Analyze CSV'):
    upl = st.file_uploader('Upload file')

    if upl:
        df = pd.read_csv(upl)
        df['Polarity'], df['Subjectivity'], df['Sentiment'], df['Emoji'] = zip(*df['tweets'].apply(analyze_sentiment))
        df['Cleaned tweets'] = df['tweets'].apply(lambda x: cleantext.clean(x, clean_all=False, extra_spaces=True,
                                 stopwords=True, lowercase=True, numbers=True, punct=True))

        st.write(df.head(10))

        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='sentiment-result.csv',
            mime='text/csv',
        )









# Analyze Image section
with st.expander('Analyze Image'):
    # Allow the user to upload an image file
    image_file = st.file_uploader('Upload an image:', type=['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    if image_file:
        # Save the uploaded image to a file
        file_path = f'{image_file.name.split(".")[0]}.{image_file.name.split(".")[-1]}'
        with open(file_path, 'wb') as f:
            f.write(image_file.getbuffer())

        # Analyze the image using DeepFace
        analysis_result = DeepFace.analyze(img_path=file_path, actions=['age', 'gender', 'race', 'emotion'])

        # Check if analysis_result is a list (DeepFace should return a list)
        if isinstance(analysis_result, list):
            # Access the first element of the list
            result = analysis_result[0]

            # Display the results of the analysis
            st.write('Age:', result['age'])
            st.write('Gender:', result['dominant_gender'])
            st.write('Race:', result['dominant_race'])
            st.write('Emotion:', result['dominant_emotion'])

            # Describe the image for sentiment analysis
            image_description = (
                f"This image features a {result['dominant_race']} {result['dominant_gender']} person with a "
                f"{result['dominant_emotion']} expression."
            )

            # Perform sentiment analysis using OpenAI GPT-3
            prompt = f"{image_description}\n\nSentiment analysis:"
            response = openai.Completion.create(
                engine='gpt-3.5-turbo-instruct',
                prompt=prompt,
                temperature=0,
                max_tokens=100
            )
            sentiment_analysis = response.choices[0].text.strip().lower()

            # Use TextBlob to calculate polarity and subjectivity
            blob = TextBlob(sentiment_analysis)
            polarity = round(blob.sentiment.polarity, 2)
            subjectivity = round(blob.sentiment.subjectivity, 2)

            # Determine sentiment and emoji based on analysis
            if "positive" in sentiment_analysis:
                sentiment = 'Positive'
                emoji = '😊'
            elif "negative" in sentiment_analysis:
                sentiment = 'Negative'
                emoji = '😔'
            else:
                sentiment = 'Neutral'
                emoji = '😐'

            # Display the sentiment analysis results
            st.write('Sentiment:', sentiment)
            st.write('Emoji:', emoji)
            st.write('Polarity:', polarity)
            st.write('Subjectivity:', subjectivity)

            # Create a dictionary of results
            data = {
                'Name': [os.path.basename(file_path)],
                'Age': [result['age']],
                'Gender': [result['dominant_gender']],
                'Race': [result['dominant_race']],
                'Emotion': [result['dominant_emotion']],
                'Sentiment': [sentiment],
                'Emoji': [emoji],
                'Polarity': [polarity],
                'Subjectivity': [subjectivity]
            }

            # Convert dictionary to DataFrame and display it
            df_image = pd.DataFrame(data)
            st.write(df_image)

            # Allow downloading of CSV file for image analysis results
            csv_image = df_image.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='Download image analysis as CSV',
                data=csv_image,
                file_name='image_analysis.csv',
                mime='text/csv'
            )








# Analyze Audio section
with st.expander('Analyze Audio'):
    # Permettre à l'utilisateur de télécharger un fichier audio
    audio_file = st.file_uploader('Upload an audio file:', type=['mp3', 'wav', 'ogg', 'flac'])
    if audio_file:
        # Transcrire l'audio en utilisant l'API OpenAI
        audio_response = openai.Audio.transcribe(
            model='whisper-1',
            file=audio_file
        )
        transcribed_text = audio_response['text']

        # Effectuer une analyse sentimentale en utilisant GPT-3
        response = openai.Completion.create(
            engine='gpt-3.5-turbo-instruct',
            prompt=f"Sentiment analysis of the following text: '{transcribed_text}'\n\nSentiment score: ",
            temperature=0,
            max_tokens=100
        )
        sentiment_analysis = response.choices[0].text.strip().lower()

        # Utilisez TextBlob pour calculer la polarité et la subjectivité
        blob = TextBlob(sentiment_analysis)
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        # Déterminez le sentiment et l'emoji en fonction de l'analyse
        if "positive" in sentiment_analysis:
            sentiment = 'Positive'
            emoji = '😊'
        elif "negative" in sentiment_analysis:
            sentiment = 'Negative'
            emoji = '😔'
        else:
            sentiment = 'Neutral'
            emoji = '😐'

        # Affichez les résultats de l'analyse sentimentale
        st.write('Transcribed text:', transcribed_text)
        st.write('Sentiment:', sentiment)
        st.write('Emoji:', emoji)
        st.write('Polarity:', polarity)
        st.write('Subjectivity:', subjectivity)

        # Créez un dictionnaire de résultats
        data = {
            'File Name': [audio_file.name],
            'Transcribed Text': [transcribed_text],
            'Sentiment': [sentiment],
            'Emoji': [emoji],
            'Polarity': [polarity],
            'Subjectivity': [subjectivity]
        }

        # Convertissez le dictionnaire en DataFrame et affichez-le
        df_audio = pd.DataFrame(data)
        st.write(df_audio)

        # Permettre le téléchargement du fichier CSV pour les résultats de l'analyse audio
        csv_audio = df_audio.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='Download audio analysis as CSV',
            data=csv_audio,
            file_name='audio_analysis.csv',
            mime='text/csv'
        )
