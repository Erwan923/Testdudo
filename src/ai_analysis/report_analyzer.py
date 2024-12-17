import openai
from typing import Dict, List

class ReportAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def analyze_scan_results(self, results: Dict) -> Dict:
        """
        Analyse les résultats de scan avec GPT-4
        """
        prompt = self._format_results_for_analysis(results)
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en sécurité offensive."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            'analysis': response.choices[0].message.content,
            'raw_results': results
        }

    def _format_results_for_analysis(self, results: Dict) -> str:
        return f"""
Analyse ces résultats de test de sécurité et fournis :
1. Les vulnérabilités détectées (par ordre de sévérité)
2. Les recommandations d'exploitation
3. Les précautions à prendre
4. Les étapes suivantes suggérées

Résultats :
{results}
"""