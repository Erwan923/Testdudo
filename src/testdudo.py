import argparse
import yaml
import json
import logging
import openai
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from modules.cheatsheet_parser import CheatsheetParser
from modules.attack_orchestrator import AttackOrchestrator
from modules.ai_analyzer import AIAnalyzer

class Testdudo:
    def __init__(self, config_path: str = 'config.yaml'):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.parser = CheatsheetParser()
        self.orchestrator = AttackOrchestrator()
        self.ai_analyzer = AIAnalyzer(self.config.get('openai_api_key'))
        
    def execute_attack(self, target: str, phase: str) -> Dict:
        # Main attack execution logic
        self.logger.info(f'Starting {phase} attack on {target}')
        
        try:
            # 1. Parse relevant cheatsheets
            commands = self.parser.parse_cheatsheet(phase)
            
            # 2. Generate and execute playbook
            results = self.orchestrator.execute_commands(target, commands)
            
            # 3. Analyze results with AI
            if self.config.get('ai_enabled'):
                analysis = self.ai_analyzer.analyze_results(results)
                results['ai_analysis'] = analysis
            
            # 4. Save results
            self._save_results(results)
            
            return results
            
        except Exception as e:
            self.logger.error(f'Attack failed: {str(e)}')
            raise
            
    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger('Testdudo')
        logger.setLevel(logging.INFO)
        return logger
        
    def _load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f'Error loading config: {str(e)}')
            return {}
            
    def _save_results(self, results: Dict):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = Path(f'results/attack_{timestamp}.json')
        path.parent.mkdir(exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(results, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True)
    parser.add_argument('--phase', choices=['recon', 'scan', 'exploit'])
    parser.add_argument('--no-ai', action='store_true')
    args = parser.parse_args()
    
    testdudo = Testdudo()
    results = testdudo.execute_attack(args.target, args.phase)
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()