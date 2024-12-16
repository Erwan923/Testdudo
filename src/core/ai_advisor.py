import openai
from typing import Dict, List

class AIAdvisor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
    
    def analyze(self, results: Dict) -> List[str]:
        """Analyse les résultats avec GPT"""
        if not self.api_key:
            return ["Clé API non configurée"]
            
        prompt = self._format_results(results)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en sécurité offensive."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.split('\n')
        
    def _format_results(self, results: Dict) -> str:
        """Formate les résultats pour l'IA"""
        return f"""Analyse ces résultats de test de sécurité :
        
        Résultats : {results}
        
        Quelles sont les prochaines étapes recommandées ?"""