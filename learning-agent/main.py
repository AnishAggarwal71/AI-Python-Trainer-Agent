from agent import LearningAgent


def main():

    agent = LearningAgent()

    while True:

        skill = agent.get_next_skill()

        if not skill:
            print("You have completed all skills!")
            break

        print(f"\nNext Skill: {skill.name}\n")

        explanation = agent.explain_skill(skill)
        print("Explanation:")
        print(explanation)

        exercise = agent.generate_exercise(skill)
        print("\nExercise:")
        print(exercise)

        user_answer = input("\nYour answer: ")

        evaluation = agent.evaluate_answer(skill, exercise, user_answer)

        print("\nEvaluation:")
        print(evaluation)

        if "correct" in evaluation.lower():
            agent.mark_completed(skill)
            print("\nSkill completed!")


if __name__ == "__main__":
    main()