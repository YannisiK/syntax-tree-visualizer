import streamlit as st
from constituent_treelib import ConstituentTree, Language
from pathlib import Path

st.set_page_config(page_title="Constituency Syntax Tree Visualizer", layout="centered")
st.title("Syntax Tree Generator")

@st.cache_resource
def load_nlp_pipeline():
    return ConstituentTree.create_pipeline(Language.English, ConstituentTree.SpacyModelSize.Medium)

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
        
        temp_svg_path = "temp_tree.svg"
        tree.export_tree(destination_filepath=temp_svg_path)

        svg_text = Path(temp_svg_path).read_text(encoding="utf-8")
        
        svg_text_with_bg = svg_text.replace("<svg ", '<svg style="background-color: white;" ', 1)
        
        styled_container = f"""
        <div style="background-color: white; padding: 20px; border-radius: 8px; display: inline-block; min-width: 100%;">
            {svg_text_with_bg}
        </div>
        """
        
        st.components.v1.html(styled_container, height=500, scrolling=True)
        
            
    except Exception as e:
        st.error(f"An error occurred while parsing: {e}")