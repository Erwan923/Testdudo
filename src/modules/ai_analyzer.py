import openai
import base64
from typing import Dict
from pathlib import Path

class AIAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def analyze_results(self, results: Dict) -> Dict:
        if not self.api_key:
            return {'error': 'No API key configured'}

        try:
            # Analyze text results
            text_analysis = self._analyze_text(results)
            
            # Analyze screenshots if available
            screenshots = self._find_screenshots()
            vision_analysis = self._analyze_screenshots(screenshots)

            return {
                'text_analysis': text_analysis,
                'vision_analysis': vision_analysis
            }
        except Exception as e:
            return {'error': str(e)}

    def _analyze_text(self, results: Dict) -> Dict:
        prompt = self._format_prompt(results)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Expert en sécurité offensive"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def _analyze_screenshots(self, screenshots: list) -> Dict:
        analyses = {}
        for screenshot in screenshots:
            base64_image = self._encode_image(screenshot)
            
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyse cette capture d'écran."},
                            {"type": "image_url",
                             "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                        ]
                    }
                ]
            )
            
            analyses[screenshot.name] = response.choices[0].message.content
        return analyses

    def _format_prompt(self, results: Dict) -> str:
        return f"""Analyse ces résultats et fournis :
1. Vulnérabilités détectées
2. Recommandations d'exploitation
3. Prochaines étapes suggérées

Résultats : {results}"""

    def _find_screenshots(self) -> list:
        screenshots_dir = Path('screenshots')
        if not screenshots_dir.exists():
            return []
        return list(screenshots_dir.glob('*.png'))

    def _encode_image(self, image_path: Path) -> str:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')