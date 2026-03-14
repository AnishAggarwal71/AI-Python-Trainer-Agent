from skills import get_available_skills
from prompts import explain_skill_prompt, generate_exercise_prompt, evaluate_answer_prompt
from llm import LLMClient


class LearningAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.completed_skills = []


    def get_next_skill(self):

        available = get_available_skills(self.completed_skills)

        if not available:
            return None

        return available[0]


    def explain_skill(self, skill):

        prompt = explain_skill_prompt.format(
            skill_name=skill.name,
            skill_description=skill.description
        )

        return self.llm.generate(prompt)


    def generate_exercise(self, skill):

        prompt = generate_exercise_prompt.format(
            skill_name=skill.name,
            skill_description=skill.description
        )

        return self.llm.generate(prompt)


    def evaluate_answer(self, skill, exercise, user_answer):

        prompt = evaluate_answer_prompt.format(
            skill_name=skill.name,
            exercise=exercise,
            user_answer=user_answer
        )

        return self.llm.generate(prompt)


    def mark_completed(self, skill):

        if skill.id not in self.completed_skills:
            self.completed_skills.append(skill.id)