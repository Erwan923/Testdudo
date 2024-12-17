#!/usr/bin/env python3

import argparse
import subprocess
import yaml
import json
import os
import logging
import openai
import base64
from typing import List, Dict
from datetime import datetime

class Testdudo:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.current_phase = None
        self.results = {}
        
        # Configuration des APIs
        self.github_token = os.getenv("GITHUB_TOKEN", self.config.get("github_token"))
        self.openai_api_key = os.getenv("OPENAI_API_KEY", self.config.get("openai_api_key"))
        openai.api_key = self.openai_api_key

    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("Testdudo")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_config(self, config_path: str) -> Dict:
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def _load_cheatsheet(self, phase: str) -> List[str]:
        """Charge les commandes depuis la cheatsheet GitHub"""
        try:
            repo_name = "Erwan923/Testdudo"
            file_path = f"cheatsheets/{phase}.md"
            headers = {'Authorization': f'token {self.github_token}'}
            api_url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"
            
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                content = base64.b64decode(response.json()['content']).decode('utf-8')
                return self._parse_markdown_commands(content, phase)
            else:
                self.logger.error(f"Failed to fetch cheatsheet: {response.status_code}")
                return []
        except Exception as e:
            self.logger.error(f"Error loading cheatsheet: {e}")
            return []

    def _parse_markdown_commands(self, content: str, phase: str) -> List[str]:
        """Parse les commandes de la cheatsheet"""
        commands = []
        current_section = None
        
        for line in content.split('\n'):
            if line.startswith('### '):
                current_section = line.strip('# ').lower()
            elif line.startswith('`') and current_section:
                cmd = line.strip('`').split('#')[0].strip()
                commands.append(cmd)
                
        return commands

    def _generate_playbook(self, commands: List[str], target: str) -> str:
        """Génère un playbook Ansible"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        playbook_path = f'playbooks/testdudo_{timestamp}.yml'
        report_path = f'reports/scan_{timestamp}.xml'
        
        tasks = []
        for cmd in commands:
            tasks.append({
                'name': f"Execute: {cmd}",
                'command': f"{cmd} {target} -oX {report_path}",
                'register': 'command_result',
                'ignore_errors': True
            })
            
        playbook = [{
            'hosts': 'localhost',
            'gather_facts': False,
            'tasks': tasks
        }]
        
        os.makedirs('playbooks', exist_ok=True)
        with open(playbook_path, 'w') as f:
            yaml.safe_dump(playbook, f)
            
        return playbook_path, report_path

    def _analyze_results(self, report_path: str) -> Dict:
        """Analyse les résultats avec GPT-4"""
        try:
            with open(report_path, 'r') as f:
                results = f.read()
                
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un expert en sécurité offensive."},
                    {"role": "user", "content": f"""Analyse ces résultats de scan et suggère :
                    1. Les vulnérabilités potentielles
                    2. Les prochaines étapes recommandées
                    3. Les précautions à prendre
                    
                    Résultats :
                    {results}
                    """}
                ]
            )
            
            analysis = response.choices[0].message.content
            return {"analysis": analysis, "raw_results": results}
            
        except Exception as e:
            self.logger.error(f"Error analyzing results: {e}")
            return {"error": str(e)}

    def execute_scan(self, target: str, phase: str = "recon"):
        """Exécute un scan complet"""
        self.logger.info(f"Starting {phase} phase on {target}")
        
        try:
            # 1. Charger les commandes
            commands = self._load_cheatsheet(phase)
            if not commands:
                raise Exception("No commands found for this phase")
                
            # 2. Générer et exécuter le playbook
            playbook_path, report_path = self._generate_playbook(commands, target)
            subprocess.run(['ansible-playbook', playbook_path], check=True)
            
            # 3. Analyser les résultats
            analysis = self._analyze_results(report_path)
            
            # 4. Sauvegarder les résultats
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_path = f'reports/analysis_{timestamp}.json'
            os.makedirs('reports', exist_ok=True)
            
            with open(results_path, 'w') as f:
                json.dump(analysis, f, indent=2)
                
            self.logger.info(f"Analysis saved to {results_path}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error during scan execution: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Testdudo - Security Testing Tool")
    parser.add_argument('--target', required=True, help="Target to scan")
    parser.add_argument('--phase', choices=['recon', 'scan', 'exploit'], 
                       default='recon', help="Phase to execute")
    args = parser.parse_args()
    
    testdudo = Testdudo()
    results = testdudo.execute_scan(args.target, args.phase)
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()