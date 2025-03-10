import re
from typing import Dict, Tuple, Optional

def extract_solution(solution_str: str) -> Tuple[Optional[str], str]:
    """Extracts the final answer from the model's response string.
    
    Args:
        solution_str: Raw response string from the language model
        
    Returns:
        Tuple containing (extracted_answer, processed_string)
    """
    # Split response to isolate assistant output
    if "Assistant:" in solution_str:
        processed_str = solution_str.split("Assistant:", 1)[1]
    elif "<|im_start|>assistant" in solution_str:
        processed_str = solution_str.split("<|im_start|>assistant", 1)[1]
    else:
        print("[Error] Failed to locate model response header")
        return None, solution_str

    # Extract final answer using XML-style tags
    answer_pattern = r'<answer>(.*?)</answer>'
    matches = list(re.finditer(answer_pattern, processed_str, re.DOTALL))
    
    if not matches:
        print("[Error] No valid answer tags found")
        return None, processed_str
        
    final_answer = matches[-1].group(1).strip()
    return final_answer, processed_str

def parse_solution_text_format(solution_text: str) -> Dict[str, str]:
    """Parses ground truth solution text into status dictionary.
    
    Args:
        solution_text: Formatted solution text from dataset
        
    Returns:
        Dictionary mapping character names to their roles (knight/knave)
    """
    status_dict = {}
    print("\n[Ground Truth Parsing]")
    
    for line in solution_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        match = re.search(r'\b([A-Za-z]+)\b.*?\b(knight|knave)\b', line, re.IGNORECASE)
        if match:
            name, role = match.groups()
            status_dict[name] = role.lower()
            print(f"  Found: {name} → {role}")
        else:
            print(f"  [Warning] Unparseable line: '{line}'")
    
    return status_dict

def parse_model_answer(answer_text: str, expected_names: list) -> Optional[Dict[str, str]]:
    """Parses model's answer text into status dictionary.
    
    Args:
        answer_text: Text extracted from model's <answer> tags
        expected_names: List of character names requiring identification
        
    Returns:
        Dictionary mapping character names to predicted roles, or None if incomplete
    """
    status_dict = {}
    print("\n[Model Answer Parsing]")
    print(f"  Expected characters: {expected_names}")

    knight_count = answer_text.lower().count('knight')
    knave_count = answer_text.lower().count('knave')

    print(f"  Number of predicted roles: {knight_count + knave_count}")
    if knight_count + knave_count != len(expected_names):
        print(f"  [Error] Number of characters mismatch: {knight_count + knave_count} != {len(expected_names)}")
        return None

    for name in expected_names:
        pattern = re.compile(
            rf'\b{re.escape(name)}\b\s+is\s+a\s+\b(knight|knave)\b', 
            re.IGNORECASE
        )
        match = pattern.search(answer_text)
        
        if match:
            role = match.group(1).lower()
            status_dict[name] = role
            print(f"  Found: {name} → {role}")
        else:
            print(f"  [Error] Missing identification for {name}")
            return None
    
    return status_dict

def validate_response_structure(processed_str: str) -> bool:
    """Performs comprehensive validation of response structure.
    
    Args:
        processed_str: Processed response string from the model
        
    Returns:
        Boolean indicating whether all formatting requirements are met
    """
    # print("\n[Structure Validation]")
    validation_passed = True

    # Check required tags
    tags = {
        'think_start': ('<think>', 1),
        'think_end': ('</think>', 1),
        'answer_start': ('<answer>', 1),
        'answer_end': ('</answer>', 1)
    }

    positions = {}
    for tag_name, (tag_str, expected_count) in tags.items():
        count = processed_str.count(tag_str)
        positions[tag_name] = pos = processed_str.find(tag_str)
        
        # print(f"  {tag_str}: count={count}, position={pos}")
        
        if count != expected_count:
            # print(f"  [Error] {tag_str} appears {count} times (expected {expected_count})")
            validation_passed = False

    # Verify tag order
    if (positions['think_start'] > positions['think_end'] or
        positions['think_end'] > positions['answer_start'] or
        positions['answer_start'] > positions['answer_end']):
        # print("  [Error] Incorrect tag order: Expected <think>...</think><answer>...</answer>")
        validation_passed = False
    else:
        # print("  Tag sequence validation passed")
        pass

    return validation_passed

def compute_score(solution_str: str, 
                 ground_truth: Dict[str, str],
                 format_reward: int = 1,
                 answer_reward: float = 1.0) :
    """Computes comprehensive score for model response.
    
    Args:
        solution_str: Raw model response string
        ground_truth: Dictionary containing ground truth data
        format_reward: Points awarded/deducted for format correctness
        answer_reward: Points awarded/deducted for answer correctness
        
    Returns:
        Total score (sum of format and answer rewards)
    """
    print("\n" + "="*80)
    print(" Processing New Sample ".center(80, '='))
    
    # 删掉system prompt
    solution_str = re.sub(r"<\|im_start\|>system.*?<\|im_end\|>", "", solution_str, flags=re.DOTALL)
    solution_str = re.sub(r"<\|im_start\|>user.*?<\|im_end\|>", "", solution_str, flags=re.DOTALL)

    format_valid = validate_response_structure(solution_str)
    
    matches = list(re.finditer(r'<answer>(.*?)</answer>', processed_str, re.DOTALL))

    try:   
        final_answer = int(matches[-1].group(1).strip())
    except:
        final_answer = -1

    if final_answer == ground_truth['target']:
        answer_score = answer_reward
        if not format_valid:
            format_score = -format_reward
        else:
            format_score = format_reward
    else:
        answer_score = -answer_reward
        format_score = -format_reward
    

    print("\n" + "-"*80)
    print(f" Final Score ".center(80, '-'))
    print(f"  Format: {format_score}")
    print(f"  Answer: {answer_score}")
    print(f"  Total: {total_score}")
    print("="*80 + "\n")

    return total_score
