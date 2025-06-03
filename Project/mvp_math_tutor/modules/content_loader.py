import os

# Define Profile IDs to map to directory names
PROFILE_STRUCTURED_ID = "PROFILE_STRUCTURED"
PROFILE_CONCEPTUAL_ID = "PROFILE_CONCEPTUAL"
PROFILE_VISUAL_ID = "PROFILE_VISUAL" # Optional Profile 3

PROFILE_DIR_MAP = {
    PROFILE_STRUCTURED_ID: "profile1_structured_methodical",
    PROFILE_CONCEPTUAL_ID: "profile2_conceptual_intuitive",
    PROFILE_VISUAL_ID: "profile3_visual_hands_on"
}

# For MVP, we have one topic: "Understanding Variables", split into 3 parts
MVP_TOPIC_ID = "TOPIC_ALGEBRA_VARIABLES"
LESSON_PART_FILENAMES = [
    "lesson_part_1.md",
    "lesson_part_2.md",
    "lesson_part_3.md"
]
MAX_LESSON_PARTS = len(LESSON_PART_FILENAMES)


def get_profile_name(profile_id):
    from .profiling_logic import PROFILE_NAMES # Avoid circular import at top level
    return PROFILE_NAMES.get(profile_id, "Unknown Profile")

def get_lesson_topic_name(topic_id):
    if topic_id == MVP_TOPIC_ID:
        return "Understanding Variables"
    return "Unknown Topic"

def load_lesson_part(profile_id, topic_id, part_index, base_path="data/lessons"):
    """
    Loads a specific part of a lesson for a given profile and topic.
    profile_id: e.g., "PROFILE_STRUCTURED"
    topic_id: e.g., "TOPIC_ALGEBRA_VARIABLES" (currently only one for MVP)
    part_index: 0, 1, or 2 for the MVP
    """
    if profile_id not in PROFILE_DIR_MAP:
        return "Error: Profile directory not found."
    if topic_id != MVP_TOPIC_ID: # For MVP, only one topic
        return "Error: Invalid topic for MVP."
    if not (0 <= part_index < MAX_LESSON_PARTS):
        return "Error: Invalid lesson part index."

    profile_dir = PROFILE_DIR_MAP[profile_id]
    lesson_filename = LESSON_PART_FILENAMES[part_index]
    
    file_path = os.path.join(base_path, profile_dir, lesson_filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: Lesson file not found at {file_path}"
    except Exception as e:
        return f"Error loading lesson: {str(e)}"

if __name__ == '__main__':
    # Example Usage:
    profile1 = PROFILE_STRUCTURED_ID
    topic = MVP_TOPIC_ID

    print(f"Profile Name for {profile1}: {get_profile_name(profile1)}")
    print(f"Topic Name for {topic}: {get_lesson_topic_name(topic)}")

    for i in range(MAX_LESSON_PARTS):
        print(f"\n--- Loading {profile1}, Part {i+1} ---")
        content = load_lesson_part(profile1, topic, i, base_path="../data/lessons") # Adjust path for direct script run
        if "Error:" not in content:
            print(content[:100] + "...") # Print first 100 chars
        else:
            print(content)
    
    # Test with a different profile
    profile2 = PROFILE_CONCEPTUAL_ID
    print(f"\n--- Loading {profile2}, Part 1 ---")
    content2 = load_lesson_part(profile2, topic, 0, base_path="../data/lessons")
    if "Error:" not in content2:
        print(content2[:100] + "...")
    else:
        print(content2)

    # Test Visual Profile
    profile3 = PROFILE_VISUAL_ID
    print(f"\n--- Loading {profile3}, Part 1 ---")
    content3 = load_lesson_part(profile3, topic, 0, base_path="../data/lessons")
    if "Error:" not in content3:
        print(content3[:100] + "...")
    else:
        print(content3)