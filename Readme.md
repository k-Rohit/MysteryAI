# 🕵️‍♂️ MysteryAI - Indian Detective Game

**रहस्यAI** - An AI-powered mystery solving game set across India, where you step into the shoes of a detective and solve compelling mysteries using artificial intelligence.

## 🌟 Features

### 🎮 Interactive Mystery Solving
- **8 Unique Indian Themes**: Mumbai Underworld, Delhi Politics, Bangalore Tech, Kolkata Literary Society, Goa Beach Resorts, Rajasthan Palaces, Kerala Backwaters, and Punjab Farmhouses
- **AI-Generated Cases**: Each mystery is uniquely crafted by AI with rich, atmospheric details
- **Realistic Indian Context**: Authentic Indian names, locations, cultural references, and social dynamics

### 🔍 Investigation Tools
- **Suspect Interrogation**: Question suspects with AI-powered responses that stay in character
- **Evidence Analysis**: Examine physical evidence with detailed forensic analysis
- **Smart Hints System**: Get contextual hints at different difficulty levels (Easy/Medium/Hard)
- **AI Auto-Solve**: Let the AI detective solve the case automatically with step-by-step reasoning

### 🤖 AI-Powered Features
- **Dynamic Mystery Generation**: Every case is unique with different suspects, evidence, and solutions
- **Intelligent Suspect Responses**: AI characters maintain consistency and personality throughout interrogations
- **Comprehensive Analysis**: AI provides detailed reasoning, evidence connections, and alibi inconsistencies
- **Solution Verification**: AI evaluates your accusations and provides detailed feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MysteryAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

### Setup OpenAI API Key

You can set up your OpenAI API key in two ways:

#### Option 1: In-App Setup (Recommended)
1. Open the application in your browser
2. Look for the "🔑 OpenAI API Key" section in the sidebar
3. Enter your API key in the password field
4. The app will automatically use this key for all AI operations

#### Option 2: Environment Variable
1. Create a `.env` file in the project root
2. Add your API key: `OPENAI_API_KEY=your_api_key_here`

## 🎯 How to Play

### 1. Choose Your Mystery
- Select from 8 Indian-themed mystery categories
- Each theme offers a unique setting and crime type

### 2. Case Briefing
- Review the AI-generated case details
- Learn about the victim, crime scene, and suspects
- Get familiar with the initial evidence

### 3. Investigation Phase
- **Interrogate Suspects**: Ask questions to gather information
- **Examine Evidence**: Get detailed forensic analysis
- **Use Hints**: Get guidance when you're stuck

### 4. Make Your Accusation
- Select the perpetrator from the suspect list
- Provide detailed reasoning for your accusation
- Get scored feedback on your solution

### 5. AI Assistant (Optional)
- Use the AI auto-solve feature to see how AI would solve the case
- Compare your reasoning with AI's analysis
- Learn investigation techniques from AI's approach

## 📁 Project Structure

```
MysteryAI/
├── app.py                 # Main Streamlit application
├── mystery_engine.py      # AI-powered mystery generation and solving
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── ui/                   # User interface modules
    ├── __init__.py
    ├── home.py           # Home page and theme selection
    ├── briefing.py       # Case briefing display
    ├── interrogation.py  # Suspect questioning interface
    ├── evidence.py       # Evidence analysis interface
    ├── hints.py          # Hint system
    ├── accusation.py     # Final accusation and evaluation
    └── sidebar.py        # Navigation and API key input
```

## 🛠️ Technical Details

### AI Models Used
- **Primary Model**: GPT-4o-mini (configurable)
- **Temperature**: 0.8 (for creative mystery generation)
- **Framework**: LangChain for AI workflows

### Key Technologies
- **Streamlit**: Web interface framework
- **LangChain**: AI application framework
- **OpenAI API**: Language model access
- **Pydantic**: Data validation and parsing
- **Python-dotenv**: Environment variable management

### Data Models
- **Suspect**: Character with alibi, motive, personality, and secrets
- **Evidence**: Physical evidence with location and significance
- **MysteryCase**: Complete case structure with all components
- **AI Solution**: Structured analysis results with confidence levels

## 🎨 Customization

### Adding New Themes
1. Add new theme to the `themes` list in `ui/home.py`
2. Add corresponding theme mapping in `ui/briefing.py`
3. Update the AI prompts in `mystery_engine.py` if needed

### Modifying AI Behavior
- Adjust temperature settings in `mystery_engine.py`
- Modify prompts for different mystery styles
- Change confidence thresholds for AI auto-solve

### UI Customization
- Modify styling in individual UI modules
- Add new pages by creating modules in the `ui/` directory
- Update navigation in `ui/sidebar.py`
