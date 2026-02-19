import requests
import time

BARDO_URL = "http://127.0.0.1:5001/listen"

historia = [
    "Arion y Lyra se adentran en el Bosque Tenebroso.",
    "El sol se oculta y la oscuridad lo envuelve todo.",
    "De repente, un grupo de goblins les ataca desde las sombras.",
    "Arion desenvaina su espada y se lanza a la carga.",
    "Lyra, por su parte, prepara un hechizo de luz.",
    "El hechizo de Lyra ilumina el claro y ciega a los goblins.",
    "Arion aprovecha la confusión y derrota a dos de ellos.",
    "Los goblins restantes huyen despavoridos.",
    "Arion y Lyra continuan su camino, más alerta que antes."
]

def narrar_historia():
    for linea in historia:
        print(f"Narrador: {linea}")
        try:
            requests.post(BARDO_URL, json={"text": linea})
        except requests.exceptions.RequestException as e:
            print(f"No se pudo contactar a Bardo: {e}")
        time.sleep(3)

if __name__ == "__main__":
    narrar_historia()
