#!/usr/bin/env python3

import re
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class Command:
    """Représente une commande avec ses métadonnées"""
    raw: str                     # Commande brute
    tool: str                    # Nom de l'outil
    arguments: List[str]         # Arguments de la commande
    description: str             # Description de la commande
    prerequisites: List[str]     # Prérequis pour la commande
    threat_level: str           # Niveau de menace de la commande

@dataclass
class Section:
    """Représente une section de la cheatsheet"""
    title: str                  # Titre de la section
    description: str            # Description de la section
    commands: List[Command]     # Commandes dans la section
    subsections: List['Section'] # Sous-sections

class MarkdownParser:
    """Parser avancé pour les cheatsheets markdown"""

    def __init__(self):
        self.logger = logging.getLogger("Testudo.MarkdownParser")
        self.current_section = None
        self.sections = []

    def parse_file(self, filepath: Path) -> List[Section]:
        """Parse un fichier markdown complet"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_content(content)
        except Exception as e:
            self.logger.error(f"Erreur lors du parsing du fichier {filepath}: {str(e)}")
            raise

    def parse_content(self, content: str) -> List[Section]:
        """Parse le contenu markdown"""
        lines = content.split('\n')
        self.sections = []
        current_section = None
        current_command = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Analyse des titres de section
            if line.startswith('#'):
                level = len(re.match(r'^#+', line).group())
                title = line.strip('#').strip()
                
                if level == 1:
                    current_section = Section(title, "", [], [])
                    self.sections.append(current_section)
                elif level == 2 and current_section:
                    subsection = Section(title, "", [], [])
                    current_section.subsections.append(subsection)
                    current_section = subsection

            # Analyse des commandes
            elif line.startswith('`'):
                current_command = self._parse_command(line)
                if current_section:
                    current_section.commands.append(current_command)

            # Analyse des descriptions
            elif current_command and not line.startswith(('#', '`')):
                current_command.description += line + "\n"

        return self.sections

    def _parse_command(self, line: str) -> Command:
        """Parse une ligne de commande avec ses métadonnées"""
        # Extrait la commande des backticks
        cmd_match = re.match(r'`([^`]+)`(?:\s+#\s*(.*))?', line)
        if not cmd_match:
            raise ValueError(f"Format de commande invalide: {line}")

        raw_cmd = cmd_match.group(1)
        comment = cmd_match.group(2) or ""

        # Parse les métadonnées de la commande
        metadata = self._parse_command_metadata(comment)
        
        # Sépare la commande en outil et arguments
        parts = raw_cmd.split()
        tool = parts[0]
        arguments = parts[1:] if len(parts) > 1 else []

        return Command(
            raw=raw_cmd,
            tool=tool,
            arguments=arguments,
            description=metadata.get('description', ''),
            prerequisites=metadata.get('prerequisites', []),
            threat_level=metadata.get('threat_level', 'medium')
        )

    def _parse_command_metadata(self, comment: str) -> Dict[str, Any]:
        """Parse les métadonnées d'une commande depuis son commentaire"""
        metadata = {
            'description': '',
            'prerequisites': [],
            'threat_level': 'medium'
        }

        if not comment:
            return metadata

        # Recherche des métadonnées dans le format YAML inline
        yaml_match = re.search(r'{([^}]+)}', comment)
        if yaml_match:
            try:
                yaml_data = yaml.safe_load(yaml_match.group(1))
                if isinstance(yaml_data, dict):
                    metadata.update(yaml_data)
            except yaml.YAMLError as e:
                self.logger.warning(f"Erreur de parsing YAML: {str(e)}")

        # Si pas de YAML, utilise le commentaire comme description
        else:
            metadata['description'] = comment.strip()

        return metadata

    def generate_ansible_tasks(self, section: Section) -> List[Dict]:
        """Génère des tâches Ansible à partir d'une section"""
        tasks = []
        for command in section.commands:
            task = {
                'name': f"Execute {command.tool}",
                'command': command.raw,
                'register': f"result_{command.tool}",
                'ignore_errors': True,
                'tags': ['security', command.threat_level],
            }
            
            # Ajoute les conditions basées sur les prérequis
            if command.prerequisites:
                task['when'] = ' and '.join(command.prerequisites)
            
            tasks.append(task)
            
            # Ajoute une tâche de vérification des résultats
            tasks.append({
                'name': f"Check {command.tool} results",
                'debug':
                    'msg': "{{ result_" + command.tool + " }}"
                'when': f"result_{command.tool} is defined"
            })
        
        return tasks

    def generate_documentation(self) -> str:
        """Génère une documentation structurée des commandes"""
        doc = []
        for section in self.sections:
            doc.append(f"# {section.title}\n")
            if section.description:
                doc.append(f"{section.description}\n")
            
            for command in section.commands:
                doc.append(f"## {command.tool}")
                doc.append(f"Command: `{command.raw}`")
                if command.description:
                    doc.append(f"Description: {command.description}")
                if command.prerequisites:
                    doc.append(f"Prerequisites: {', '.join(command.prerequisites)}")
                doc.append(f"Threat Level: {command.threat_level}\n")
            
            doc.append("---\n")
        
        return "\n".join(doc)