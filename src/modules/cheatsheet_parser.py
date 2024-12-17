import yaml
from pathlib import Path
from typing import Dict, List

class CheatsheetParser:
    def __init__(self):
        self.attack_types = {
            'recon': ['passive', 'active'],
            'scan': ['port', 'vulnerability'],
            'exploit': ['web', 'network', 'system']
        }

    def parse_cheatsheet(self, phase: str) -> List[Dict]:
        path = Path(f'cheatsheets/{phase}.md')
        if not path.exists():
            raise FileNotFoundError(f'Cheatsheet not found: {path}')

        with open(path, 'r') as f:
            content = f.read()

        return self._parse_content(content)

    def _parse_content(self, content: str) -> List[Dict]:
        commands = []
        current_section = None

        for line in content.split('\n'):
            if line.startswith('###'):
                current_section = line.strip('# ')
            elif line.strip().startswith('*') and '`' in line:
                cmd = self._parse_command_line(line, current_section)
                if cmd:
                    commands.append(cmd)

        return commands

    def _parse_command_line(self, line: str, section: str) -> Dict:
        try:
            cmd_part = line.split('`')[1]
            metadata = self._parse_metadata(line)

            return {
                'command': cmd_part,
                'section': section,
                'metadata': metadata
            }
        except Exception:
            return None

    def _parse_metadata(self, line: str) -> Dict:
        metadata = {
            'severity': 'medium',
            'noisy': False,
            'requires_root': False
        }

        if '#' in line and '{' in line:
            try:
                yaml_part = line.split('#')[1].strip()
                if yaml_part.startswith('{') and yaml_part.endswith('}'):
                    parsed = yaml.safe_load(yaml_part)
                    if isinstance(parsed, dict):
                        metadata.update(parsed)
            except Exception:
                pass

        return metadata