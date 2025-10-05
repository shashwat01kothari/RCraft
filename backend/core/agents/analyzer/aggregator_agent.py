import json

class AggregatorAgent:
    """Combines scores and feedback from all agents into a final report."""

    def __init__(self):
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
                result = json.loads(result_json)
                score = result.get('score', 0)
                fb = result.get('feedback', '')

                # Scale score (1-10) to the category's max possible points
                category_scores[category] = round((score / 10) * (self.weights[category] * 100), 1)
                if fb:
                    feedback_summary[category] = fb
                    recommendations.add(fb)
            except (json.JSONDecodeError, TypeError):
                category_scores[category] = 0
                feedback_summary[category] = f"Error processing the '{category}' category."

        # As noted, these are placeholders until their prompts are implemented
        category_scores['structure'] = 12.0
        category_scores['language'] = 7.0
        category_scores['ats'] = 8.0

        # Calculate final score out of 100
        overall_score = sum(category_scores.values())

        output = {
            "overall_score": round(overall_score),
            "category_scores": category_scores,
            "feedback": feedback_summary,
            "recommendations": sorted(list(recommendations))
        }

        return json.dumps(output, indent=2)