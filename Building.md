# MVP-building.md: AI-Personalized Math Tutor

## 1. Overall MVP Goal

To create a functional web application prototype that demonstrates the core value proposition:
*   Assesses a user's cognitive traits through a short, interactive quiz.
*   Generates a simplified "Learner Profile" based on the assessment.
*   Delivers a segment of an Algebra lesson in a style demonstrably tailored to that Learner Profile.
*   The primary audience for this MVP is potential pre-seed investors and early advisors to showcase the concept and technical feasibility.

## 2. Target Timeline

*   **3-4 weeks** of focused development.

## 3. Core User Flow

1.  **Welcome/Landing Page:**
    *   Brief introduction to the app.
    *   Button: "Start Your Personalized Assessment."
2.  **Cognitive Assessment:**
    *   User answers a short sequence of questions (selected from `Onboarding-Easy.json`).
    *   Questions are presented one at a time.
    *   User submits answers.
3.  **Profile "Revelation" (Optional but Recommended):**
    *   A simple screen briefly indicating the derived Learner Profile (e.g., "Your Profile: Visual & Structured Learner"). This makes the personalization more explicit.
4.  **Personalized Lesson Delivery:**
    *   User is presented with a short Algebra lesson snippet (e.g., "Solving Linear Equations").
    *   The style, explanation, and examples in the lesson are visibly different based on the Learner Profile derived in step 3.
5.  **Contrast/Showcase Personalization (Optional but Recommended):**
    *   A button/option to "See how other profiles might learn this concept," allowing the user to view the alternative lesson variations.
6.  **Call to Action/Next Steps:**
    *   Brief concluding message.
    *   Link to pitch deck or contact information.

## 4. Key Modules / Components

### 4.1. Assessment Engine

*   **Functionality:**
    *   Load assessment questions from the provided JSON file (`Onboarding-Easy.json`).
    *   For the MVP, select a **subset of 5-7 questions** that represent diverse cognitive skills and are easier to implement (see "Question Types for MVP" below).
    *   Present questions one by one to the user.
    *   Collect user answers (multiple choice, text input).
    *   Track basic scoring (correct/incorrect). For timed questions in the JSON, implement a simple countdown timer if feasible within the timeframe; otherwise, ignore timer for MVP and score based on correctness only.
    *   Calculate a raw score for each cognitive attribute (e.g., `visual`, `logic`, `memory`) based on the `scoring.weights` in the JSON for correctly answered questions.
*   **Data Source:** `Onboarding-Easy.json` (and potentially similar files for medium/hard, though MVP will focus on easy).

### 4.2. Cognitive Profiling Logic

*   **Functionality:**
    *   Takes the raw cognitive attribute scores from the Assessment Engine.
    *   Applies a **simple rule-based system** to assign the user to one of **2-3 pre-defined Learner Profiles.**
    *   **Example Learner Profiles & Logic (to be refined):**
        *   **Profile 1: "Structured & Methodical"**
            *   *Criteria (example):* Higher scores in `memory`, moderate in `logic`.
            *   *Implication for Lesson:* Benefits from step-by-step instructions, clear definitions, repetition, fewer abstractions initially.
        *   **Profile 2: "Conceptual & Intuitive"**
            *   *Criteria (example):* Higher scores in `abstract`, `pattern recognition` (if questions for this are used), moderate `logic`.
            *   *Implication for Lesson:* Can handle more complex examples sooner, benefits from analogies, big-picture explanations, connections to other concepts.
        *   **(Optional) Profile 3: "Visual & Hands-On"**
            *   *Criteria (example):* Higher scores in `visual`, `spatial` (if questions are used).
            *   *Implication for Lesson:* Benefits from diagrams, visual examples, less text-heavy explanations. (Visuals might be described in text for MVP if image generation is too complex).
*   **Output:** A simple identifier for the determined Learner Profile (e.g., `PROFILE_STRUCTURED`, `PROFILE_CONCEPTUAL`).

### 4.3. Personalized Content Delivery

*   **Functionality:**
    *   Based on the Learner Profile determined by the Profiling Logic:
        *   Select and display the corresponding pre-written variation of an Algebra lesson snippet.
    *   **Content Source:** Manually pre-written lesson variations (2-3 versions for 1-2 Algebra concepts).
        *   **Example Algebra Concept for MVP:** "Understanding Variables" or "Solving Basic Linear Equations (e.g., x + 5 = 10)."
        *   Each variation should be clearly distinct in its language, examples, and structure to showcase personalization.

### 4.4. User Interface (UI)

*   **Functionality:**
    *   Simple, clean, and functional. Prioritize clarity over aesthetics.
    *   Display welcome message and start button.
    *   Present assessment questions clearly (text, options for MCQ, input fields).
    *   Navigation (Next question, Submit assessment).
    *   Display the tailored lesson content.
    *   (Optional) Display the "other styles" for contrast.
    *   Display the final call to action.
*   **Responsiveness:** Aim for basic responsiveness so it's viewable on desktop and mobile browsers.

## 5. Technology Stack Recommendations

*   **Backend & Frontend:** **Python with Streamlit.**
    *   *Reasoning:* Fastest way to build interactive web UIs with Python, ideal for data-centric apps and demos. Handles state management for simple multi-page flows acceptably for an MVP. Your Python proficiency is a key advantage here.
*   **Alternative (if more traditional web dev experience):** Python with Flask (for backend API) + simple HTML/CSS/JavaScript (for frontend). This offers more control but has a steeper curve for a quick, polished UI if web dev isn't a primary strength.
*   **Data Storage:** For MVP, no persistent database is strictly needed. User session can hold assessment state. Questions are loaded from JSON.
*   **Deployment:** Streamlit Cloud (easy, free for public apps), Heroku (free tier), or PythonAnywhere.

## 6. Content Requirements

### 6.1. Assessment Questions (from `Onboarding-Easy.json`)

*   **Question Types for MVP (prioritize based on ease of implementation):**
    1.  **`type: "text", format: "multiple_choice"`** (e.g., `KNOW-001`, `KNOW-002`, `KNOW-003`): Easiest.
    2.  **`type: "text", format: "text_input"`** (e.g., `LOGIC-001`, `ABSTRACT-001`, `LOGIC-003`): Relatively easy.
    3.  **`type: "image", format: "multiple_choice"`** (e.g., `VIS-001`, `LOGIC-002`, `VIS-002`): Requires handling image display. Use placeholder text (e.g., "Image for VIS-001") or very simple, easily sourced/created images if actual image assets are time-consuming. Focus on questions where the *logic* can be assessed even if the image is simple.
    4.  **`type: "memory", format: "phased"` (text-based variations ONLY):** (e.g., `MEM-001`). Can be implemented with two simple screens in Streamlit.
*   **Question Types to DEFER or SIMULATE for MVP (due to complexity):**
    *   **`type: "drawing", format: "canvas"`**: Too complex. Replace with a conceptual MCQ about the task if desired, or omit.
    *   **`type: "auditory"` / sound files**: Playback adds complexity. Replace with text-based memory/sequence tasks, or omit.
    *   Complex **`phased` questions with media**: Simplify.
*   **Selection for MVP:** Choose 5-7 questions from the "easier to implement" types above that provide a good mix for scoring `visual`, `logic`, `memory`, `knowledge`, `abstract`.

### 6.2. Algebra Lesson Snippets

*   **Topic:** Choose 1 (max 2) simple Algebra concept. E.g., "What is a variable?" or "Solving one-step equations like x + 3 = 8."
*   **Variations:** Write 2-3 distinct variations for EACH chosen concept, tailored to the Learner Profiles defined in 4.2.
    *   **Variation 1 (for "Structured & Methodical"):** Very step-by-step, definitions upfront, simple examples, repetition.
    *   **Variation 2 (for "Conceptual & Intuitive"):** Starts with a bigger picture/analogy, uses more complex or abstract examples, encourages connections.
    *   **(Optional) Variation 3 (for "Visual & Hands-On"):** Describes visual approaches, uses spatial language, even if actual diagrams are just text placeholders like "[Imagine a number line here]".
*   **Format:** Store as plain text or simple Markdown within the Python application code.

## 7. Key Features (MVP Scope)

*   Load questions from JSON.
*   Present a sequence of 5-7 selected assessment questions.
*   Basic scoring of answers.
*   Rule-based assignment to 1 of 2-3 Learner Profiles.
*   Display of 1 Algebra lesson snippet tailored to the profile.
*   (Highly Recommended) Option to view alternative lesson styles for contrast.

### What's OUT of Scope for this MVP:

*   User accounts & login.
*   Persistent data storage for users.
*   Full implementation of all question types from JSON (especially drawing/audio).
*   Actual LLM integration for dynamic content generation (this is *simulated* by pre-written variations).
*   Gamification elements.
*   Adaptive learning *orders* (the "Alpha vision").
*   Advanced UI styling or animations.
*   Comprehensive error handling or input validation.
*   Scalability features.
*   Administrative backend.

## 8. Deployment

*   **Goal:** Easy, quick deployment for demo purposes.
*   **Recommendation:** Streamlit Cloud (if using Streamlit), or Heroku free tier.

## 9. Success Metrics for THIS MVP (Internal & Demo)

*   **Completion:** Can a user complete the assessment and see a personalized lesson?
*   **Clarity of Personalization:** Is it *obvious* to a viewer (e.g., investor) that the lesson content has changed based on the (simulated) profile? The "see other styles" feature is key here.
*   **Plausibility:** Does the flow and the type of personalization seem credible and align with the pitch?
*   **Founder Demo-Readiness:** Can you, the founder, confidently walk someone through the MVP and explain the underlying logic and future vision?

---

This `MVP-building.md` provides a solid roadmap. For the `tests.md`, I'll create a separate file.