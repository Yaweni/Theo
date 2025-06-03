# tests.md: Unit Tests for AI-Personalized Math Tutor MVP

This file outlines key areas for unit testing to ensure the core logic of the MVP is functioning as expected. For a 3-4 week MVP, focus on testing critical business logic rather than exhaustive UI testing. Frameworks like `pytest` are recommended for Python.

## 1. Assessment Engine Logic

### 1.1. Question Loading & Parsing
*   **Test:** `test_load_questions_from_json`
    *   Verify that questions are correctly loaded from the `Onboarding-Easy.json` file.
    *   Check if the number of loaded questions matches the expected subset for the MVP.
    *   Verify that essential fields (id, type, format, prompt, options, correct, scoring.weights) are parsed correctly for a sample of selected MVP question types.
*   **Test:** `test_invalid_json_format`
    *   Ensure the system handles a malformed JSON file gracefully (e.g., logs an error, doesn't crash). (Lower priority for MVP if JSON is static).

### 1.2. Question Scoring
*   **Test:** `test_score_mcq_correct`
    *   Given a multiple-choice question and the correct user answer, verify the score is 1 (or appropriate positive score).
*   **Test:** `test_score_mcq_incorrect`
    *   Given a multiple-choice question and an incorrect user answer, verify the score is 0.
*   **Test:** `test_score_text_input_correct`
    *   Given a text input question and the correct user answer (case-insensitivity might be a factor to test), verify the score is 1.
*   **Test:** `test_score_text_input_incorrect`
    *   Given a text input question and an incorrect user answer, verify the score is 0.
*   **Test:** `test_score_phased_memory_question_correct` (for simplified text-based memory)
    *   Verify correct scoring for a simple phased memory question.
*   **Test:** `test_timer_ignored_for_scoring` (If timer functionality is deferred for MVP)
    *   Verify that scoring is based on correctness, irrespective of any timer values in the JSON if timer logic isn't implemented.

## 2. Cognitive Profiling Logic

### 2.1. Attribute Score Aggregation
*   **Test:** `test_aggregate_cognitive_scores`
    *   Given a set of answered questions and their individual scores, verify that the weighted scores for each cognitive attribute (e.g., `visual`, `logic`, `memory`) are calculated correctly according to `scoring.weights`.
    *   Example: If a user answers 2 logic questions correctly (one with `logic: 1.0` weight, another with `logic: 0.8` weight), the total raw logic score should reflect this.

### 2.2. Learner Profile Assignment
*   **Test:** `test_assign_profile_structured_methodical`
    *   Given a set of aggregated cognitive scores that meet the criteria for the "Structured & Methodical" profile, verify this profile is assigned.
*   **Test:** `test_assign_profile_conceptual_intuitive`
    *   Given scores meeting criteria for "Conceptual & Intuitive," verify this profile is assigned.
*   **(Optional) Test:** `test_assign_profile_visual_hands_on`
    *   Test assignment for the third profile if implemented.
*   **Test:** `test_profile_assignment_boundary_conditions` (Lower priority for MVP but good practice)
    *   Test scenarios where scores are exactly on the boundary between two profiles to ensure consistent assignment.
*   **Test:** `test_default_profile_assignment` (If applicable)
    *   If there's a scenario where no specific profile criteria are met, does it assign a default profile correctly?

## 3. Personalized Content Delivery

### 3.1. Lesson Variation Selection
*   **Test:** `test_select_lesson_for_structured_profile`
    *   Given the "Structured & Methodical" profile, verify that the correct pre-written lesson variation (Variation 1) for that profile is selected.
*   **Test:** `test_select_lesson_for_conceptual_profile`
    *   Given the "Conceptual & Intuitive" profile, verify that its corresponding lesson variation (Variation 2) is selected.
*   **Test:** `test_content_exists_for_all_profiles_and_concepts`
    *   Verify that for every defined profile and every MVP Algebra concept, a corresponding lesson variation is available (to prevent errors if a profile is assigned but no content exists).

## General Notes for MVP Testing:

*   **Mocking:** Use mocking for external dependencies or complex UI interactions if necessary, to keep unit tests focused on specific logic.
*   **Simplicity:** For the MVP, these tests are primarily to ensure the core decision-making logic is sound.
*   **Data-Driven Tests:** Where possible, use data-driven approaches (e.g., `pytest.mark.parametrize`) to test various input combinations for scoring and profiling logic efficiently.

---

This should give you a very solid plan to build from! The JSON file is a fantastic asset. Good luck!