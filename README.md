# IUI 2025 User Study: Voice-Adaptive Conversational AI

This repository contains the code and deployment infrastructure for a user study investigating how AI systems perceive and respond to user inputs delivered in different voice characteristics (gender, accent, emotion).

## 📋 Overview

This study provides an interactive environment where participants:
1. Select conversation starter questions
2. Record themselves asking questions
3. Hear their voice converted to different voice characteristics
4. Listen to AI responses to those converted voices
5. Provide feedback on their experience

## 🗂️ Repository Structure

```
iui_2025/
├── user_study_iui_2025.ipynb    # Main interactive study notebook
├── modal_app.py                  # Modal deployment configuration
├── deploy_modal.sh               # Deployment automation script
├── MODAL_DEPLOYMENT.md           # Detailed deployment guide
├── requirements.txt              # Local dependencies
├── modal_requirements.txt        # Modal-specific dependencies
├── target_voices/                # Reference voice samples for conversion
├── DiT_uvit_tat_xlsr_ema.pth    # Pre-trained Seed-VC model weights
└── .gitattributes               # Git LFS configuration
```

## 🚀 Quick Start

### Option 1: Run Locally

**Installation:**

```bash
# Clone the repository
git clone https://github.com/shreeharsha-bs/iui_2025.git
cd iui_2025

# Install dependencies
pip install -r requirements.txt

# Clone Seed-VC
git clone https://github.com/Plachtaa/seed-vc.git

# Launch Jupyter
jupyter notebook user_study_iui_2025.ipynb
```
## 📊 Study Workflow

### 1. Setup & Configuration
- Loads required libraries and initializes the Seed-VC voice conversion model
- Configures file paths and target voice profiles

### 2. Question Selection
- Participants choose from 8 conversation starters covering topics like:
  - Career advancement
  - Workplace relationships
  - Work-life balance
  - Professional development

### 3. Audio Recording
- Browser-based audio recording (no plugins required)
- Supports microphone input with automatic format conversion

### 4. Voice Conversion
- Converts recorded audio to multiple target voices:
  - Female American (Happy emotion)
  - Male British (Angry emotion)
  - Male American (Sad emotion)

### 5. Feedback Collection
Participants rate each interaction on:
- **Content Quality**: Relevance and helpfulness of AI responses
- **Voice Quality**: Naturalness, clarity, and tone appropriateness
- **Interaction Experience**: Understanding, comfort, trust, and engagement
- **Open-ended feedback**: Additional comments and observations

### 6. Final Questionnaire
- Overall preference comparison
- Importance of consistent AI behavior
- Concerns about voice-adaptive systems
- Optional demographics

## 📧 Contact

For questions about the study or technical issues:
- GitHub: [@shreeharsha-bs](https://github.com/shreeharsha-bs)
- Open an issue in this repository

---

**Note**: This study involves human participants and voice data. Please ensure compliance with your institution's IRB requirements before conducting the study.
