**Project Goal:** Develop an MVP for an AI-Personalized Math Tutor web application.

**Core Task:** Generate the Python code structure (primarily using Streamlit) for the core user flow of this MVP.

**Key Files Provided (Assume these are attached/accessible):**
1.  `MVP-building.md`: Outlines the overall MVP scope, user flow, modules, tech stack (Streamlit), and features. Please adhere closely to this specification.
2.  `Onboarding-Easy.json`: Contains the structure for assessment questions. The MVP will use a subset of these (specified in `MVP-building.md` or chosen as per its guidance).
3.  Lesson Markdown Files (e.g., `profile1_lesson1.md`, `profile2_lesson1.md`, etc.): Contains the pre-written lesson content for different learner profiles and topics.

**Specific Instructions for Code Generation:**

**1. Overall Application Structure (Streamlit Multi-Page App if appropriate):**
    *   Create a main `app.py` file.
    *   Organize different sections/steps of the user flow (Welcome, Assessment, Profile Display, Lesson, "See Other Styles") into logical functions or, if using Streamlit's multi-page app feature, separate Python files in a `pages/` directory.

**2. Welcome Page (`pages/01_Welcome.py` or function in `app.py`):**
    *   Display a simple welcome message.
    *   A button to navigate to the Assessment.

**3. Assessment Module (`pages/02_Assessment.py` or function):**
    *   **Question Loading:** Function to load and parse the *selected MVP subset* of questions from `Onboarding-Easy.json`.
    *   **Question Presentation:**
        *   Display questions one at a time.
        *   Use appropriate Streamlit widgets for different question `format`s from the JSON (e.g., `st.radio` for `multiple_choice`, `st.text_input` for `text_input`).
        *   For `type: "image"` questions, if actual image display is complex, display the `image_url` as text or a placeholder.
        *   For `type: "memory", format: "phased"` (text-only versions), implement a two-step display (memorization phase, then question phase).
        *   Implement a "Next Question" button.
    *   **Answer Collection & Scoring:**
        *   Store user answers.
        *   After all questions are answered, implement a function `calculate_scores(user_answers, questions_data)` that calculates raw scores for each cognitive attribute (e.g., `visual`, `logic`, `memory`) based on `scoring.weights` in the JSON for correctly answered questions.
    *   **State Management:** Use `st.session_state` to manage the current question index, user answers, and calculated scores across interactions.

**4. Cognitive Profiling Module (function, likely called after assessment):**
    *   Implement a function `determine_learner_profile(cognitive_scores)`:
        *   Input: The dictionary of aggregated cognitive scores (e.g., `{'visual': 0.8, 'logic': 0.5, ...}`).
        *   Logic: Apply the **simple rule-based system** (as discussed and to be detailed based on chosen MVP questions and their weights from `MVP-building.md` or my refined notes) to assign the user to one of 2-3 pre-defined Learner Profiles (e.g., `PROFILE_STRUCTURED`, `PROFILE_CONCEPTUAL`).
        *   Output: The assigned profile identifier. Store this in `st.session_state`.

**5. Profile "Revelation" Page (Optional - `pages/03_Your_Profile.py` or function):**
    *   Display a message like "Based on your assessment, your learning profile appears to be: [Profile Name]."
    *   Button to proceed to the lesson.

**6. Personalized Lesson Delivery Module (`pages/04_Lesson.py` or function):**
    *   **Content Loading:** Function to load the appropriate Markdown lesson file based on the `st.session_state.learner_profile` and the current (MVP's first) Algebra topic.
        *   Example: If profile is `PROFILE_STRUCTURED` and topic is "Understanding Variables - Lesson 1", load `profile1_lesson1_what_is_a_variable.md`.
    *   **Display:** Use `st.markdown()` to render the lesson content.
    *   Implement navigation for the 3 mini-lessons per profile (e.g., "Next Lesson Part" button).

**7. "See Other Styles" Functionality (within lesson page or separate):**
    *   If the user is viewing a lesson for `PROFILE_STRUCTURED`, provide buttons/options to view the same lesson topic (e.g., Lesson 1.1) as it would be presented for `PROFILE_CONCEPTUAL` and `PROFILE_VISUAL`. This involves loading and displaying the alternative Markdown files.

**8. Code Style and Comments:**
    *   Generate clean, well-commented Python code.
    *   Use meaningful variable and function names.
    *   Focus on functionality and clarity for this MVP.

**Output Desired:**
*   Python files (`app.py`, and files in `pages/` if using multi-page structure).
*   Clear separation of concerns where possible (e.g., distinct functions for assessment logic, profiling, content loading).
*   Basic error handling is not a priority, but code should not crash on expected valid inputs.

**Constraints for MVP (reiterate from `MVP-building.md`):**
*   No user accounts/login.
*   No persistent database.
*   Focus on the core loop: Assessment -> Profiling -> Personalized Content Display.
*   LLM integration is SIMULATED by pre-written content.
*   Gamification is OUT of scope.
*   Adaptive learning ORDERS are OUT of scope.
