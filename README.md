# InsightForge

## 🔍 Overview
InsightForge is an intelligent industry analysis platform that combines AI-powered research, use case identification, and resource discovery into a unified workflow. Using a multi-agent approach powered by CrewAI, it delivers comprehensive insights for business strategy and AI implementation opportunities.

## ⭐ Key Features
- **Automated Industry Intelligence**: Deep-dive analysis of industry trends and competitive landscapes
- **AI Opportunity Discovery**: Identification of relevant AI/ML use cases with complexity assessment
- **Resource Compilation**: Curated collection of datasets and implementation resources
- **Interactive Reporting**: Clean, structured outputs through an intuitive Streamlit interface
- **Persistent Storage**: Automated saving of research findings for future reference

## 🏗️ Architecture
### Agent Ecosystem
1. **Industry Research Specialist**
   - Analyzes market dynamics
   - Maps competitive landscapes
   - Identifies strategic focus areas

2. **AI/ML Use Case Analyst**
   - Evaluates implementation opportunities
   - Assesses technical feasibility
   - Determines business impact

3. **Resource Asset Collector**
   - Sources relevant datasets
   - Finds implementation guides
   - Curates learning resources
     
  ![image](https://github.com/user-attachments/assets/e9260649-be22-4b43-9d67-777d690d02cf)

## 🚀 Getting Started
### Prerequisites
```bash
pip install crewai streamlit python-dotenv
```

### Configuration
1. Create `.env` file with required API keys
2. Configure Serper API for web search capabilities
3. Set up resource storage directory

### Running the Application
```bash
streamlit run main.py
```

## 💡 Usage
1. Launch the Streamlit interface
2. Enter target company name
3. Review insights across three dimensions:
   - Industry Analysis
   - AI Use Cases
   - Implementation Resources

## 🛠️ Technical Stack
- **AI Framework**: CrewAI with Gemini 1.5 Flash
- **Interface**: Streamlit
- **Processing**: Sequential multi-agent workflow
- **Output**: Structured JSON with markdown formatting

## 📁 Output Management
- Automated markdown file generation
- Company-specific directory structure
- Timestamped resource compilation

## ⚙️ Error Handling
- Robust directory management
- Graceful error reporting
- User-friendly status updates

## 🎥 Demo Video

   ![Watch Full Demo Video](https://drive.google.com/file/d/1XyZEay2Px6jeH2Bj1TG4VSiPfBEedEGs/view?usp=sharing)
   
To view the demo:

Click the link above

If not already signed in, you may need to sign in to your Google account

The video will open in Google Drive's video player
