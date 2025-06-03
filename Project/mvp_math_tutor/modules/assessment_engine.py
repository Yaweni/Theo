import json
from collections import defaultdict

# MVP Question IDs to be used
MVP_QUESTION_IDS = ["KNOW-001", "LOGIC-001", "VIS-001", "MEM-001", "ABSTRACT-001"]
# Max 5-7 questions for MVP, selected 5
# KNOW-001: MCQ Text (knowledge)
# LOGIC-001: Text Input (logic)
# VIS-001: MCQ Image (visual, logic) - text placeholder for image
# MEM-001: Phased Text (memory)
# ABSTRACT-001: Text Input (abstract, logic)

def load_questions(json_path="data/Onboarding-Easy.json", question_ids=None):
    """
    Loads assessment questions from the JSON file.
    Filters by question_ids if provided.
    """
    try:
        with open(json_path, 'r') as f:
            all_questions = json.load(f)
        
        if question_ids:
            selected_questions = [q for q in all_questions if q['id'] in question_ids]
            # Ensure the order of selected_questions matches question_ids
            ordered_questions = sorted(selected_questions, key=lambda q: question_ids.index(q['id']))
            return ordered_questions
        return all_questions
    except FileNotFoundError:
        return [] # Or raise an error
    except json.JSONDecodeError:
        return [] # Or raise an error

def calculate_scores(user_answers, questions_data):
    """
    Calculates raw scores for each cognitive attribute.
    user_answers: A list of dictionaries, e.g., [{'question_id': 'KNOW-001', 'answer': 'B'}]
    questions_data: The list of question objects used in the assessment.
    """
    cognitive_scores = defaultdict(float)
    
    questions_map = {q['id']: q for q in questions_data}

    for ua in user_answers:
        question_id = ua['question_id']
        user_answer = ua['answer']
        
        question = questions_map.get(question_id)
        if not question:
            continue

        correct_answer = ""
        if question['type'] == "memory" and question['format'] == "phased":
            # For phased questions, the correct answer is in the second phase
            if len(question.get('phases', [])) > 1 and 'correct' in question['phases'][1]:
                correct_answer = question['phases'][1]['correct']
        else:
            correct_answer = question.get('correct')

        # Simple correctness check (case-insensitive for text input)
        is_correct = False
        if isinstance(user_answer, str) and isinstance(correct_answer, str):
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        else: # For multiple choice or other types if answers are not strings
             is_correct = user_answer == correct_answer


        if is_correct:
            if 'scoring' in question and 'weights' in question['scoring']:
                for attribute, weight in question['scoring']['weights'].items():
                    cognitive_scores[attribute] += float(weight)
            elif question['type'] == "memory" and question['format'] == "phased" and \
                 'scoring' in question and 'weights' in question['scoring']: # MEM-001 is structured this way
                for attribute, weight in question['scoring']['weights'].items():
                     cognitive_scores[attribute] += float(weight)


    return dict(cognitive_scores)

def get_max_scores(questions_data):
    """
    Calculates the maximum possible score for each cognitive attribute
    based on the provided questions.
    """
    max_scores = defaultdict(float)
    for question in questions_data:
        if 'scoring' in question and 'weights' in question['scoring']:
            for attribute, weight in question['scoring']['weights'].items():
                max_scores[attribute] += float(weight)
    return dict(max_scores)

if __name__ == '__main__':
    # Example Usage:
    questions = load_questions(question_ids=MVP_QUESTION_IDS)
    print(f"Loaded {len(questions)} MVP questions.")
    # for q in questions:
    #     print(f"- {q['id']} ({q.get('type')}, {q.get('format')})")

    sample_user_answers = [
        {'question_id': 'KNOW-001', 'answer': 'B'}, # Correct
        {'question_id': 'LOGIC-001', 'answer': '48'},  # Correct
        {'question_id': 'VIS-001', 'answer': 'B'},   # Correct
        {'question_id': 'MEM-001', 'answer': 'C'},   # Correct
        {'question_id': 'ABSTRACT-001', 'answer': 'sand'} # Correct
    ]
    
    scores = calculate_scores(sample_user_answers, questions)
    print("\nCalculated Cognitive Scores (all correct):")
    for attr, score in scores.items():
        print(f"- {attr}: {score}")

    max_scores_val = get_max_scores(questions)
    print("\nMaximum Possible Scores:")
    for attr, score in max_scores_val.items():
        print(f"- {attr}: {score}")

    sample_user_answers_mixed = [
        {'question_id': 'KNOW-001', 'answer': 'A'}, # Incorrect
        {'question_id': 'LOGIC-001', 'answer': '48'},  # Correct
        {'question_id': 'VIS-001', 'answer': 'A'},   # Incorrect
        {'question_id': 'MEM-001', 'answer': 'B'},   # Correct
        {'question_id': 'ABSTRACT-001', 'answer': 'wrong'} # Incorrect
    ]
    scores_mixed = calculate_scores(sample_user_answers_mixed, questions)
    print("\nCalculated Cognitive Scores (mixed correctness):")
    for attr, score in scores_mixed.items():
        print(f"- {attr}: {score}")