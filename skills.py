"""
We use a Directed Acyclic Graph (DAG) because learning systems
must never create circular dependencies.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Skill:
    # Unique identifier for the skill
    id: str

    # Human-readable name of the skill
    name: str

    # Detailed description of what the skill does or covers
    description: str

    # List of skill IDs that must be learned before this skill
    dependencies: List[str]

    # Difficulty level on a numeric scale (e.g., 1–10)
    difficulty: int


SKILLS: dict[str, Skill] = {
    "python_variables": Skill(
        id="python_variables",
        name="Python Variables",
        description="Learn how to declare, assign, and use variables in Python",
        dependencies=[],
        difficulty=1
    ),

    "python_loops": Skill(
        id="python_loops",
        name="Python Loops",
        description="Master for and while loops for iterating over data",
        dependencies=["python_variables"],
        difficulty=3
    ),

    "python_functions": Skill(
        id="python_functions",
        name="Python Functions",
        description="Understand how to define and call functions with parameters and return values",
        dependencies=["python_variables"],
        difficulty=3
    ),

    "python_lists": Skill(
        id="python_lists",
        name="Python Lists",
        description="Learn to create and manipulate lists, including indexing and slicing",
        dependencies=["python_variables"],
        difficulty=2
    ),

    "python_dicts": Skill(
        id="python_dicts",
        name="Python Dictionaries",
        description="Understand key-value pairs and how to work with dictionaries",
        dependencies=["python_lists"],
        difficulty=3
    )
}

# Helper Function

def get_available_skills(completed_skills: List[str]) -> List[Skill]:
    """
    Returns a list of skills that can be learned next based on completed skills.
    A skill is available if all its dependencies have been completed.
    """
    available_skills = []
    
    # Iterate through all skills in the SKILLS dictionary
    for skill in SKILLS.values():
        # Skip skills that have already been completed
        if skill.id in completed_skills:
            continue
        
        # Check if all dependencies for this skill are satisfied
        # (i.e., all dependencies are in the completed_skills list)
        if all(dep in completed_skills for dep in skill.dependencies):
            # If all dependencies are met, add this skill to available list
            available_skills.append(skill)
    
    return available_skills