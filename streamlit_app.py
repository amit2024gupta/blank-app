import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model with safety settings
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1024,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel(
    model_name='gemini-pro',
    generation_config=generation_config,
    safety_settings=safety_settings
)

def configure_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(page_title="Song Lyrics Maker", page_icon="\U0001F3B6", layout="centered")

def display_title_and_description():
    """Display the app's title and description."""
    st.title("\U0001F3B6 Song Lyrics Maker")
    st.write("Create custom song lyrics tailored to your preferences!")

def get_user_inputs():
    """Collect user inputs for lyrics generation."""
    genre = st.selectbox("Select Genre", [
        "Pop", "Rock", "Hip Hop", "Jazz", "Country", "Classical", "Electronic", "Other"
    ])
    lyrics_writer_style = st.text_input("Lyrics Writer Style", placeholder="e.g., Bob Dylan, Taylor Swift, Eminem")
    prompt = st.text_area("Prompt", placeholder="Write a brief description or theme for the song")
    purpose = st.selectbox("Purpose of the Song", ["Fun", "Heartfelt", "Romantic", "Inspirational", "Other"])
    temperature = st.slider("Creativity Level", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    return genre, lyrics_writer_style, prompt, purpose, temperature

def refine_prompt(genre, lyrics_writer_style, prompt, purpose):
    """Refine the input prompt for better lyrics generation."""
    tone = "Energetic and upbeat" if genre in ["Pop", "Electronic"] else "Soulful and deep"
    language_style = "modern and conversational" if genre in ["Hip Hop", "Pop"] else "timeless and poetic"
    
    refined_prompt = (
        f"Create song lyrics with the following characteristics:\n"
        f"- **Genre**: {genre}\n"
        f"- **Lyrics Writer Style**: {lyrics_writer_style}\n"
        f"- **Purpose**: {purpose}\n"
        f"- **Theme/Prompt**: {prompt}\n"
        f"\nAdditional Details:\n"
        f"1. Tone: {tone}.\n"
        f"2. Include imagery and metaphors matching the genre.\n"
        f"3. Keep the language {language_style}.\n"
    )
    return refined_prompt

def display_refined_prompt(refined_prompt):
    """Display the refined prompt to the user."""
    st.write("**Refined Prompt for Generation:**")
    st.text_area("Prompt Preview", refined_prompt, height=200)

def display_generated_lyrics(refined_prompt, temperature):
    """Generate and display lyrics based on the refined prompt."""
    try:
        lyrics = generate_text(refined_prompt, temperature)
        st.success("Here are your generated lyrics:")
        st.text_area("Generated Lyrics", lyrics, height=300)
    except Exception as e:
        st.error(f"An error occurred while generating lyrics: {e}")

def clean_ai_response(response_text: str) -> str:
    """Clean up AI response text and handle markdown formatting"""
    
    try:
        # Remove markdown code blocks if present
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text.replace("```json", "").replace("```", "")
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.replace("```", "")
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text
    except Exception as e:
        raise

def generate_text(prompt: str, temperature: float) -> str:
    """Generate text using the AI model"""
    try:
        response = model.generate_content(prompt)
        return clean_ai_response(response.text)
    except Exception as e:
        st.error("Failed to generate content")
        return ""

def main():
    configure_page()
    display_title_and_description()
    genre, lyrics_writer_style, prompt, purpose, temperature = get_user_inputs()

    if st.button("Generate Lyrics"):
        if not prompt:
            st.error("Please enter a prompt to generate lyrics.")
        else:
            refined_prompt = refine_prompt(genre, lyrics_writer_style, prompt, purpose)
            display_refined_prompt(refined_prompt)
            display_generated_lyrics(refined_prompt, temperature)

if __name__ == "__main__":
    main()
