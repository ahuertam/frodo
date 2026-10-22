from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import random


@dataclass(frozen=True)
class EncounterInput:
    system: str
    module: str | None
    scene: str | None
    mode: str
    seed: str | None
    party: str
    emphasis: str
    keywords: str
    title: str
    hook: str
    objective: str
    opposition: str
    pressure: str
    twist: str
    terrain: str
    rewards: str
    kind: str = "escena"
    location: str = ""
    from_location: str = ""
    to_location: str = ""


@dataclass(frozen=True)
class Encounter:
    system: str
    source: str
    title: str
    hook: str
    objectives: list[str]
    opposition: list[str]
    terrain: list[str]
    pressure: str
    twist: str
    scaling_easier: str
    scaling_harder: str
    rewards: str
    beats: list[str]
    tags: list[str]
    kind: str = "escena"
    location: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# {self.title}")
        lines.append("")
        lines.append(f"**Sistema:** {self.system}")
        lines.append(f"**Fuente:** {self.source}")
        lines.append(f"**Tipo:** {self.kind}")
        if self.location:
            lines.append(f"**Localización:** {self.location}")
        lines.append("")
        lines.append(f"**Gancho:** {self.hook}")
        lines.append("")
        lines.append("## Objetivo(s)")
        for o in self.objectives:
            lines.append(f"- {o}")
        lines.append("")
        lines.append("## Oposición")
        for o in self.opposition:
            lines.append(f"- {o}")
        lines.append("")
        lines.append("## Terreno (5)")
        for t in self.terrain:
            lines.append(f"- {t}")
        lines.append("")
        lines.append("## Presión")
        lines.append(self.pressure)
        lines.append("")
        lines.append("## Giro")
        lines.append(self.twist)
        lines.append("")
        lines.append("## Escalado")
        lines.append(f"- Más fácil: {self.scaling_easier}")
        lines.append(f"- Más duro: {self.scaling_harder}")
        lines.append("")
        lines.append("## Recompensas / Consecuencias")
        lines.append(self.rewards)
        lines.append("")
        lines.append("## Beats (Inicio / Medio / Final)")
        for b in self.beats:
            lines.append(f"- {b}")
        if self.tags:
            lines.append("")
            lines.append("## Tags")
            lines.append(", ".join(self.tags))
        return "\n".join(lines).strip() + "\n"


LOCATIONS = [
    "Colmillo de Krayt (a bordo)",
    "Órbita de Ryloth",
    "Nabat (plataformas de aterrizaje)",
    "Nabat (subsuelo / mercado)",
    "Nabat (piso franco de Nyn)",
    "Tierras baldías de Ryloth (en deslizador)",
    "Guarida del lylek",
    "Nueva Meen (asentamiento minero)",
    "Terrenos de Drombb (campamento de prospectores)",
    "Geonosis (colmena Gogum)",
    "Cantina Roche J9 (colmena Gogum)",
    "Geonosis (fiesta de Piddock)",
    "Geonosis (colmena Trellik, muelle AA7)",
    "Mos Shuuta",
    "Palacio de Teemo (perímetro)",
    "Palacio de Teemo (interior)",
]

SCENES_LONG_ARM = [
    "Acto I: Problemas a bordo del Colmillo de Krayt",
    "Acto I: Intercepción violenta (Thwheek en el espacio)",
    "Acto I: Llegada a Nabat y piso franco de Nyn",
    "Acto I: Emboscada en la guarida del lylek (en ruta a Nueva Meen)",
    "Acto I: Nueva Meen (tensión social y petición de ayuda)",
    "Acto I: Alteración del orden público (tractor oruga de Drombb)",
    "Acto I: Asalto al campamento de Drombb",
    "Acto I: Regreso a Nabat (Thwheek acecha) y reunión con Ota",
    "Acto II: Ota presenta la recompensa y el plan Geonosis",
    "Acto II: Cantina Roche J9 (contactos y etiqueta geonosiana)",
    "Acto II: Fiesta privada del duque Piddock",
    "Acto II: Muelle AA7 (colmena Trellik)",
    "Acto III: Infiltración en el palacio de Teemo",
    "Acto III: Taller de droides B1",
    "Acto III: Celdas de gladiadores",
    "Acto III: Confrontación final con Teemo",
]

OBJECTIVES = [
    "Conseguir la información sin escalar a masacre",
    "Escapar con la carga intacta antes de que cierren la ruta",
    "Capturar vivo al objetivo para negociar",
    "Aguantar X asaltos hasta que llegue extracción",
    "Desactivar la alarma/compuerta mientras el resto cubre",
    "Rescatar a un rehén y salir sin llamar a un ejército",
]

PRESSURES = [
    "A los 3 beats sube el nivel de alerta y llega un refuerzo con ventaja posicional.",
    "Cada asalto que pasa empeora la situación: más ruido, menos salidas, más civiles en peligro.",
    "Cuando alguien cae Incapacitado, una tercera parte interviene y cambia el objetivo.",
    "Si se usan armas pesadas, el entorno se vuelve hostil (humo, fuego, sellos de seguridad).",
    "El objetivo se mueve: si no lo frenan en X, la escena termina en persecución o puerta cerrada.",
]

TWISTS = [
    "Un tercero irrumpe reclamando la presa: no atacan a todos, atacan al que les interesa.",
    "El enemigo ofrece trato en mitad del fuego, pero exige algo inmediato.",
    "El terreno cambia: se apaga la luz, se cierra una compuerta o se rompe una pasarela.",
    "Aparece un inocente/aliado en la línea de tiro y obliga a decidir prioridades.",
    "El líder enemigo intenta huir con una pieza clave, forzando cambio de objetivo.",
]

OPPOSITION = [
    "Un rival con nombre y un grupo de esbirros bien coordinados",
    "Seguridad local (esbirros) con un supervisor (rival) que quiere arresto limpio",
    "Banda de swoops (esbirros) liderada por un piloto agresivo (rival)",
    "Un cazarrecompensas (rival) que interrumpe para cobrar su contrato",
    "Droides de seguridad lentos pero duros con apoyo de operadores humanos",
]

TERRAIN_BITS = [
    "Cobertura dura: contenedores apilados o maquinaria",
    "Cobertura móvil: droides de carga / mesas volcadas / carros",
    "Altura: pasarela, balcón o repisa con línea de visión",
    "Riesgo: combustible, chispas, humo o suelo inestable",
    "Botón interactivo: consola (luces/puertas/alarma) o torno/montacargas",
    "Ruta secundaria: puerta trasera, atajo estrecho o escalera de servicio",
    "Elemento social: público, clientes o trabajadores que pueden estorbar/ayudar",
]

EMPHASIS_TAGS = {
    "setpieces": ["setpiece", "terreno-interactivo"],
    "tensión": ["timer", "presión"],
    "social+fuego": ["social", "negociación", "amenaza"],
    "variedad": ["variedad"],
}


def _rng(seed: str | None) -> random.Random:
    if seed is None or str(seed).strip() == "":
        return random.Random()
    return random.Random(str(seed))


def _pick(r: random.Random, items: list[str]) -> str:
    return r.choice(items)


def _split_lines(text: str) -> list[str]:
    raw = [l.strip() for l in (text or "").splitlines()]
    return [l for l in raw if l]


def _terrain_from_input(r: random.Random, terrain: str) -> list[str]:
    provided = _split_lines(terrain)
    if len(provided) >= 5:
        return provided[:5]
    chosen: list[str] = []
    pool = TERRAIN_BITS[:]
    r.shuffle(pool)
    for t in pool:
        if len(chosen) >= 5:
            break
        if t not in chosen:
            chosen.append(t)
    merged = provided + [t for t in chosen if t not in provided]
    return merged[:5]


def _scene_defaults(scene: str | None) -> dict[str, str]:
    if not scene:
        return {}
    if scene == SCENES_LONG_ARM[0]:
        return {
            "location": "Colmillo de Krayt (a bordo)",
            "title": "Control total del Colmillo de Krayt",
            "hook": "La nave huele a problemas: alarmas, rastreo, un prisionero y un cargamento comprometedor.",
            "objective": "Asegurar la nave (rastro, prisionero, fallos) y fijar un rumbo viable sin atraer persecución.",
            "opposition": "Amenazas no humanas: tiempo, mala información, tensiones internas y un rastro que delata su posición.",
            "pressure": "Cada decisión que ignore el rastreo o el estado de la nave aumenta la probabilidad de una intercepción hostil al llegar.",
            "twist": "Una pista inesperada conecta a Teemo con Geonosis y con un intermediario desaparecido.",
            "terrain": "Interfaz de navegación y alarmas (botón)\nCompartimentos ocultos (botín/peligro)\nBodega 3 con celda de contención (objetivo)\nBodega principal con hedor persistente (penalizaciones)\nPasillos estrechos: moverse con prisas cuesta",
            "rewards": "Ventaja táctica: reducir/evitar persecución, información clave y acceso a recursos escondidos a bordo.",
        }
    if scene == SCENES_LONG_ARM[1]:
        return {
            "location": "Órbita de Ryloth",
            "title": "Intercepción violenta",
            "hook": "Una nave rápida aparece en vector de ataque. No quieren hablar: quieren abatirles o forzar un aterrizaje.",
            "objective": "Llegar a Nabat con la nave operativa (o al menos con un aterrizaje controlado).",
            "opposition": "Un caza estelar pilotado por un agente de Teemo que intenta mantener ventaja posicional.",
            "pressure": "Si el casco aguanta poco o el piloto pierde el control, el combate desemboca en aterrizaje de emergencia con daño y heridas.",
            "twist": "El atacante rompe contacto si su nave queda dañada: pueden perseguirlo o priorizar la llegada.",
            "terrain": "Corto alcance inicial\nNubes/atmósfera de Ryloth como cobertura\nBotón: maniobras evasivas / seguir al objetivo\nRiesgo: daño al casco y tensión de sistemas\nElección: perseguir o aterrizar",
            "rewards": "Si lo superan, el perseguidor queda fuera de juego a corto plazo y llegan con iniciativa narrativa.",
        }
    if scene == SCENES_LONG_ARM[2]:
        return {
            "location": "Nabat (piso franco de Nyn)",
            "title": "Bajo la ciudad de Nabat",
            "hook": "Un contacto militante ofrece refugio, curas y una petición: ayudar a una comunidad minera presionada.",
            "objective": "Cerrar trato, aprovisionarse y salir con un plan claro hacia Nueva Meen sin levantar sospechas.",
            "opposition": "Presión social: recursos limitados, confianza frágil y la sombra de perseguidores que ya han llegado al puerto.",
            "pressure": "Si se demoran o hacen mucho ruido, la vigilancia enemiga escala y el viaje se complica.",
            "twist": "Llega aviso de visitantes recientes procedentes de Tatooine: alguien les está siguiendo.",
            "terrain": "Piso franco con salidas controladas\nMercado subterráneo (compras rápidas)\nBotón: favores de Nyn (equipo/curas)\nRiesgo: revelar demasiado sobre Teemo\nRuta: túnel de servicio hacia el exterior",
            "rewards": "Recuperación total, un recurso extra, y acceso a un deslizador para la ruta.",
        }
    if scene == SCENES_LONG_ARM[3]:
        return {
            "location": "Guarida del lylek",
            "title": "Emboscada en la guarida del lylek",
            "hook": "En plena ruta, una emboscada bien preparada intenta volcar el deslizador y forzar rendición.",
            "objective": "Romper la emboscada, evitar captura y conservar movilidad para llegar a Nueva Meen.",
            "opposition": "Cazarrecompensas con buena cobertura y un plan de retirada por túneles.",
            "pressure": "La movilidad se degrada: el deslizador puede quedar dañado; el combate atrae al depredador local si se alarga.",
            "twist": "Los enemigos se hacen pasar por 'autoridad' para provocar dudas; el depredador no distingue bandos.",
            "terrain": "Deslizador volcado como cobertura\nEntrada de caverna (choke)\nTúneles laterales para flanqueo\nMontones de roca / escombros (cobertura)\nRiesgo: el lylek entra si hay carne fresca y ruido",
            "rewards": "Botín de emergencia y, si se gestiona bien, un aliado narrativo que empuja a seguir adelante.",
        }
    if scene == SCENES_LONG_ARM[4]:
        return {
            "location": "Nueva Meen (asentamiento minero)",
            "title": "Nueva Meen pide ayuda",
            "hook": "Una comunidad minera resiste extorsión y sabotajes. Quieren que hagáis de palanca para cambiar el equilibrio.",
            "objective": "Ganar información, escoger enfoque (diplomacia, sabotaje, asalto) y asegurar apoyo local.",
            "opposition": "Un capataz con fachada 'legal' y matones que buscan intimidar, no negociar.",
            "pressure": "Si la tensión sube, la violencia se vuelve inevitable y los civiles quedan en medio.",
            "twist": "La recompensa por los PJ empieza a circular: enemigos oportunistas cambian de objetivo hacia ellos.",
            "terrain": "Calles de tierra con chatarra\nCondensadores de vapor dañados (riesgo)\nChabolas y tiendas (cobertura blanda)\nMontón de tierra/rocas al sur (altura/obstáculo)\nBotón: apoyo de mineros si se ganan su confianza",
            "rewards": "Apoyo twi'lek, logística local y una vía clara para atacar el problema en su origen.",
        }
    if scene == SCENES_LONG_ARM[5]:
        return {
            "location": "Nueva Meen (asentamiento minero)",
            "title": "Alteración del orden público",
            "hook": "De noche, unos matones borrachos convierten un conflicto latente en crisis visible.",
            "objective": "Proteger a la comunidad, evitar daños mayores y decidir si escalan el conflicto hacia el campamento enemigo.",
            "opposition": "Un grupo pequeño de matones armados y muy agresivos, con ventaja por oscuridad y caos.",
            "pressure": "El condensador de vapor dañado y la casa a punto de caer vuelven la escena un cronómetro.",
            "twist": "Intentan requisar el deslizador: si lo pierden, pierden control del ritmo y del viaje.",
            "terrain": "Oscuridad (setbacks)\nTractor oruga como cobertura móvil\nVapor/agua a presión (riesgo)\nChabolas frágiles (consecuencias)\nBotón: civiles pueden intervenir si se les arma o inspira",
            "rewards": "Moral y apoyo; además, justificación perfecta para ir a por el cabecilla.",
        }
    if scene == SCENES_LONG_ARM[6]:
        return {
            "location": "Terrenos de Drombb (campamento de prospectores)",
            "title": "Asalto al campamento de Drombb",
            "hook": "La fuente del acoso está a pocos kilómetros: vehículos industriales, un edificio prefabricado y una cantina fachada.",
            "objective": "Romper la cadena de mando, destruir capacidad operativa o forzar retirada sin masacrar a todo el mundo.",
            "opposition": "Un líder fanfarrón y varios grupos de matones con acceso a vehículos y mejores posiciones.",
            "pressure": "Si la alarma salta, se reagrupan y se vuelven más peligrosos; si el combate se alarga, llegan refuerzos internos.",
            "twist": "Hay evidencia que apunta a un intermediario clave de Teemo y a su red de contactos.",
            "terrain": "Tractores oruga (cobertura y peligro)\nEdificio prefabricado (objetivo)\nCantina (social + combate)\nBotón: cortar energía/vehículos\nRuta: huida hacia Nueva Meen o al yermo",
            "rewards": "Liberan la comunidad, obtienen pruebas útiles y ganan aliados para el acto III.",
        }
    if scene == SCENES_LONG_ARM[7]:
        return {
            "location": "Nabat (piso franco de Nyn)",
            "title": "Regreso a Nabat",
            "hook": "De vuelta al puerto, una sombra observa desde los túneles: alguien toma nota de todo.",
            "objective": "Cerrar filas con los aliados, detectar vigilancia y decidir el siguiente paso sin que el enemigo controle el tempo.",
            "opposition": "Un observador escurridizo y la presión de una recompensa creciente.",
            "pressure": "Si lo persiguen sin plan, se convierten en presa; si lo ignoran, les sigue hasta el siguiente acto.",
            "twist": "Un nuevo contacto propone una jugada contra los acuerdos de Teemo fuera de Ryloth.",
            "terrain": "Túneles subterráneos (persecución)\nMultitud del puerto (ocultación)\nBotón: refugio seguro\nRiesgo: perder al objetivo\nRuta: salto a Geonosis",
            "rewards": "Acceso al acto II con iniciativa: información, plan y ventana de acción.",
        }
    if scene == SCENES_LONG_ARM[8]:
        return {
            "location": "Nabat (piso franco de Nyn)",
            "title": "Ota pone el tablero",
            "hook": "Un espía bothan trae pruebas: hay recompensa por sus cabezas y una vía para golpear a Teemo donde le duele.",
            "objective": "Negociar con Ota: qué quiere, qué ofrece y cómo entran en Geonosis sin parecer amateurs.",
            "opposition": "Burocracia criminal, credibilidad y una negociación en la que cualquier paso en falso cuesta.",
            "pressure": "Cada día que pasa, más cazarrecompensas se interesan por los 50.000; la ventana se cierra.",
            "twist": "Ota no lo sabe todo: parte de su info es útil, parte es cebo.",
            "terrain": "Sala privada\nBotón: comunicador/credenciales\nRiesgo: acordar algo que no pueden cumplir\nRuta: salida a hipersalto",
            "rewards": "Ganchos claros y objetivos concretos para el acto II.",
        }
    if scene == SCENES_LONG_ARM[9]:
        return {
            "location": "Cantina Roche J9 (colmena Gogum)",
            "title": "Roche J9",
            "hook": "Una cantina geonosiana pensada para 'extranjeros' es la antesala de la política insectoide.",
            "objective": "Entrar, leer el ambiente, conseguir presentaciones y evitar ofender a la casta equivocada.",
            "opposition": "Etiqueta, malentendidos culturales y guardias atentos.",
            "pressure": "Si llaman demasiado la atención, los escoltan fuera o les ponen una marca social difícil de borrar.",
            "twist": "Un invitado ofrece acceso… a cambio de algo incómodo.",
            "terrain": "Barra atendida por obreros\nReservados\nBotón: credenciales/presentación\nRiesgo: meterse en la colmena equivocada\nRuta: invitación a fiesta",
            "rewards": "Acceso social a PNJ clave y al evento que concentra la información.",
        }
    if scene == SCENES_LONG_ARM[10]:
        return {
            "location": "Geonosis (fiesta de Piddock)",
            "title": "Fiesta privada",
            "hook": "Una fiesta de alto riesgo: criminales delegados, nobles insectoides y secretos cruzados.",
            "objective": "Extraer información y sembrar dudas contra Teemo sin provocar un tiroteo en una colmena hostil.",
            "opposition": "Vigilancia, egos, duques rivales y un equilibrio social frágil.",
            "pressure": "Tres beats: llegada, brindis/negocio, cierre. Cada beat reduce margen para improvisar.",
            "twist": "Alguien intenta usar a los PJ como chivo expiatorio o como cortina de humo.",
            "terrain": "Salón ceremonial\nReservados\nPasarelas\nBotón: audiencia / entrega de pruebas\nRuta: pista hacia muelle AA7",
            "rewards": "Información accionable para el acto III y/o acceso a un carguero clave.",
        }
    if scene == SCENES_LONG_ARM[11]:
        return {
            "location": "Geonosis (colmena Trellik, muelle AA7)",
            "title": "Muelle AA7",
            "hook": "Un muelle vigilado: el carguero que necesitan está cerca, pero la patrulla está lista.",
            "objective": "Entrar, tomar el carguero o la carga, y salir sin desencadenar una respuesta masiva.",
            "opposition": "Soldados geonosianos en patrulla y mecanismos de seguridad.",
            "pressure": "Si hay disparos, llegan refuerzos y la ventana de escape se cierra.",
            "twist": "Los guardias huyen si la cosa se tuerce, pero vuelven con más; la clave es el ritmo.",
            "terrain": "Pasarela elevada\nCajas/carga como cobertura\nBotón: control del muelle\nRiesgo: refuerzos\nRuta: salida a hipersalto",
            "rewards": "Acceso sigiloso al acto III: un vector de entrada al palacio de Teemo.",
        }
    if scene == SCENES_LONG_ARM[12]:
        return {
            "location": "Palacio de Teemo (perímetro)",
            "title": "Entrada indirecta",
            "hook": "Asaltar el palacio es suicida. La clave es entrar cuando el palacio te recibe sin darse cuenta.",
            "objective": "Colarse, desactivar defensas puntuales y llegar a una posición desde la que dictar el final.",
            "opposition": "Guardias, protocolos y un palacio diseñado para humillar intrusos.",
            "pressure": "Cada alarma cerrada abre otra: cuanto más ruido, más se sellan rutas y se reorganizan.",
            "twist": "Un aliado inesperado dentro del palacio necesita algo para ayudar.",
            "terrain": "Muelles/carga\nPasillos de servicio\nBotón: consola de seguridad\nRiesgo: ser aislados\nRuta: talleres y celdas",
            "rewards": "Acceso al clímax en sus términos.",
        }
    if scene == SCENES_LONG_ARM[13]:
        return {
            "location": "Palacio de Teemo (interior)",
            "title": "Taller de droides",
            "hook": "El corazón tecnológico del plan: piezas, droides almacenados y alguien que no debería estar aquí.",
            "objective": "Sabotear, robar o reprogramar para quitarle recursos a Teemo.",
            "opposition": "Guardias y sistemas; el ruido atrae más problemas que el combate en sí.",
            "pressure": "Si tardan, se cierran salidas y llegan refuerzos.",
            "twist": "Un droide o prisionero ofrece una ruta alternativa con un precio.",
            "terrain": "Mesas de trabajo (cobertura)\nCajas de droides B1 (peligro)\nBotón: cortar energía\nRiesgo: explosión/alarma\nRuta: comunicaciones",
            "rewards": "Reducen la capacidad militar de Teemo y ganan leverage.",
        }
    if scene == SCENES_LONG_ARM[14]:
        return {
            "location": "Palacio de Teemo (interior)",
            "title": "Celdas de gladiadores",
            "hook": "El palacio guarda 'activos' vivos: rehenes, gladiadores y resentimientos listos para explotar.",
            "objective": "Liberar aliados potenciales y evitar que la fuga se convierta en matanza caótica.",
            "opposition": "Guardias y disciplina: liberar es fácil, controlar consecuencias no.",
            "pressure": "Si el palacio entra en lockdown, las celdas se convierten en trampa.",
            "twist": "Entre los prisioneros hay alguien con una razón para no confiar en los PJ.",
            "terrain": "Pasillos estrechos\nRejas/compuertas (botón)\nRiesgo: alarma\nRuta: atajo al interior",
            "rewards": "Refuerzos aliados o distracción decisiva para el final.",
        }
    if scene == SCENES_LONG_ARM[15]:
        return {
            "location": "Palacio de Teemo (interior)",
            "title": "Final con Teemo",
            "hook": "La última escena no es un duelo: es una ejecución pública o un trato imposible, según cómo lleguen.",
            "objective": "Cerrar el arco: matar, humillar, forzar exilio, o atar a Teemo con su propia red.",
            "opposition": "Teemo y su aparato: guardias, trampas y control del entorno.",
            "pressure": "Cada beat, Teemo usa el palacio como arma: puertas, trampas, rehenes y refuerzos.",
            "twist": "Plan B: alguien traiciona o se abre una vía de escape que cambia el objetivo.",
            "terrain": "Trono elevado\nPasarelas laterales\nBotón: comunicaciones/puertas\nRiesgo: rehenes\nRuta: huida final",
            "rewards": "Cierre de campaña: reputación, aliados y nuevas complicaciones.",
        }
    return {}


INTERLUDES = [
    {
        "from": "Nabat (piso franco de Nyn)",
        "to": "Tierras baldías de Ryloth (en deslizador)",
        "title": "Salida por el túnel de servicio",
        "hook": "Salir de Nabat sin levantar sospechas requiere elegir ruta, hora y señuelo.",
        "objective": "Ganar distancia sin que nadie pueda seguirles hasta Nueva Meen.",
        "opposition": "Vigilancia oportunista y controles improvisados.",
        "pressure": "Si fallan, empiezan el siguiente combate con desventaja (posiciones malas o menos recursos).",
        "twist": "Un trabajador del puerto les reconoce y quiere un favor ahora.",
        "terrain": "Túnel estrecho\nPunto de control improvisado\nBotón: soborno/engaño\nRiesgo: persecución\nRuta: yermo abierto",
        "rewards": "Empiezan la ruta con iniciativa y sin 'calor' extra.",
    },
    {
        "from": "Nueva Meen (asentamiento minero)",
        "to": "Terrenos de Drombb (campamento de prospectores)",
        "title": "Entre el pueblo y el campamento",
        "hook": "El camino es corto, pero el enemigo domina el ritmo con vehículos y exploradores.",
        "objective": "Reconocer, tender trampa o infiltrar antes de la acción principal.",
        "opposition": "Exploradores y patrullas ligeras.",
        "pressure": "Si se detecta, el campamento se atrinchera y el asalto se endurece.",
        "twist": "Un minero radical intenta ir por su cuenta y puede fastidiar el sigilo.",
        "terrain": "Terreno abierto\nMontículos y rocas\nBotón: apagón/sabotaje\nRiesgo: ser vistos\nRuta: vuelta rápida",
        "rewards": "Ventaja posicional o una vía de entrada segura.",
    },
    {
        "from": "Geonosis (fiesta de Piddock)",
        "to": "Geonosis (colmena Trellik, muelle AA7)",
        "title": "Colas largas y miradas largas",
        "hook": "Salir de una fiesta geonosiana con información no garantiza salir sin ser seguido.",
        "objective": "Detectar cola, romperla y llegar a AA7 sin que el muelle esté preparado.",
        "opposition": "Agentes atentos y guardias que preguntan demasiado.",
        "pressure": "Si llegan tarde, la patrulla de AA7 duplica efectivos.",
        "twist": "Un contacto de la fiesta aparece y pide cerrar un trato ya.",
        "terrain": "Pasarelas\nMultitud\nBotón: perderse en la colmena\nRiesgo: ser marcado\nRuta: transporte interno",
        "rewards": "Entrada limpia al muelle.",
    },
]


def _interlude_defaults(from_location: str, to_location: str) -> dict[str, str]:
    for it in INTERLUDES:
        if it["from"] == from_location and it["to"] == to_location:
            d = dict(it)
            if not d.get("location"):
                d["location"] = f"{from_location} → {to_location}".strip(" →")
            return d
    return {
        "location": f"{from_location} → {to_location}".strip(" →"),
        "title": "Transición peligrosa",
        "hook": "La distancia entre escenas es donde la campaña te cobra intereses.",
        "objective": "Llegar al siguiente punto con recursos y control del ritmo.",
        "opposition": "Patrullas, fauna o curiosos armados que huelen oportunidad.",
        "pressure": "Cada beat añade una complicación que reduce opciones en la siguiente escena.",
        "twist": "Una elección moral corta aparece en el peor momento.",
        "terrain": "Ruta principal\nAtajo\nCobertura improvisada\nBotón: soborno/engaño\nRiesgo: alarma o persecución",
        "rewards": "Si lo resuelven bien, entran en la siguiente escena con ventaja.",
    }


def generate_encounter(inp: EncounterInput) -> Encounter:
    r = _rng(inp.seed)
    kind = (inp.kind or "escena").strip().lower()
    if kind == "interludio":
        defaults = _interlude_defaults((inp.from_location or "").strip(), (inp.to_location or "").strip())
    else:
        defaults = _scene_defaults(inp.scene)

    title = (inp.title or "").strip() or defaults.get("title") or _pick(r, ["Control de daños", "Fuego cruzado", "Negocio sucio", "Puerta sellada"])
    hook = (inp.hook or "").strip() or defaults.get("hook") or "Algo se tuerce y obliga a decidir rápido bajo presión."

    objective = (inp.objective or "").strip() or defaults.get("objective") or _pick(r, OBJECTIVES)
    objectives = [objective]

    opposition = (inp.opposition or "").strip() or defaults.get("opposition") or _pick(r, OPPOSITION)
    opposition_list = _split_lines(opposition) or [opposition]

    pressure = (inp.pressure or "").strip() or defaults.get("pressure") or _pick(r, PRESSURES)
    twist = (inp.twist or "").strip() or defaults.get("twist") or _pick(r, TWISTS)

    terrain_text = (inp.terrain or "").strip() or str(defaults.get("terrain") or "").strip()
    terrain_list = _terrain_from_input(r, terrain_text)

    rewards = (inp.rewards or "").strip() or defaults.get("rewards") or "Recompensa útil inmediata y una consecuencia clara si fallan."

    if inp.party.lower().startswith("3") or inp.party.lower().startswith("peque"):
        scaling_easier = "Reduce un grupo de esbirros o dales mala cobertura; ofrece una salida clara."
        scaling_harder = "Añade un rival extra o adelanta el refuerzo un beat."
    else:
        scaling_easier = "Reduce un grupo de esbirros o retrasa el refuerzo un beat; aumenta la cobertura favorable."
        scaling_harder = "Añade un refuerzo ligero o un 'hazard' extra del entorno; cierra una ruta secundaria."

    if kind == "interludio":
        beats = [
            "Inicio: aviso temprano; se intuye la complicación.",
            "Medio: la complicación golpea; decidir rápido o perder el ritmo.",
            "Final: salida limpia o salida con coste; engancha con la siguiente escena.",
        ]
    else:
        beats = [
            "Inicio: presentación del objetivo y primera complicación visible.",
            "Medio: la presión sube y el terreno cambia o aparece una decisión moral.",
            "Final: escape/captura/negociación; consecuencias inmediatas en escena.",
        ]

    tags: list[str] = []
    emphasis_key = inp.emphasis.strip().lower()
    tags.extend(EMPHASIS_TAGS.get(emphasis_key, []))
    tags.append(kind)
    if inp.scene:
        tags.append("largo-brazo-del-hutt")
    if inp.keywords.strip():
        tags.extend([k.strip() for k in inp.keywords.split(",") if k.strip()])

    source_parts = []
    if inp.module:
        source_parts.append(inp.module)
    if kind == "interludio":
        if inp.from_location or inp.to_location:
            source_parts.append(f"{(inp.from_location or '').strip()} → {(inp.to_location or '').strip()}".strip(" →"))
    elif inp.scene:
        source_parts.append(inp.scene)
    source = " · ".join([p for p in source_parts if p]) if source_parts else "Generado"

    location = (inp.location or "").strip() or str(defaults.get("location") or "").strip()

    return Encounter(
        system=inp.system,
        source=source,
        title=title,
        hook=hook,
        objectives=objectives,
        opposition=opposition_list,
        terrain=terrain_list,
        pressure=pressure,
        twist=twist,
        scaling_easier=scaling_easier,
        scaling_harder=scaling_harder,
        rewards=rewards,
        beats=beats,
        tags=tags,
        kind=kind,
        location=location,
    )
