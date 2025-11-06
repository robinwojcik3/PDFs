#!/usr/bin/env python3
"""
Script de démarrage pour PDF Explorer avec fallbacks robustes.
Démarre le backend FastAPI et le frontend React avec gestion d'erreurs complète.
"""

import subprocess
import sys
import os
import socket
import time
import platform
import signal
from pathlib import Path
from typing import Optional, Tuple

# Configuration par défaut
DEFAULT_BACKEND_PORT = 8000
DEFAULT_FRONTEND_PORT = 5173
BACKEND_FALLBACK_PORTS = [8000, 8001, 8080, 8888, 9000]
FRONTEND_FALLBACK_PORTS = [5173, 5174, 3000, 3001, 4000]

# Couleurs pour les logs
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

    @staticmethod
    def disable_on_windows():
        """Désactive les couleurs sur Windows si nécessaire."""
        if platform.system() == 'Windows':
            Colors.GREEN = Colors.BLUE = Colors.YELLOW = Colors.RED = Colors.BOLD = Colors.NC = ''

# Désactiver couleurs sur Windows par défaut
Colors.disable_on_windows()

def log(message: str, color: str = Colors.NC):
    """Log avec couleur."""
    print(f"{color}{message}{Colors.NC}")

def log_success(message: str):
    """Log de succès."""
    log(f"✓ {message}", Colors.GREEN)

def log_info(message: str):
    """Log d'information."""
    log(f"ℹ {message}", Colors.BLUE)

def log_warning(message: str):
    """Log d'avertissement."""
    log(f"⚠ {message}", Colors.YELLOW)

def log_error(message: str):
    """Log d'erreur."""
    log(f"✗ {message}", Colors.RED)

def is_port_available(port: int) -> bool:
    """Vérifie si un port est disponible."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.bind(('', port))
            return True
    except (OSError, socket.error):
        return False

def find_available_port(preferred_ports: list) -> Optional[int]:
    """Trouve un port disponible parmi une liste."""
    for port in preferred_ports:
        if is_port_available(port):
            return port

    # Si aucun port préféré n'est disponible, chercher un port aléatoire
    log_warning("Aucun port préféré disponible, recherche d'un port libre...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    except Exception as e:
        log_error(f"Impossible de trouver un port libre : {e}")
        return None

def check_python_version() -> bool:
    """Vérifie la version de Python."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        log_success(f"Python {version.major}.{version.minor}.{version.micro} détecté")
        return True
    else:
        log_warning(f"Python {version.major}.{version.minor} détecté. Python 3.9+ recommandé.")
        return version.major >= 3 and version.minor >= 7

def check_node_installed() -> bool:
    """Vérifie si Node.js est installé."""
    try:
        result = subprocess.run(['node', '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            log_success(f"Node.js {version} détecté")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    log_error("Node.js n'est pas installé ou n'est pas dans le PATH")
    log_info("Téléchargez Node.js depuis : https://nodejs.org/")
    return False

def check_npm_installed() -> bool:
    """Vérifie si npm est installé."""
    try:
        result = subprocess.run(['npm', '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            log_success(f"npm {version} détecté")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    log_error("npm n'est pas installé ou n'est pas dans le PATH")
    return False

def setup_backend_venv() -> Tuple[bool, Optional[str]]:
    """Configure l'environnement virtuel Python pour le backend."""
    backend_dir = Path(__file__).parent / 'backend'
    venv_dir = backend_dir / 'venv'

    if not backend_dir.exists():
        log_error(f"Le dossier backend n'existe pas : {backend_dir}")
        return False, None

    # Créer le venv si nécessaire
    if not venv_dir.exists():
        log_info("Création de l'environnement virtuel Python...")
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)],
                         check=True,
                         timeout=60)
            log_success("Environnement virtuel créé")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            log_error(f"Échec de la création du venv : {e}")
            return False, None

    # Déterminer le chemin de l'exécutable Python dans le venv
    if platform.system() == 'Windows':
        python_exe = venv_dir / 'Scripts' / 'python.exe'
        pip_exe = venv_dir / 'Scripts' / 'pip.exe'
    else:
        python_exe = venv_dir / 'bin' / 'python'
        pip_exe = venv_dir / 'bin' / 'pip'

    if not python_exe.exists():
        log_error(f"Python venv non trouvé : {python_exe}")
        return False, None

    # Installer les dépendances
    requirements_file = backend_dir / 'requirements.txt'
    if requirements_file.exists():
        log_info("Installation des dépendances Python...")
        try:
            subprocess.run([str(pip_exe), 'install', '-q', '-r', str(requirements_file)],
                         check=True,
                         timeout=300)
            log_success("Dépendances Python installées")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            log_warning(f"Avertissement lors de l'installation des dépendances : {e}")
            log_info("Tentative de continuer malgré tout...")

    return True, str(python_exe)

def setup_frontend_deps() -> bool:
    """Installe les dépendances Node.js pour le frontend."""
    frontend_dir = Path(__file__).parent / 'frontend'
    node_modules = frontend_dir / 'node_modules'

    if not frontend_dir.exists():
        log_error(f"Le dossier frontend n'existe pas : {frontend_dir}")
        return False

    # Installer les dépendances si nécessaire
    if not node_modules.exists():
        log_info("Installation des dépendances Node.js...")
        try:
            subprocess.run(['npm', 'install'],
                         cwd=str(frontend_dir),
                         check=True,
                         timeout=300)
            log_success("Dépendances Node.js installées")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            log_error(f"Échec de l'installation des dépendances npm : {e}")
            return False
    else:
        log_success("Dépendances Node.js déjà installées")

    return True

def start_backend(python_exe: str, port: int) -> Optional[subprocess.Popen]:
    """Démarre le serveur backend FastAPI."""
    backend_dir = Path(__file__).parent / 'backend'

    log_info(f"Démarrage du backend FastAPI sur le port {port}...")

    try:
        # Commande pour démarrer uvicorn
        cmd = [
            python_exe,
            '-m', 'uvicorn',
            'app.main:app',
            '--reload',
            '--host', '0.0.0.0',
            '--port', str(port)
        ]

        process = subprocess.Popen(
            cmd,
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Attendre un peu pour vérifier que le processus démarre
        time.sleep(2)

        if process.poll() is None:
            log_success(f"Backend démarré sur http://localhost:{port}")
            log_info(f"Documentation API : http://localhost:{port}/docs")
            return process
        else:
            stdout, stderr = process.communicate(timeout=1)
            log_error(f"Le backend s'est arrêté immédiatement")
            if stderr:
                log_error(f"Erreur : {stderr[:200]}")
            return None

    except Exception as e:
        log_error(f"Échec du démarrage du backend : {e}")
        return None

def start_frontend(port: int, backend_port: int) -> Optional[subprocess.Popen]:
    """Démarre le serveur frontend React."""
    frontend_dir = Path(__file__).parent / 'frontend'

    log_info(f"Démarrage du frontend React sur le port {port}...")

    try:
        # Créer un environnement avec le port du backend
        env = os.environ.copy()
        env['VITE_API_URL'] = f'http://localhost:{backend_port}'
        env['PORT'] = str(port)

        # Sur Windows, utiliser npm.cmd
        npm_cmd = 'npm.cmd' if platform.system() == 'Windows' else 'npm'

        process = subprocess.Popen(
            [npm_cmd, 'run', 'dev', '--', '--port', str(port), '--host'],
            cwd=str(frontend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )

        # Attendre un peu pour vérifier que le processus démarre
        time.sleep(3)

        if process.poll() is None:
            log_success(f"Frontend démarré sur http://localhost:{port}")
            return process
        else:
            stdout, stderr = process.communicate(timeout=1)
            log_error(f"Le frontend s'est arrêté immédiatement")
            if stderr:
                log_error(f"Erreur : {stderr[:200]}")
            return None

    except Exception as e:
        log_error(f"Échec du démarrage du frontend : {e}")
        return None

def wait_for_service(port: int, max_wait: int = 30) -> bool:
    """Attend qu'un service soit disponible sur un port."""
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(('localhost', port))
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(1)
    return False

def cleanup_processes(processes: list):
    """Arrête proprement tous les processus."""
    log_info("Arrêt des services...")
    for process in processes:
        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    log_success("Services arrêtés")

def main():
    """Fonction principale."""
    processes = []

    # Signal handler pour arrêt propre
    def signal_handler(sig, frame):
        print()  # Nouvelle ligne après Ctrl+C
        cleanup_processes(processes)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    if platform.system() != 'Windows':
        signal.signal(signal.SIGTERM, signal_handler)

    # En-tête
    log("=" * 60, Colors.BOLD)
    log("🚀 Démarrage de PDF Explorer", Colors.BOLD)
    log("=" * 60, Colors.BOLD)
    print()

    # Vérifications préliminaires
    log_info("Vérification des prérequis...")

    if not check_python_version():
        log_error("Version Python incompatible")
        return 1

    # Trouver les ports disponibles
    backend_port = find_available_port(BACKEND_FALLBACK_PORTS)
    if not backend_port:
        log_error("Impossible de trouver un port disponible pour le backend")
        return 1

    if backend_port != DEFAULT_BACKEND_PORT:
        log_warning(f"Port {DEFAULT_BACKEND_PORT} occupé, utilisation du port {backend_port}")

    frontend_port = find_available_port(FRONTEND_FALLBACK_PORTS)
    if not frontend_port:
        log_error("Impossible de trouver un port disponible pour le frontend")
        return 1

    if frontend_port != DEFAULT_FRONTEND_PORT:
        log_warning(f"Port {DEFAULT_FRONTEND_PORT} occupé, utilisation du port {frontend_port}")

    print()

    # Configuration du backend
    log_info("Configuration du backend...")
    success, python_exe = setup_backend_venv()
    if not success:
        log_error("Échec de la configuration du backend")
        log_info("Fallback : Tentative d'utilisation de Python système...")
        python_exe = sys.executable

    print()

    # Démarrage du backend
    backend_process = start_backend(python_exe, backend_port)
    if backend_process:
        processes.append(backend_process)

        # Attendre que le backend soit prêt
        log_info("Attente du démarrage du backend...")
        if wait_for_service(backend_port, max_wait=20):
            log_success("Backend prêt !")
        else:
            log_warning("Le backend met du temps à démarrer, mais continuons...")
    else:
        log_error("Impossible de démarrer le backend")
        log_warning("L'application continuera sans backend (mode frontend seul)")

    print()

    # Vérification de Node.js et npm
    if not check_node_installed() or not check_npm_installed():
        log_error("Node.js ou npm manquant, impossible de démarrer le frontend")
        if backend_process:
            log_info(f"Le backend REST API est accessible sur http://localhost:{backend_port}/docs")
            log_info("Appuyez sur Ctrl+C pour arrêter...")
            try:
                backend_process.wait()
            except KeyboardInterrupt:
                pass
        cleanup_processes(processes)
        return 1

    print()

    # Configuration du frontend
    log_info("Configuration du frontend...")
    if not setup_frontend_deps():
        log_error("Échec de la configuration du frontend")
        cleanup_processes(processes)
        return 1

    print()

    # Démarrage du frontend
    frontend_process = start_frontend(frontend_port, backend_port)
    if frontend_process:
        processes.append(frontend_process)

        # Attendre que le frontend soit prêt
        log_info("Attente du démarrage du frontend...")
        if wait_for_service(frontend_port, max_wait=30):
            log_success("Frontend prêt !")
        else:
            log_warning("Le frontend met du temps à démarrer...")
    else:
        log_error("Impossible de démarrer le frontend")

    print()
    log("=" * 60, Colors.BOLD)
    log_success("✓ Application démarrée !")
    log("=" * 60, Colors.BOLD)
    print()

    # Afficher les URLs
    if frontend_process:
        log(f"📖 Application web : {Colors.GREEN}http://localhost:{frontend_port}{Colors.NC}", Colors.BOLD)
    if backend_process:
        log(f"📚 Documentation API : {Colors.BLUE}http://localhost:{backend_port}/docs{Colors.NC}", Colors.BOLD)

    print()
    log_info("Appuyez sur Ctrl+C pour arrêter les services...")
    print()

    # Attendre l'arrêt
    try:
        while True:
            # Vérifier si les processus sont toujours en vie
            if backend_process and backend_process.poll() is not None:
                log_error("Le backend s'est arrêté de manière inattendue")
                break
            if frontend_process and frontend_process.poll() is not None:
                log_error("Le frontend s'est arrêté de manière inattendue")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print()  # Nouvelle ligne

    cleanup_processes(processes)
    return 0

if __name__ == '__main__':
    sys.exit(main())
