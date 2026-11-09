import streamlit as st
import google.generativeai as genai
import tempfile
import os

# Top-level Page Configuration
st.set_page_config(
    page_title="Suno AI Prompt Extractor",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Suno AI Prompt Extractor")
st.write("Ngarkoni skedarin tuaj MP3 të gjeneruar nga Suno për të nxjerrë **Style Prompt-in** e saktë.")

# Sidebar per vendosjen e API Key
st.sidebar.header("Konfigurimi")
api_key = st.sidebar.text_input("Vendosni Google Gemini API Key:", type="password")

if not api_key:
    st.info("Ju lutemi vendosni Gemini API Key në menu-në anësore për të vazhduar.", icon="🔑")
    st.stop()

# Konfigurimi i Gemini Client
genai.configure(api_key=api_key)

# Upload i skedarit Audio
uploaded_file = st.file_uploader("Zgjidhni skedarin MP3", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/mp3")
    
    if st.button("🚀 Gjenero Suno Style Prompt", type="primary"):
        with st.spinner("Po analizohet audioja dhe po dekodohet stili..."):
            try:
                # Ruajtja e skedarit përkohësisht në disk për t'ia dërguar API-së
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # 1. Ngarkimi i audios në Gemini File API
                audio_file = genai.upload_file(path=tmp_file_path)

                # 2. Udhëzimi i saktë (System Prompt) për analizën e Suno Styles
                system_prompt = """
                You are an expert audio engineer and AI music prompt specialist for Suno AI.
                Analyze the provided audio file thoroughly and determine its musical parameters.
                Extract and reconstruct the exact Suno AI 'Style Prompt' that was used or would recreate this exact sound.

                Follow these guidelines for the output:
                1. Focus on main genre, sub-genres, specific instruments, tempo/BPM feeling, vocal style/gender, mood, and production quality tags.
                2. Use standard Suno style tag formats (comma-separated English keywords).
                3. Avoid overly verbose explanations in the main prompt string.

                Format your final response as follows:
                
                ### 🎯 Suno Style Prompt (Kopjoje këtë):
                `[Comma-separated Suno prompt tags here]`

                ### 📊 Analiza e Detajuar:
                - **Zhanri Kryesor:** ...
                - **Instrumentet:** ...
                - **BPM & Ritmi:** ...
                - **Stili i Zërit:** ...
                - **Atmosfera / Mood:** ...
                """

                # 3. Thirrja e Modelit Multimodal
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([audio_file, system_prompt])

                # 4. Pastrimi i skedarit të përkohshëm
                os.remove(tmp_file_path)

                # Paraqitja e Rezultatit
                st.success("Analiza u krye me sukses!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Pati një gabim gjatë përpunimit: {str(e)}")
