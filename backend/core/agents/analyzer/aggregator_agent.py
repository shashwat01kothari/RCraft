# aggregator_agent.py

import json

class AggregatorAgent:
    """Combines scores from the holistic LLM evaluation into a final report."""

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

    def aggregate_scores(self, holistic_eval_json: str, rule_feedback: dict) -> str:
        """Calculates the weighted score from a single, comprehensive JSON response."""
        category_scores = {}
        feedback_summary = {}
        recommendations = set(rule_feedback.values())

        try:
            evaluations = json.loads(holistic_eval_json)
            
            # Verify that the loaded JSON is a dictionary before proceeding.
            if not isinstance(evaluations, dict):
                raise TypeError(f"LLM response was not a valid JSON object, but a {type(evaluations).__name__}.")

            if "error" in evaluations:
                 raise ValueError(f"LLM analysis failed with an API error: {evaluations['error']}")

            for category, details in evaluations.items():
                if category not in self.weights:
                    continue
                
                score = details.get('score', 0)
                fb = details.get('feedback', '')

                max_points = self.weights[category] * 100
                category_scores[category] = round((score / 10) * max_points, 1)

                if fb:
                    feedback_summary[category] = fb
                    recommendations.add(fb)
        
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print(f"CRITICAL ERROR: Could not process the LLM's holistic response. {e}")
            for category in self.weights:
                category_scores[category] = 0
            feedback_summary["error"] = "Could not parse the complete AI analysis. The response was likely malformed or an error."

        overall_score = sum(category_scores.values())

        output = {
            "overall_score": round(overall_score),
            "category_scores": category_scores,
            "feedback": feedback_summary,
            "recommendations": sorted(list(recommendations))
        }

        return json.dumps(output, indent=2)