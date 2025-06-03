from collections import defaultdict

# Define Profile IDs and Names
PROFILE_STRUCTURED_ID = "PROFILE_STRUCTURED"
PROFILE_CONCEPTUAL_ID = "PROFILE_CONCEPTUAL"
PROFILE_VISUAL_ID = "PROFILE_VISUAL"

PROFILE_NAMES = {
    PROFILE_STRUCTURED_ID: "Structured & Methodical",
    PROFILE_CONCEPTUAL_ID: "Conceptual & Intuitive",
    PROFILE_VISUAL_ID: "Visual & Hands-On"
}

# Example Learner Profiles & Logic (to be refined based on actual question weights and desired sensitivity)
# For MVP, we'll use a simplified rule based on the dominant scored attribute from the selected MVP questions.
# Selected MVP questions score: knowledge, logic, visual, memory, abstract.

def determine_learner_profile(cognitive_scores, max_attribute_scores):
    """
    Applies a simple rule-based system to assign the user to one of 2-3 pre-defined Learner Profiles.
    Input:
        cognitive_scores: Dict of raw scores (e.g., {'visual': 0.8, 'logic': 0.5, ...})
        max_attribute_scores: Dict of max possible scores for each attribute (e.g., {'visual': 0.9, ...})
    Output:
        Tuple: (profile_id, profile_name)
    """
    
    # Calculate percentage scores
    p_scores = {}
    for attr, score in cognitive_scores.items():
        max_score = max_attribute_scores.get(attr, 1.0) # Avoid division by zero if attr not in max_scores
        if max_score > 0:
            p_scores[attr] = score / max_score
        else:
            p_scores[attr] = 0.0

    # For easier access to percentage scores, default to 0 if not present
    p_visual = p_scores.get('visual', 0.0)
    p_abstract = p_scores.get('abstract', 0.0)
    p_memory = p_scores.get('memory', 0.0)
    p_logic = p_scores.get('logic', 0.0) # Logic might be a secondary characteristic

    # Determine dominant primary trait
    primary_traits = {
        'visual': p_visual,
        'abstract': p_abstract,
        'memory': p_memory
    }
    
    # Sort traits by score in descending order
    sorted_traits = sorted(primary_traits.items(), key=lambda item: item[1], reverse=True)
    
    # Default profile
    assigned_profile_id = PROFILE_STRUCTURED_ID 

    if not sorted_traits or sorted_traits[0][1] < 0.3: # If no significant score or no scores
        return assigned_profile_id, PROFILE_NAMES[assigned_profile_id]

    dominant_trait, dominant_score = sorted_traits[0]

    # Simplified MVP rules:
    if dominant_trait == 'visual' and dominant_score >= 0.4:
        assigned_profile_id = PROFILE_VISUAL_ID
    elif dominant_trait == 'abstract' and dominant_score >= 0.4:
        # Conceptual often has a logic component
        if p_logic >= 0.2: # Check for some logical reasoning
            assigned_profile_id = PROFILE_CONCEPTUAL_ID
        else: # If abstract is high but logic is very low, might fall back
            assigned_profile_id = PROFILE_STRUCTURED_ID # Or a more general profile
    elif dominant_trait == 'memory' and dominant_score >= 0.4:
        # Structured often has memory and logic components
        if p_logic >= 0.2:
             assigned_profile_id = PROFILE_STRUCTURED_ID
        else: # If memory is high but logic is very low
            assigned_profile_id = PROFILE_STRUCTURED_ID # Fallback for now
    else:
        # If the dominant trait score is low, or doesn't fit neatly, use default
        # This could also be a point to assign a "Balanced" profile if desired later
        assigned_profile_id = PROFILE_STRUCTURED_ID


    # Fallback if primary traits are very close or low, logic can influence
    # This is a very basic MVP logic, can be greatly expanded.
    # Example: if p_logic is exceptionally high and others are moderate, it might influence.

    # Ensure a profile is always assigned
    if assigned_profile_id not in PROFILE_NAMES:
        assigned_profile_id = PROFILE_STRUCTURED_ID # Default safeguard

    return assigned_profile_id, PROFILE_NAMES[assigned_profile_id]


if __name__ == '__main__':
    from assessment_engine import MVP_QUESTION_IDS, load_questions, get_max_scores
    
    # Load questions to get max scores correctly
    questions = load_questions(question_ids=MVP_QUESTION_IDS)
    max_scores = get_max_scores(questions)
    print(f"Max scores for profiling: {max_scores}")

    # Test cases:
    scores1 = {'visual': 0.9, 'logic': 0.5, 'memory': 0.2, 'abstract': 0.1} # Expect Visual
    profile_id1, profile_name1 = determine_learner_profile(scores1, max_scores)
    print(f"Scores: {scores1} -> Profile: {profile_name1} ({profile_id1})")

    scores2 = {'visual': 0.2, 'logic': 0.8, 'memory': 0.3, 'abstract': 0.7} # Expect Conceptual (abstract high, logic moderate)
    profile_id2, profile_name2 = determine_learner_profile(scores2, max_scores)
    print(f"Scores: {scores2} -> Profile: {profile_name2} ({profile_id2})")

    scores3 = {'visual': 0.1, 'logic': 0.6, 'memory': 0.9, 'abstract': 0.2} # Expect Structured
    profile_id3, profile_name3 = determine_learner_profile(scores3, max_scores)
    print(f"Scores: {scores3} -> Profile: {profile_name3} ({profile_id3})")
    
    scores4 = {'visual': 0.1, 'logic': 0.1, 'memory': 0.1, 'abstract': 0.1} # Expect Default (Structured)
    profile_id4, profile_name4 = determine_learner_profile(scores4, max_scores)
    print(f"Scores: {scores4} -> Profile: {profile_name4} ({profile_id4})")

    # Test with actual max scores for normalization
    # Assuming all correct for VIS-001, ABSTRACT-001, LOGIC-001
    # VIS-001: visual: 0.9, logic: 0.1
    # ABSTRACT-001: abstract: 0.7, logic: 0.3
    # LOGIC-001: logic: 1.0
    # MEM-001: memory: 0.9
    # KNOW-001: knowledge: 1.0
    
    # Max: {'visual': 0.9, 'logic': 1.4, 'memory': 0.9, 'abstract': 0.7, 'knowledge': 1.0}

    scores_visual_heavy = {'visual': 0.9, 'logic': 0.1, 'memory': 0.0, 'abstract': 0.0}
    pid, pname = determine_learner_profile(scores_visual_heavy, max_scores)
    print(f"Scores: {scores_visual_heavy} -> Profile: {pname} ({pid})") # Expect Visual

    scores_abstract_heavy = {'visual': 0.0, 'logic': 0.4, 'memory': 0.0, 'abstract': 0.7} # logic 0.4/1.4 = ~0.28
    pid, pname = determine_learner_profile(scores_abstract_heavy, max_scores)
    print(f"Scores: {scores_abstract_heavy} -> Profile: {pname} ({pid})") # Expect Conceptual

    scores_memory_heavy = {'visual': 0.0, 'logic': 0.5, 'memory': 0.9, 'abstract': 0.0} # logic 0.5/1.4 = ~0.35
    pid, pname = determine_learner_profile(scores_memory_heavy, max_scores)
    print(f"Scores: {scores_memory_heavy} -> Profile: {pname} ({pid})") # Expect Structured