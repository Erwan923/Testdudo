import typer
from rich.console import Console
from typing import Optional
from .attack_manager import AttackManager
from .ai_advisor import AIAdvisor

app = typer.Typer()
console = Console()

@app.command()
def attack(
    target: str = typer.Argument(..., help="Cible à analyser"),
    mode: str = typer.Option("full", help="Mode : full, recon, network, web"),
    ai: bool = typer.Option(True, help="Utiliser l'IA pour l'analyse")
):
    """Lance une attaque automatisée"""
    console.print(f"[⚔️] Démarrage de l'attaque sur {target}")
    
    try:
        manager = AttackManager()
        results = manager.execute_attack(target, mode)
        
        if ai:
            advisor = AIAdvisor()
            recommendations = advisor.analyze(results)
            console.print("[🤖] Recommandations IA :")
            for rec in recommendations:
                console.print(f"- {rec}")
                
    except Exception as e:
        console.print(f"[red]Erreur: {str(e)}[/red]")