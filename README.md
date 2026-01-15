# The Pitch Visualizer

## Overview

The Pitch Visualizer is an AI-powered web application that automatically transforms narrative text (such as customer success stories, sales pitches, or product descriptions) into visual storyboards. Simply paste your narrative text, select a visual style, and the application generates a multi-panel storyboard with AI-generated images that bring your story to life.

### Capabilities

- **Automatic Narrative Segmentation:** Intelligently breaks text into logical scenes using NLTK's sentence tokenization
- **AI-Powered Image Generation:** Creates high-quality images using Stable Diffusion 2.1 via Hugging Face's Inference API
- **Style Customization:** Choose from multiple visual styles (Corporate Vector, Cinematic, Sketch, Cyberpunk, Oil Painting) that are consistently applied across all panels
- **Prompt Engineering:** Automatically enhances simple sentences into detailed, style-optimized prompts for better image generation
- **Web-Based Interface:** Clean, responsive UI built with Bootstrap 5 for easy interaction

## Setup & Installation

### Prerequisites

- **Python 3.8 or higher**
- **Hugging Face Access Token** (required for image generation)
  - Sign up at [Hugging Face](https://huggingface.co/join)
  - Generate a token at [Hugging Face Settings](https://huggingface.co/settings/tokens)
  - Select **"Read"** role (sufficient for using the Inference API)

### Step-by-Step Setup

1. **Clone or download the repository**
   ```bash
   cd pitch_visualizer
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API key management**
   
   Create a `.env` file in the project root directory:
   ```bash
   touch .env
   ```
   
   Add your Hugging Face API token to the `.env` file:
   ```
   HF_API_KEY=your_huggingface_token_here
   ```
   
   **Important:** The `.env` file is already included in `.gitignore` to keep your API key secure. Never commit your API key to version control.

5. **Verify the static images directory exists**
   
   The application will automatically create `static/images/` on first run, but you can create it manually:
   ```bash
   mkdir -p static/images
   ```

### Execution

1. **Activate your virtual environment** (if not already active)
   ```bash
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. **Run the Flask application**
   ```bash
   python app.py
   ```

3. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

4. **Generate your first storyboard**
   - Paste your narrative text in the textarea
   - Select a visual style from the dropdown
   - Click "Generate Storyboard"
   - Wait 30-60 seconds for image generation (images are generated sequentially)
   - View your generated storyboard with up to 3 panels

## Design Choices & Methodology

### Architecture Decisions

**Single AI Model Approach:**
- The application uses **Stable Diffusion 2.1** exclusively via Hugging Face's Inference API
- This choice prioritizes simplicity, cost-effectiveness (free tier available), and reliability
- No external LLM is needed for prompt engineering, keeping the architecture lightweight

**Narrative Processing:**
- **NLTK Sentence Tokenization:** Uses NLTK's `sent_tokenize()` for intelligent sentence segmentation
- **Fallback Mechanism:** If NLTK tokenization fails, falls back to simple period-based splitting
- **Panel Limitation:** Processes only the first 3 sentences to balance generation time and user experience

### Prompt Engineering Methodology

The core of the image generation quality lies in the prompt engineering strategy implemented in the `enhance_prompt()` function:

**Template Structure:**
```
[Original Sentence] + [User-Selected Style] + [Quality Enhancers]
```

**Components:**

1. **Original Sentence (Base Content):**
   - The user's narrative text, cleaned and stripped of extra whitespace
   - Provides the semantic content and context for the image

2. **User-Selected Style:**
   - Pre-defined style strings that guide the visual aesthetic
   - Examples include:
     - `"Corporate Memphis vector art, flat design, vibrant colors"`
     - `"Cinematic photorealistic, dramatic lighting, 4k"`
     - `"Hand-drawn sketch, black and white, pencil texture"`
   - Ensures visual consistency across all panels in a storyboard

3. **Quality Enhancers (Fixed):**
   - `"highly detailed"` - Encourages the model to generate intricate images
   - `"8k"` - Signals high resolution expectations
   - `"cinematic lighting"` - Adds professional visual quality

**Why This Approach Works:**

- **Simplicity:** Direct concatenation is fast and predictable
- **Consistency:** Same enhancement pattern ensures uniform quality across panels
- **User Control:** Style selection gives users creative control while maintaining technical quality
- **Stable Diffusion Optimization:** The keyword-rich format aligns with how Stable Diffusion models interpret prompts

**Example Transformation:**
```
Input:  "John struggled with manual data entry."
Style:  "Corporate Memphis vector art, flat design, vibrant colors"

Output: "John struggled with manual data entry., Corporate Memphis vector art, flat design, vibrant colors, highly detailed, 8k, cinematic lighting"
```

### Error Handling

- **Image Generation Failures:** Returns a placeholder image URL instead of crashing
- **NLTK Tokenization Errors:** Gracefully falls back to simple text splitting
- **Missing API Key:** Application will fail with a clear error message (handled by `os.getenv()`)

### File Management

- **Unique Filenames:** Uses UUID4 to prevent filename collisions
- **Local Storage:** Images saved to `static/images/` for web serving
- **Automatic Directory Creation:** Creates `static/images/` on application startup if missing

## Tech Stack

- **Backend Framework:** Flask (Python)
- **NLP Library:** NLTK (Natural Language Toolkit) for sentence segmentation
- **Image Generation:** Hugging Face Inference API with Stable Diffusion 2.1
- **Image Processing:** Pillow (PIL) for image handling
- **Environment Management:** python-dotenv for secure API key storage
- **Frontend:** HTML5, Jinja2 templating, Bootstrap 5
- **HTTP Client:** httpx (via huggingface_hub)

## Project Structure

```
pitch_visualizer/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not in version control)
├── .gitignore            # Git ignore rules
├── templates/
│   ├── index.html        # Main input form
│   └── storyboard.html   # Generated storyboard display
└── static/
    └── images/           # Generated images storage
```

## Usage Tips

- **Narrative Length:** Keep narratives concise (3-5 sentences work best)
- **Style Selection:** Choose styles that match your narrative tone
- **Generation Time:** Each image takes 10-20 seconds; be patient
- **Image Quality:** Results vary based on prompt clarity and style selection

## Troubleshooting

**"Generation Error" messages:**
- Verify your `HF_API_KEY` is correctly set in `.env`
- Check your internet connection
- Ensure your Hugging Face token has "Read" permissions

**NLTK download issues:**
- The application automatically downloads required NLTK data on first run
- If downloads fail, manually run: `python -m nltk.downloader punkt punkt_tab`

**Port already in use:**
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

## License

This project is open source and available for modification and distribution.
