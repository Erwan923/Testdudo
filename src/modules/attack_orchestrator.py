import subprocess
import yaml
from typing import Dict, List
from datetime import datetime

class AttackOrchestrator:
    def __init__(self):
        self.current_phase = None
        self.results = []

    def execute_commands(self, target: str, commands: List[Dict]) -> Dict:
        playbook = self._generate_playbook(target, commands)
        results = self._execute_playbook(playbook)
        return self._process_results(results)

    def _generate_playbook(self, target: str, commands: List[Dict]) -> str:
        tasks = []
        for cmd in commands:
            task = {
                'name': f"Execute: {cmd['command']}",
                'command': cmd['command'].format(target=target),
                'register': 'command_result'
            }
            
            if cmd['metadata'].get('requires_root'):
                task['become'] = True
                
            tasks.append(task)

        playbook = [{
            'hosts': 'localhost',
            'tasks': tasks
        }]

        playbook_path = f'playbooks/attack_{datetime.now().strftime("%Y%m%d_%H%M%S")}.yml'
        with open(playbook_path, 'w') as f:
            yaml.dump(playbook, f)

        return playbook_path

    def _execute_playbook(self, playbook_path: str) -> Dict:
        try:
            result = subprocess.run(
                ['ansible-playbook', playbook_path],
                capture_output=True,
                text=True
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _process_results(self, results: Dict) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'results': results
        }