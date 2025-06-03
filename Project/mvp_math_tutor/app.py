import streamlit as st

st.set_page_config(
    page_title="Theo",
    layout="wide"
)

# This app uses Streamlit's multi-page app feature.
# Navigation is handled by files in the `pages/` directory.
# `01_Welcome.py` will be the default starting page due to numerical prefixing.

st.sidebar.success("Navigate through the app above.")

# You can add any global configurations or session state initializations here if needed,
# though most will be handled within individual pages.

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Welcome" # Default starting point

# The actual page content is in the `pages/` directory.
# Streamlit automatically creates a sidebar for navigation.
# To ensure `01_Welcome.py` is the first page users see, we don't need much here.
# If you wanted to force a specific page programmatically (though not standard for multipage apps):
# from streamlit.runtime.scriptrunner import RerunData, RerunException
# from streamlit.source_util import get_pages
#
# def switch_page(page_name: str):
#     pages = get_pages("app.py")
#     for page_hash, pag_config in pages.items():
#         if pag_config["page_script_hash"] == page_hash and pag_config["page_name"] == page_name:
#             raise RerunException(RerunData(page_script_hash=page_hash))
#
# if st.session_state.current_page == "Welcome":
#      pass # Streamlit will load 01_Welcome.py by default
# elif st.session_state.current_page == "Assessment":
#      # Potentially switch to Assessment page, but better handled by button navigation
#      pass


st.markdown(
    """
    <style>
    /* Optional: Add some global styling if desired */
    .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AI-Personalized Tutor MVP")
st.caption("Navigate using the sidebar to start your personalized learning experience.")