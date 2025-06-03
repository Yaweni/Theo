import streamlit as st
from modules.assessment_engine import load_questions, calculate_scores, MVP_QUESTION_IDS, get_max_scores
from modules.profiling_logic import determine_learner_profile
import time

# --- State Initialization ---
def initialize_assessment_state():
    if 'assessment_questions' not in st.session_state:
        st.session_state.assessment_questions = load_questions(question_ids=MVP_QUESTION_IDS)
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = [] # Store as list of dicts: {'question_id': id, 'answer': ans}
    if 'cognitive_scores' not in st.session_state:
        st.session_state.cognitive_scores = {}
    if 'learner_profile' not in st.session_state:
        st.session_state.learner_profile = None
    if 'learner_profile_name' not in st.session_state:
        st.session_state.learner_profile_name = ""
    # For phased questions (like MEM-001)
    if 'phased_question_step' not in st.session_state: # 0 for memorization, 1 for question
        st.session_state.phased_question_step = 0 
    if 'phased_memorization_content' not in st.session_state:
        st.session_state.phased_memorization_content = None
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False
    if 'timer_start_time' not in st.session_state:
        st.session_state.timer_start_time = 0
    if 'question_submitted_answer' not in st.session_state: # To store answer for current question before moving
        st.session_state.question_submitted_answer = None

# --- Helper Functions ---
def display_question(question):
    st.subheader(f"Question {st.session_state.current_question_idx + 1} of {len(st.session_state.assessment_questions)}")
    if question.get('type') != "memory" or question.get('format') != "phased":
        st.markdown(f"**{question['prompt']}**")

    answer = None
    q_type = question.get('type')
    q_format = question.get('format')

    if q_type == "image" and q_format == "multiple_choice":
        # Display the question prompt
        st.subheader(question.get("prompt", "Question prompt not available"))
    
        # Try to load the main question image
        question_image = question.get("image_url")
        if question_image:
            try:
                st.image(question_image, width=min(200, st.session_state.get('screen_width', 200)))
            except Exception as e:
                st.warning(f"Could not load question image: {question_image}")
                st.text(f"Image reference: {question_image}")
        else:
            st.info("No image provided for this question")
        
        # Process options
        options_data = question.get("options", [])
        option_texts = []
        option_ids = []

        # Determine column layout based on option count
        cols = st.columns(min(4, len(options_data)))
        
        for idx, opt in enumerate(options_data):
            with cols[idx % len(cols)]:
                with st.container():
                    # Display option image or fallback
                    if 'image_url' in opt:
                        try:
                            st.image(
                                opt['image_url'],
                                width=60,  # Fixed small size for options
                                use_container_width='auto',  # Responsive within container
                                caption=f"Option {opt['id']}"
                            )
                            option_texts.append(f"Option {opt['id']}")
                        except Exception as e:
                            option_texts.append(f"Option {opt['id']} (Image unavailable)")
                    else:
                        option_texts.append(f"Option {opt['id']}: {opt.get('text', '')}")
                    
                    option_ids.append(opt['id'])
        
        # Radio button selection
        radio_key = f"q_{question['id']}_{st.session_state.current_question_idx}"
        selected_option = st.radio(
            "Your answer:",
            options=option_texts,
            key=radio_key,
            index=None,
            horizontal=True  # Better for small option sets
        )
        
        # Map selection to option ID
        if selected_option:
            answer = option_ids[option_texts.index(selected_option)]
            #st.session_state.answers[st.session_state.current_question_idx] = answer     

    elif q_type == "text" and q_format == "multiple_choice":
        options = [opt['text'] for opt in question.get('options', [])]
        option_ids = [opt['id'] for opt in question.get('options', [])]
        radio_key = f"q_{question['id']}_{st.session_state.current_question_idx}"
        selected_option_text = st.radio("Your Answer:", options, key=radio_key, index=None)
        if selected_option_text:
            answer = option_ids[options.index(selected_option_text)]

    elif q_type == "text" and q_format == "text_input":
        text_input_key = f"q_{question['id']}_{st.session_state.current_question_idx}"
        answer = st.text_input("Your Answer:", key=text_input_key, placeholder="Type your answer here")

    elif q_type == "memory" and q_format == "phased": # Specifically for MEM-001 (text-based)
        phases = question.get('phases', [])
        if st.session_state.phased_question_step == 0: # Memorization phase
            st.session_state.phased_memorization_content = phases[0]['prompt']
            st.markdown(f"**Memorize the following:**")
            st.markdown(f"### {st.session_state.phased_memorization_content.split(': ')[1]}") # Show only symbols
            
            # For MVP, a simple "I've memorized" button. Timer can be added later.
            # duration = phases[0].get('duration', 10)
            # st.caption(f"You have {duration} seconds to memorize.")
            # if st.button("I've memorized", key=f"mem_confirm_{question['id']}"):
            #     st.session_state.phased_question_step = 1
            #     st.rerun() # Rerun to show question phase
            # We will advance this with the "Next" button logic.
        
        elif st.session_state.phased_question_step == 1: # Question phase
            st.markdown(f"**{phases[1]['prompt']}**")
            options = [opt['text'] for opt in phases[1].get('options', [])]
            option_ids = [opt['id'] for opt in phases[1].get('options', [])]
            radio_key = f"q_phase1_{question['id']}_{st.session_state.current_question_idx}"
            selected_option_text = st.radio("Your Answer:", options, key=radio_key, index=None)
            if selected_option_text:
                answer = option_ids[options.index(selected_option_text)]
    else:
        st.warning(f"Unsupported question type/format for MVP: {q_type}/{q_format}")

    return answer

def process_answer_and_advance(current_question, submitted_answer):
    if submitted_answer is not None and submitted_answer != "": # Ensure some answer is given
        st.session_state.user_answers.append({
            'question_id': current_question['id'],
            'answer': submitted_answer
        })

        # For phased questions, handle step transition
        if current_question.get('type') == "memory" and current_question.get('format') == "phased":
            if st.session_state.phased_question_step == 0: # Was memorization phase
                st.session_state.phased_question_step = 1 # Move to question phase
                st.session_state.question_submitted_answer = None # Clear for next part of question
                st.rerun()
                return # Don't advance question index yet
            # If it was question phase, it will fall through to advance index

        st.session_state.current_question_idx += 1
        st.session_state.phased_question_step = 0 # Reset for next potential phased question
        st.session_state.question_submitted_answer = None # Clear for next question
        
        if st.session_state.current_question_idx >= len(st.session_state.assessment_questions):
            # Assessment finished
            st.session_state.max_scores = get_max_scores(st.session_state.assessment_questions)
            st.session_state.cognitive_scores = calculate_scores(
                st.session_state.user_answers, 
                st.session_state.assessment_questions
            )
            profile_id, profile_name = determine_learner_profile(
                st.session_state.cognitive_scores,
                st.session_state.max_scores
            )
            st.session_state.learner_profile = profile_id
            st.session_state.learner_profile_name = profile_name
            st.switch_page("pages/03_Your_Profile.py")
        else:
            st.rerun() # Rerun to display next question
    else:
        st.warning("Please select or enter an answer before proceeding.")

# --- Main Page Logic ---
def show_assessment_page():
    st.title("📝 Cognitive Assessment")
    initialize_assessment_state()

    if not st.session_state.assessment_questions:
        st.error("Could not load assessment questions. Please check the configuration.")
        if st.button("Back to Welcome"):
            st.switch_page("pages/01_Welcome.py")
        return

    # Check if assessment is complete
    if st.session_state.current_question_idx >= len(st.session_state.assessment_questions):
        st.success("Assessment Completed!")
        st.write("Calculating your profile...")
        # This state should ideally be caught by the advancement logic, but as a fallback:
        if st.session_state.learner_profile:
             st.switch_page("pages/03_Your_Profile.py")
        else: # Recalculate if somehow missed
            st.session_state.max_scores = get_max_scores(st.session_state.assessment_questions)
            st.session_state.cognitive_scores = calculate_scores(
                st.session_state.user_answers, 
                st.session_state.assessment_questions
            )
            profile_id, profile_name = determine_learner_profile(
                st.session_state.cognitive_scores,
                st.session_state.max_scores
            )
            st.session_state.learner_profile = profile_id
            st.session_state.learner_profile_name = profile_name
            st.switch_page("pages/03_Your_Profile.py")
        return

    # Display current question
    current_question = st.session_state.assessment_questions[st.session_state.current_question_idx]
    
    # Store the answer from the widget in session_state immediately if it changes
    # This is useful if we want to show immediate feedback or have complex forms
    # For simple next button, we can just pass it.
    submitted_answer = display_question(current_question)
    if submitted_answer is not None: # Capture widget output
        st.session_state.question_submitted_answer = submitted_answer

    # --- Navigation Buttons ---
    cols = st.columns(2)
    with cols[0]:
        if st.button("⬅️ Previous Question", disabled=st.session_state.current_question_idx == 0 and st.session_state.phased_question_step == 0):
            if st.session_state.phased_question_step == 1: # If in question part of phased q
                st.session_state.phased_question_step = 0 # Go back to memorization part
            else:
                st.session_state.current_question_idx -= 1
                st.session_state.phased_question_step = 0 # Reset phase for previous q
                if st.session_state.user_answers: # Remove last answer if going back
                    st.session_state.user_answers.pop()
            st.session_state.question_submitted_answer = None # Clear submitted answer
            st.rerun()
    
    with cols[1]:
        button_text = "Next Question ➡️"
        if current_question.get('type') == "memory" and current_question.get('format') == "phased" and st.session_state.phased_question_step == 0:
            button_text = "I've Memorized, Next Step ➡️"
        elif st.session_state.current_question_idx == len(st.session_state.assessment_questions) - 1 and \
             not (current_question.get('type') == "memory" and current_question.get('format') == "phased" and st.session_state.phased_question_step == 0):
            button_text = "Submit Assessment 🏁"

        if st.button(button_text, type="primary", use_container_width=True):
            answer_to_process = st.session_state.get('question_submitted_answer')
            # For phased memorization, answer is not submitted until question phase
            if current_question.get('type') == "memory" and current_question.get('format') == "phased" and st.session_state.phased_question_step == 0:
                 answer_to_process = "MEMORIZED" # Placeholder for memorization step

            if answer_to_process is not None or (current_question.get('type') == "memory" and current_question.get('format') == "phased" and st.session_state.phased_question_step == 0) :
                process_answer_and_advance(current_question, answer_to_process)
            else:
                st.warning("Please select or enter an answer before proceeding.")


    st.markdown("---")
    if st.button("Restart Assessment / Back to Welcome"):
        # Clear relevant session state before switching
        keys_to_reset = ['assessment_questions', 'current_question_idx', 'user_answers', 
                         'cognitive_scores', 'learner_profile', 'learner_profile_name',
                         'phased_question_step', 'phased_memorization_content', 'question_submitted_answer']
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page("pages/01_Welcome.py")

if __name__ == '__main__':
    show_assessment_page()
