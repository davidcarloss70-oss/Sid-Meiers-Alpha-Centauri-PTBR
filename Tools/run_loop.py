import subprocess
import time

while True:
    print("Iniciando translate_game.py...")
    process = subprocess.Popen(["uv", "run", "python", "-u", "translate_game.py"])
    try:
        process.wait(timeout=60)
    except subprocess.TimeoutExpired:
        print("Processo travado (timeout de 60s). Matando e reiniciando...")
        process.kill()
        process.wait()
        continue

    if process.returncode == 0:
        print("Concluido com sucesso!")
        break
    else:
        print(f"Falhou com {process.returncode}, reiniciando...")
        time.sleep(2)
