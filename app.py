import os
import uuid

import nltk
import requests
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from huggingface_hub import InferenceClient 


# Initialize environment configuration from .env file
load_dotenv()
session = requests.Session()
session.verify = False
app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'

# Configure Hugging Face Inference API client for image generation
# Using Stable Diffusion 2.1 for high-quality, reliable image synthesis
client = InferenceClient(
    token=os.getenv("HF_API_KEY"),
    model="stabilityai/stable-diffusion-xl-base-1.0" 
)

# Ensure NLTK tokenizers are available for sentence segmentation
# Downloads punkt tokenizers if not already present in the system
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

def segment_text(text):
    try:
        return nltk.sent_tokenize(text)
    except:
        return [s.strip() for s in text.split('.') if s.strip()]

def enhance_prompt(sentence, style):
    clean_sentence = sentence.strip()
    prompt = f"{clean_sentence}, {style}, highly detailed, 8k, cinematic lighting"
    print(f"Generated Prompt: {prompt}")
    return prompt

def generate_image_sd(prompt):
    """
    Generate an image from a text prompt using Hugging Face's Stable Diffusion model.
    Returns the URL path to the saved image or a placeholder on failure.
    """
    try:
        # Generate image via API (client handles retries and error recovery internally)
        image = client.text_to_image(prompt)
        
        # Persist generated image to static/images directory with unique filename
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join('static', 'images', filename)
        image.save(filepath)
        
        print(f"Success! Image saved to {filepath}")
        return f"/static/images/{filename}"

    except Exception as e:
        print(f"Generation Error: {e}")
        return "https://placehold.co/600x400?text=Generation+Failed"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        narrative = request.form.get('narrative')
        style = request.form.get('style')

        if not narrative:
            return render_template('index.html')

        sentences = segment_text(narrative)[:3] 
        storyboard_panels = []

        for sent in sentences:
            engineered_prompt = enhance_prompt(sent, style)
            image_url = generate_image_sd(engineered_prompt)
            
            storyboard_panels.append({
                'original_text': sent,
                'engineered_prompt': engineered_prompt,
                'image_url': image_url
            })

        return render_template('storyboard.html', panels=storyboard_panels, style=style)

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(os.path.join('static', 'images'), exist_ok=True)
    app.run(debug=True)