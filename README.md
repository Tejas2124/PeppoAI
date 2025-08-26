# 🎥 Peppo Task – AI Video Generator  

Peppo Task is a simple web-based application that lets users generate videos from text prompts using different AI video models. It provides a clean interface to select models, enter API keys, and instantly generate AI-driven video content.  

---

## 🚀 How It Works  

1. **Login & Authentication**  
   - Users log in (via frontend + Flask backend).  
   - API keys are securely saved through the backend `/set-key` endpoint.  

2. **Model Selection**  
   - The sidebar provides a dropdown with supported AI models:  
     - `veo-3.0-generate-preview`
   - These model will be available shortly:  
     - `veo-2.5`  
     - `gen-1`  
     - Hugging Face `Wan-AI/Wan2.2-TI2V-5B`  

3. **Video Generation**  
   - Enter a text **prompt** (e.g., *"A futuristic city skyline at sunset"*)  
   - Choose a model  
   - Click **Generate** → the backend calls the corresponding API (Gemini or Hugging Face).  

4. **Video Display**  
   - The generated video is saved in the server and shown inside a player on the main screen.  

---

## 🛠️ Built With  

- **Frontend** → HTML, CSS, JavaScript  
- **Backend** → Python (Flask)  
- **APIs** →  
  - Google Gemini Video Models (`veo-3.0`,)  
  - Hugging Face `Wan-AI/Wan2.2-TI2V-5B`  
- **Authentication** → JWT Tokens handled by Flask  

---

## 📂 Components  

- **Sidebar**  
  - Model selection dropdown  
  - API key input & save button  

- **Main Section**  
  - Video player container  
  - Prompt input box + Generate button  

- **Profile & User Management**  
  - Profile button in top-right corner  
  - Logout & re-login flow  

---

## ▶️ Example Usage  

1. Select model **Veo 3.0 Preview**  
2. Enter API Key 
3. Type a prompt:  a dog whose fur look like cat.
4. Click **Generate**  
5. Video appears in the player 🎬  

---

## 📹 Example Video  

👉 Here’s a sample output video (generated with `veo-3.0-preview`):  
[![Watch Example](https://img.youtube.com/vi/7a68yf9jSO0/0.jpg)](https://www.youtube.com/watch?v=7a68yf9jSO0) 

  

---

## ⚡ Quick Start  

```bash
# Clone the repo
git clone https://github.com/Tejas2124/PeppoAI.git
cd PeppoAI

# Install dependencies
pip install -r requirements.txt

# Run the Flask backend
python app.py

# Open index.html in your browser

