import streamlit as st

def show_welcome_page():
    st.title("👋 Welcome to UnlockED 😁")
    st.subheader("Your AI-Personalized Tutor!")
    
    st.markdown("""
    This application is an MVP (Minimum Viable Product) designed to showcase how AI can tailor learning
    experiences to your unique cognitive traits.

    **Here's how it works:**
    1.  You'll take a short, interactive **Cognitive Assessment**.
    2.  Based on your results, we'll generate a simplified **Learner Profile**.
    3.  You'll then receive an Algebra lesson snippet delivered in a style personalized to your profile.

    The goal is to demonstrate the concept and technical feasibility of personalized education.
    """)
    
    st.info("Ready to discover your learning style and experience personalized content?")

    # Using st.page_link for navigation (Streamlit 1.30+)
    # Ensure the target pages exist in the `pages` directory.
    if st.button("🚀 Start Your Personalized Assessment", type="primary", use_container_width=True):
        st.switch_page("pages/02_Assessment.py")

    st.markdown("---")
    st.markdown("Built with ❤️ by YaYa.")

if __name__ == '__main__':
    show_welcome_page()