# Sentiment Analysis Projects

This repository contains two comprehensive sentiment analysis applications built with Python, offering different approaches to text and multimedia sentiment analysis.

## 📁 Project Structure

```
├── sentiment analysis GPT/          # GPT-powered sentiment analysis
│   ├── finalapp.py                 # Main Streamlit application
│   ├── requirements.txt            # Dependencies
│   ├── output/                     # Output directory
│   └── int/                        # Input files
│
└── Zero Shot Classification/        # Zero-shot classification system
    ├── newappp.py                  # Main Streamlit application
    ├── app.py                      # Flask web application
    ├── requirements.txt            # Dependencies
    ├── templates/                  # HTML templates
    │   └── formulaire.html         # Client feedback form
    ├── output/                     # Output directory
    └── input/                      # Input directory
```

## 🚀 Project 1: GPT-Powered Sentiment Analysis

### Overview
A comprehensive sentiment analysis application that leverages OpenAI's GPT-3.5-turbo for advanced text analysis, combined with TextBlob for polarity and subjectivity scoring. The app also includes image and audio analysis capabilities.

### Features

#### 📝 Text Analysis
- **GPT-3.5 Integration**: Advanced sentiment analysis using OpenAI's language model
- **TextBlob Analysis**: Polarity and subjectivity scoring
- **Text Cleaning**: Comprehensive text preprocessing with cleantext
- **Visual Feedback**: Emoji-based sentiment representation

#### 📊 CSV Analysis
- **Bulk Processing**: Analyze multiple texts from CSV files
- **Automated Cleaning**: Clean all text entries automatically
- **Export Results**: Download analyzed data as CSV

#### 🖼️ Image Analysis
- **DeepFace Integration**: Facial analysis (age, gender, race, emotion)
- **Sentiment Inference**: GPT-based sentiment analysis of image descriptions
- **Comprehensive Results**: Detailed analysis with downloadable reports

#### 🎵 Audio Analysis
- **Speech-to-Text**: OpenAI Whisper integration for audio transcription
- **Sentiment Analysis**: Analyze transcribed audio content
- **Multi-format Support**: MP3, WAV, OGG, FLAC formats

### Installation

1. **Clone the repository**
   ```bash
   git clone <https://github.com/alaahazili/Sentiment-Analysis-with-GPT-3-and-Evaluation-of-Resistance-to-Change-with-Zero-shot-Classification.git>
   cd "sentiment analysis GPT"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**
   - Create a `.streamlit/secrets.toml` file
   - Add your OpenAI API key:
   ```toml
   [openai]
   api_key = "your-openai-api-key-here"
   ```

4. **Run the application**
   ```bash
   streamlit run finalapp.py
   ```

### Usage

1. **Text Analysis**: Enter text in the "Analyze Text" section
2. **CSV Analysis**: Upload a CSV file with a 'tweets' column
3. **Image Analysis**: Upload images for facial and sentiment analysis
4. **Audio Analysis**: Upload audio files for transcription and sentiment analysis

## 🎯 Project 2: Zero-Shot Classification System

### Overview
A sophisticated zero-shot classification system that categorizes text based on predefined axes (Synergie and Antagonisme). The system uses the mDeBERTa-v3 model for multilingual classification and includes both Streamlit and Flask interfaces.

### Features

#### 🧠 Zero-Shot Classification
- **mDeBERTa-v3 Model**: State-of-the-art multilingual classification
- **Dual-Axis Analysis**: Synergie and Antagonisme classification
- **Custom Categories**: 
  - Synergie: engagé, coopérant, interessé, minimaliste, indifférent
  - Antagonisme: conciliant, résistant, opposant, irréconciliant

#### 📊 Classification Results
- **Four Categories**: Pionniers, Partagés, Opposants, Passifs
- **Multi-label Support**: Handle complex text classifications
- **Bulk Processing**: Analyze multiple texts from CSV files

#### 🌐 Web Interface
- **Streamlit App**: Interactive analysis interface
- **Flask Web App**: Client feedback collection system
- **CSV Export**: Download analysis results

#### 🎵 Audio Support
- **Audio Transcription**: OpenAI Whisper integration
- **Audio Classification**: Apply zero-shot classification to transcribed audio

### Installation

1. **Navigate to the project directory**
   ```bash
   cd "Zero Shot Classification"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**
   - Edit `newappp.py` and replace `"YOUR OPENAI KEY"` with your actual API key
   - Or set up environment variables

4. **Run the applications**

   **Streamlit App (Main Analysis Tool):**
   ```bash
   streamlit run newappp.py
   ```

   **Flask App (Client Feedback Collection):**
   ```bash
   python app.py
   ```

### Usage

#### Streamlit Application
1. **Text Analysis**: Enter text and classify using zero-shot approach
2. **CSV Analysis**: Upload CSV files with "Avis" columns
3. **Audio Analysis**: Upload audio files for transcription and classification

#### Flask Application
1. **Start the server**: `python app.py`
2. **Access the form**: Navigate to `http://localhost:5000`
3. **Collect feedback**: Submit client opinions for multiple projects
4. **Data storage**: Results saved to `Avis_clients.csv`

## 🔧 Dependencies

### Project 1: GPT-Powered Analysis
- `openai>=1.0.0` - OpenAI API integration
- `streamlit>=1.24.0` - Web application framework
- `textblob>=0.17.1` - Text processing and sentiment analysis
- `pandas>=2.0.0` - Data manipulation
- `cleantext>=1.1.4` - Text cleaning utilities
- `deepface>=0.0.79` - Facial analysis
- `tensorflow>=2.12.0` - Deep learning framework
- `opencv-python>=4.7.0` - Computer vision

### Project 2: Zero-Shot Classification
- `transformers==4.38.2` - Hugging Face transformers
- `torch==2.2.1` - PyTorch deep learning
- `streamlit==1.32.0` - Web application framework
- `flask==3.0.2` - Web framework
- `pandas==2.2.1` - Data manipulation
- `openai==1.12.0` - OpenAI API integration
- `cleantext==1.1.4` - Text cleaning utilities

## 📊 Output Examples

### Sentiment Analysis Results
```
Sentiment: Positive
Polarity: 0.8
Subjectivity: 0.6
Emoji: 😊
```

### Zero-Shot Classification Results
```
Synergie Label: engagé
Antagonisme Label: conciliant
Classification Result: Pionniers
```

## 🎯 Use Cases

### Project 1: GPT-Powered Analysis
- **Social Media Monitoring**: Analyze customer feedback and social media posts
- **Content Analysis**: Evaluate marketing content and product reviews
- **Multimedia Analysis**: Analyze images and audio for sentiment
- **Research**: Academic research in sentiment analysis

### Project 2: Zero-Shot Classification
- **Customer Segmentation**: Classify customer feedback into behavioral categories
- **Market Research**: Analyze survey responses and feedback
- **Content Categorization**: Automatically categorize text content
- **Behavioral Analysis**: Understand user engagement patterns

## 🔒 Security Notes

- **API Keys**: Never commit API keys to version control
- **Data Privacy**: Be mindful of sensitive data in uploaded files
- **Rate Limits**: Respect OpenAI API rate limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational and research purposes. Please ensure compliance with OpenAI's terms of service and other API providers' policies.

## 🆘 Troubleshooting

### Common Issues

1. **OpenAI API Errors**: Check API key configuration and rate limits
2. **Model Loading Issues**: Ensure sufficient RAM for large models
3. **Audio Processing**: Verify audio file formats are supported
4. **CSV Upload Errors**: Check file encoding and column names

### Support

For issues and questions, please check the project documentation or create an issue in the repository.
