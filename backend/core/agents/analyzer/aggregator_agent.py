# aggregator_agent.py

import json

class AggregatorAgent:
    """Combines scores and feedback from all agents into a final report."""

    def __init__(self):
        # The official weights for each category
        self.weights = {
            "structure": 0.15,
            "summary": 0.10,
            "experience": 0.25,
            "skills": 0.20,
            "language": 0.10,
            "ats": 0.10,
            "relevance": 0.10,
        }

    def aggregate_scores(self, llm_evals: dict, rule_feedback: dict) -> str:
        """Calculates the weighted score and formats the final JSON output."""
        category_scores = {}
        feedback_summary = {}
        recommendations = set(rule_feedback.values())

        for category, result_json in llm_evals.items():
            try:
                # Add a check for empty or invalid JSON string from the LLM
                if not result_json or not result_json.strip().startswith('{'):
                    raise json.JSONDecodeError("Empty or invalid JSON response", result_json, 0)

                result = json.loads(result_json)
                score = result.get('score', 0)
                fb = result.get('feedback', '')

                # Calculate the weighted score for the category
                # Max points for a category = weight * 100
                max_points = self.weights.get(category, 0) * 100
                category_scores[category] = round((score / 10) * max_points, 1)

                if fb:
                    feedback_summary[category] = fb
                    recommendations.add(fb) # Aggregate actionable feedback
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error for category '{category}': {e}. Response was: {result_json}")
                category_scores[category] = 0
                feedback_summary[category] = f"Could not process the AI's response for the '{category}' category."
            except TypeError as e:
                print(f"Type Error for category '{category}': {e}. Response was: {result_json}")
                category_scores[category] = 0
                feedback_summary[category] = f"Invalid data type in response for the '{category}' category."

        # --- PLACEHOLDERS ARE NOW REMOVED ---

        # Calculate final score out of 100
        overall_score = sum(category_scores.values())

        output = {
            "overall_score": round(overall_score),
            "category_scores": category_scores,
            "feedback": feedback_summary,
            "recommendations": sorted(list(recommendations))
        }

        return json.dumps(output, indent=2)