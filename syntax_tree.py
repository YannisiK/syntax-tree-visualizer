
import streamlit as st
from constituent_treelib import ConstituentTree, Language
from pathlib import Path
import nltk
import benepar

st.set_page_config(page_title="Constituency Syntax Tree Visualizer", layout="centered")
st.title("Syntax Tree Generator")

NLTK_DATA = Path(".nltk_data")
NLTK_DATA.mkdir(exist_ok=True)

nltk.data.path.insert(0, str(NLTK_DATA))

@st.cache_resource
def load_nlp_pipeline():
    try:
        benepar.Parser("benepar_en3")
    except Exception:
        benepar.download(
            "benepar_en3",
            download_dir=str(NLTK_DATA)
        )
    return ConstituentTree.create_pipeline(Language.English, ConstituentTree.SpacyModelSize.Medium, download_models=False)

with st.spinner("Loading NLP engine..."):
    nlp_pipeline = load_nlp_pipeline()

user_sentence = st.text_input(
    "Enter a sentence:", 
    value=""
)

if user_sentence.strip():
    try:
        tree = ConstituentTree(user_sentence, nlp_pipeline)
        st.subheader("Visual Tree Structure")
        
        svg_text = tree._repr_svg_()

        st.components.v1.html(
            svg_text,
            height=500,
            scrolling=True
        )
        
       
        
            
    except Exception as e:
        st.error(f"An error occurred while parsing: {e}")

