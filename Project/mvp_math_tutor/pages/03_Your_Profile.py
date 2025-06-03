import streamlit as st

def show_profile_revelation_page():
    st.title("🌟 Your Learner Profile")

    if 'learner_profile_name' in st.session_state and st.session_state.learner_profile_name:
        profile_name = st.session_state.learner_profile_name
        st.success(f"Based on your assessment, your learning profile appears to be: **{profile_name}**")
        
        st.markdown(f"""
        This profile suggests how you might best engage with new mathematical concepts.
        For instance, as a **{profile_name}**:
        """)

        # Add brief descriptions based on profile (can be expanded)
        if st.session_state.learner_profile == "PROFILE_STRUCTURED":
            st.markdown("""
            *   You may benefit from clear, step-by-step instructions.
            *   Well-defined concepts and examples likely help you learn effectively.
            *   Repetition and methodical approaches could be your strong suit.
            """)
        elif st.session_state.learner_profile == "PROFILE_CONCEPTUAL":
            st.markdown("""
            *   You might grasp the 'big picture' quickly.
            *   Analogies and connections to other concepts could be very helpful.
            *   You may enjoy exploring complex examples sooner.
            """)
        elif st.session_state.learner_profile == "PROFILE_VISUAL":
            st.markdown("""
            *   Visual aids, diagrams, and spatial representations can significantly enhance your understanding.
            *   You might prefer less text-heavy explanations and more visual examples.
            *   "Seeing" the problem can be key for you.
            """)
        else:
            st.markdown("*   Your unique blend of traits will be considered in the upcoming lesson.")

        st.info("Next, you'll experience a short Algebra lesson tailored to this profile.")
        
        if st.button("📚 Proceed to Your Personalized Lesson", type="primary", use_container_width=True):
            st.switch_page("pages/04_Lesson.py")
            
    else:
        st.warning("Your learner profile hasn't been determined yet. Please complete the assessment first.")
        if st.button("⬅️ Go to Assessment"):
            st.switch_page("pages/02_Assessment.py")
        if st.button("🏠 Back to Welcome"):
            st.switch_page("pages/01_Welcome.py")

    st.markdown("---")
    st.caption("Note: This is a simplified profile for MVP demonstration purposes.")

if __name__ == '__main__':
    # For direct testing, mock session state
    if 'learner_profile_name' not in st.session_state:
        st.session_state.learner_profile_name = "Conceptual & Intuitive" # Example
        st.session_state.learner_profile = "PROFILE_CONCEPTUAL"
    show_profile_revelation_page()