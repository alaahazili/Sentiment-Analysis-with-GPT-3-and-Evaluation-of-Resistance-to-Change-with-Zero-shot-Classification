import streamlit as st
from transformers import pipeline
import pandas as pd
import cleantext
import openai

# Clé API OpenAI
openai.api_key = "YOUR OPENAI KEY"

# Configuration de Streamlit
st.header('Zero-Shot Classification App')

# Initialisation du pipeline de classification Zero-Shot
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

# Définition des axes et des labels
antagonisme_labels = ['conciliant', 'résistant', 'opposant', 'irréconciliant']
synergie_labels = ['engagé', 'coopérant', 'interessé', 'minimaliste', 'indifférent']

# Fonction pour nettoyer un texte
def clean_text(text):
    return cleantext.clean(text, clean_all=False, extra_spaces=True,
                           stopwords=True, lowercase=True, numbers=True, punct=True)

# Fonction pour classer un texte en fonction des axes
def classify_text_with_axes(text):
    output = classifier(text, synergie_labels + antagonisme_labels, multi_label=True)
    
    synergie_scores = [output['scores'][output['labels'].index(label)] for label in synergie_labels]
    antagonisme_scores = [output['scores'][output['labels'].index(label)] for label in antagonisme_labels]
    
    max_synergie_score = max(synergie_scores)
    max_antagonisme_score = max(antagonisme_scores)
    
    max_synergie_label = synergie_labels[synergie_scores.index(max_synergie_score)]
    max_antagonisme_label = antagonisme_labels[antagonisme_scores.index(max_antagonisme_score)]
    
    result_score = ""
    if max_synergie_label in ['interessé', 'minimaliste', 'indifférent'] and max_antagonisme_label in ['conciliant', 'résistant']:
        result_score = "Passifs"
    elif max_synergie_label in ['minimaliste', 'indifférent'] and max_antagonisme_label in ['opposant']:
        result_score = "Opposants"
    elif max_synergie_label in ['coopérant', 'interessé'] and max_antagonisme_label in ['opposant', 'irréconciliant']:
        result_score = "Partagés"
    elif max_synergie_label in ['engagé', 'coopérant'] and max_antagonisme_label in ['conciliant', 'résistant']:
        result_score = "Pionniers"
    
    return max_synergie_label, max_antagonisme_label, result_score

# Analyse du texte
with st.expander('Analyze Text'):
    sequence_to_classify = st.text_input('Enter the text to classify:')

    if st.button('Clean Text'):
        cleaned_text = clean_text(sequence_to_classify)
        st.write('Cleaned Text:', cleaned_text)

    if st.button('Classify Text'):
        if sequence_to_classify.strip():  # Vérification que le texte n'est pas vide
            max_synergie_label, max_antagonisme_label, result_score = classify_text_with_axes(sequence_to_classify)
            st.subheader('Zero-Shot Classification Results:')
            st.write(f"Synergie Label : {max_synergie_label}")
            st.write(f"Antagonisme Label : {max_antagonisme_label}")
            st.write(f"Classification Result: {result_score}")
        else:
            st.warning('Enter the text to classify.')

# Analyse CSV
with st.expander('Analyze CSV'):
    uploaded_csv = st.file_uploader('Upload CSV File', type=['csv', 'txt'])
    
    if uploaded_csv is not None:
        try:
            df = pd.read_csv(uploaded_csv)
            
            # Identifier les colonnes contenant "Avis"
            avis_columns = [col for col in df.columns if 'Avis' in col]

            # Analyser chaque avis
            for col in avis_columns:
                df[f'Cleaned {col}'] = df[col].apply(clean_text)
                classification_results = df[f'Cleaned {col}'].apply(classify_text_with_axes)
                df[[f'{col} Synergie_Label', f'{col} Antagonisme_Label', f'{col} Classification_Label']] = pd.DataFrame(classification_results.tolist(), index=df.index)
            
            # Afficher les résultats bien analysés
            st.subheader('Table 1: Well-Analyzed Results')
            st.write(df)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV of Well-Analyzed Results",
                data=csv_data,
                file_name='csv_analysis_results.csv',
                mime='text/csv'
            )

            # Calculer la classification dominante pour chaque projet
            dominant_classifications = []
            for col in avis_columns:
                dominant_classification = df[f'{col} Classification_Label'].value_counts().idxmax()
                dominant_classifications.append((col, dominant_classification))
            
            # Créer un dataframe pour les résultats bien résumés
            df_summary = pd.DataFrame(dominant_classifications, columns=['Projet', 'Classification Dominante'])

            # Afficher les résultats bien résumés
            st.subheader('Table 2: Summarized Results')
            st.write(df_summary)
            csv_data_summary = df_summary.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV of Summarized Results",
                data=csv_data_summary,
                file_name='csv_summary_results.csv',
                mime='text/csv'
            )

        except pd.errors.ParserError as e:
            st.error("Erreur lors de l'analyse du fichier CSV : Le fichier contient des lignes mal formées ou des erreurs de format.")
        except Exception as e:
            st.error(f"Une erreur inattendue s'est produite : {str(e)}")

# Analyse Audio
with st.expander('Analyze Audio'):
    audio_file = st.file_uploader('Upload Audio File:', type=['mp3', 'wav', 'ogg', 'flac'])
    
    if audio_file is not None:
        try:
            # Transcrire le fichier audio
            transcribed_text = openai.Audio.transcribe(model='whisper-1', file=audio_file)['text']
            cleaned_transcribed_text = clean_text(transcribed_text)
            classification_output_audio = classify_text_with_axes(cleaned_transcribed_text)
            
            df_audio = pd.DataFrame({
                'Contenu Audio': [transcribed_text],
                'Contenu Audio Nettoyé': [cleaned_transcribed_text],
                'Synergie_Label': [classification_output_audio[0]],
                'Antagonisme_Label': [classification_output_audio[1]],
                'Classification_Label': [classification_output_audio[2]]
            })

            st.write(df_audio)
            csv_data_audio = df_audio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV of Audio Analysis",
                data=csv_data_audio,
                file_name='audio_analysis_results.csv',
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"An error occurred during audio analysis: {str(e)}")
