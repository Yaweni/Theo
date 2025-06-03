import streamlit as st
from modules.content_loader import (
    load_lesson_part, 
    get_profile_name, 
    get_lesson_topic_name,
    MVP_TOPIC_ID, 
    MAX_LESSON_PARTS,
    PROFILE_STRUCTURED_ID,
    PROFILE_CONCEPTUAL_ID,
    PROFILE_VISUAL_ID
)
PROFILE_NAMES = {
    PROFILE_STRUCTURED_ID: "Structured & Methodical",
    PROFILE_CONCEPTUAL_ID: "Conceptual & Intuitive",
    PROFILE_VISUAL_ID: "Visual & Hands-On"
}

# --- State Initialization ---
def initialize_lesson_state():
    if 'current_lesson_part_idx' not in st.session_state:
        st.session_state.current_lesson_part_idx = 0
    if 'viewing_profile_for_contrast' not in st.session_state:
        # This will store the profile ID whose lesson content is currently being displayed.
        # Initially, it's the user's actual determined profile.
        st.session_state.viewing_profile_for_contrast = st.session_state.get('learner_profile', PROFILE_STRUCTURED_ID)


# --- Main Page Logic ---
def show_lesson_page():
    st.title("📖 Personalized Algebra Lesson")
    initialize_lesson_state()

    user_actual_profile = st.session_state.get('learner_profile')
    user_actual_profile_name = st.session_state.get('learner_profile_name', "Not Determined")

    if not user_actual_profile:
        st.error("Learner profile not found. Please complete the assessment first.")
        if st.button("⬅️ Go to Assessment"):
            st.switch_page("pages/02_Assessment.py")
        return

    # Determine which profile's content to show (either user's or one selected for contrast)
    profile_to_display = st.session_state.viewing_profile_for_contrast
    profile_name_to_display = get_profile_name(profile_to_display)
    
    # Display info about whose lesson style is being shown
    if profile_to_display == user_actual_profile:
        st.info(f"This lesson is tailored for your **{user_actual_profile_name}** profile.")
    else:
        st.warning(
            f"You are currently viewing the lesson as it would be presented for a "
            f"**{profile_name_to_display}** profile (for contrast). "
            f"Your actual profile is **{user_actual_profile_name}**."
        )

    # Load and display lesson content
    topic_id = MVP_TOPIC_ID
    lesson_part_idx = st.session_state.current_lesson_part_idx
    
    lesson_content = load_lesson_part(profile_to_display, topic_id, lesson_part_idx)
    topic_name = get_lesson_topic_name(topic_id)
    
    st.header(f"{topic_name} - Part {lesson_part_idx + 1} of {MAX_LESSON_PARTS}")
    st.markdown(f"*(Style: {profile_name_to_display})*")
    st.markdown("---")
    
    if "Error:" in lesson_content:
        st.error(lesson_content)
    else:
        st.markdown(lesson_content, unsafe_allow_html=True) # Allow HTML if your MD has it

    st.markdown("---")

    # --- Navigation for Lesson Parts ---
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if st.button("⬅️ Previous Part", disabled=(lesson_part_idx == 0), use_container_width=True):
            st.session_state.current_lesson_part_idx -= 1
            st.rerun()
    with col3:
        if st.button("Next Part ➡️", disabled=(lesson_part_idx >= MAX_LESSON_PARTS - 1), use_container_width=True):
            st.session_state.current_lesson_part_idx += 1
            st.rerun()
    
    st.markdown("---")

    # --- "See Other Styles" Functionality ---
    st.subheader("👀 See How Other Profiles Might Learn This Concept")
    st.caption("Select a different profile to see this lesson part presented in their style.")

    available_profiles_for_contrast = {
        "Your Profile": user_actual_profile,
        PROFILE_NAMES[PROFILE_STRUCTURED_ID]: PROFILE_STRUCTURED_ID,
        PROFILE_NAMES[PROFILE_CONCEPTUAL_ID]: PROFILE_CONCEPTUAL_ID,
        PROFILE_NAMES[PROFILE_VISUAL_ID]: PROFILE_VISUAL_ID,
    }
    
    # Ensure "Your Profile" is distinct if it's one of the standard ones
    # and avoid duplicate buttons
    
    unique_contrast_buttons = {}
    if profile_to_display != user_actual_profile: # Add button to switch back to user's own profile
         unique_contrast_buttons[f"Revert to My Profile ({user_actual_profile_name})"] = user_actual_profile
    
    for name, id_val in available_profiles_for_contrast.items():
        if id_val == profile_to_display: # Don't show button for currently viewed style
            continue
        if name == "Your Profile" and id_val == user_actual_profile and profile_to_display == user_actual_profile:
            continue # Already viewing own profile

        button_label = name
        if name == "Your Profile": # Clarify if it's the user's own
            button_label = f"View as My Profile ({user_actual_profile_name})"
            
        if id_val != user_actual_profile: # Avoid duplicates
            unique_contrast_buttons[button_label] = id_val

    cols_contrast = st.columns(len(unique_contrast_buttons))
    idx = 0
    for btn_label, profile_id_to_set in unique_contrast_buttons.items():
        with cols_contrast[idx]:
            if st.button(btn_label, key=f"contrast_{profile_id_to_set}", use_container_width=True):
                st.session_state.viewing_profile_for_contrast = profile_id_to_set
                # st.session_state.current_lesson_part_idx = 0 # Optionally reset to first part
                st.rerun()
        idx += 1
        if idx >= len(cols_contrast): # Safety for more buttons than columns
            idx = 0 


    st.markdown("---")
    # --- Call to Action / Next Steps ---
    if lesson_part_idx >= MAX_LESSON_PARTS - 1:
        st.success("🎉 You've completed this lesson segment!")
        st.markdown("""
        **Thank you for trying out the AI-Personalized Tutor MVP!**

        This demonstration aimed to show how learning content can be adapted based on a
        quick cognitive assessment. Imagine a future where entire courses are dynamically
        tailored to help each student learn most effectively.

        **Next Steps & Vision:**
        *   Integrate more sophisticated AI for dynamic content generation.
        *   Expand the range of cognitive traits assessed and learning styles addressed.
        *   Develop a full curriculum with adaptive learning paths.
        *   Incorporate interactive exercises and real-time feedback.

        Interested in learning more or discussing the project?
        *   [Read the Pitch Deck]()
        *   Contact: `www.kaaynos.com/contact`
        *   Follow us on [LinkedIn](https://www.linkedin.com/company/kaaynos) for updates.
        """)

    if st.button("↩️ Back to Profile Revelation"):
        # Reset viewing contrast to user's actual profile before going back
        st.session_state.viewing_profile_for_contrast = user_actual_profile
        st.session_state.current_lesson_part_idx = 0 # Reset lesson part
        st.switch_page("pages/03_Your_Profile.py")

if __name__ == '__main__':
    # For direct testing, mock necessary session state from previous pages
    if 'learner_profile' not in st.session_state:
        st.session_state.learner_profile = PROFILE_CONCEPTUAL_ID # Example
        st.session_state.learner_profile_name = get_profile_name(PROFILE_CONCEPTUAL_ID)
    
    show_lesson_page()