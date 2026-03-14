explain_skill_prompt = """
You are an expert programming instructor.

Explain the following skill clearly for a learner.

Skill Name:
{skill_name}

Description:
{skill_description}

Instructions:
- Explain the concept simply and clearly.
- Break the explanation into key ideas.
- Provide one practical example.
- Keep the explanation concise.

Return your answer in the following JSON format:

{{
  "summary": "short explanation of the concept",
  "key_points": ["point1", "point2", "point3"],
  "example": "short practical example"
}}
"""

generate_exercise_prompt = """
You are an instructor creating a practice exercise.

Skill:
{skill_name}

Description:
{skill_description}

Generate a short coding exercise.

Requirements:
- The exercise should take about 5 minutes.
- Focus only on the target skill.
- Do not include the solution.

Return output in JSON format:

{{
  "title": "exercise title",
  "instructions": "clear description of the problem",
  "example_input": "optional example",
  "example_output": "optional example"
}}
"""


evaluate_answer_prompt = """
You are evaluating a learner's answer.

Skill:
{skill_name}

Exercise:
{exercise}

Learner Answer:
{user_answer}

Evaluate whether the learner demonstrated understanding.

Return JSON only:

{{
  "score": 1-5,
  "correct": true/false,
  "feedback": "short explanation",
  "improvement_tip": "what the learner should improve"
}}
"""