# AI Research Agents - Multi-Agent System

Un sistema de inteligencia artificial multi-agente que simula 3 AIs trabajando coordinadamente para investigar temas relacionados a la inteligencia artificial en el ámbito académico. El sistema expone sus resultados a través de un servidor MCP (Model Context Protocol) usando FastMCP.

## 🤖 Agentes

El sistema cuenta con tres agentes especializados que trabajan en secuencia:

### 1. **Researcher Agent (Investigador)**
- **Rol**: Especialista en investigación académica de IA
- **Función**: Busca y recopila información sobre temas de IA
- **Salida**: Hallazgos de investigación con resúmenes, puntos clave y fuentes académicas

### 2. **Curator Agent (Curador)**
- **Rol**: Curador de contenido de investigación
- **Función**: Organiza, filtra y evalúa la calidad de los hallazgos
- **Salida**: Contenido curado con categorización, puntuación de calidad y recomendaciones

### 3. **Editor Agent (Editor)**
- **Rol**: Tomador de decisiones editoriales
- **Función**: Aprueba o rechaza contenido para publicación
- **Salida**: Decisión editorial con razonamiento y sugerencias de mejora

## 🏗️ Arquitectura

```
ResearchTopic → Researcher → ResearchFinding
                                ↓
                            Curator → CuratedContent
                                ↓
                            Editor → EditorialDecision
                                ↓
                            ResearchReport (Approved/Rejected)
```

## 🚀 Instalación

### Requisitos
- Python 3.10 o superior
- pip

### Pasos de instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/facundodortuy/genai-code-by-agent-example.git
cd genai-code-by-agent-example
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. (Opcional) Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

## 📖 Uso

### Demo Script

Ejecuta el script de demostración para ver el sistema en acción:

```bash
python demo.py
```

Este script:
- Investiga 4 temas de IA diferentes
- Muestra el proceso de cada agente
- Presenta estadísticas y resultados aprobados/rechazados

### Servidor MCP (FastMCP)

Inicia el servidor MCP para exponer las herramientas y recursos:

```bash
python -m src.server
```

El servidor proporciona:

#### **Tools (Herramientas)**
- `research_topic(topic, keywords)` - Investiga un tema específico
- `research_multiple_topics(topics)` - Investiga múltiples temas
- `get_research_statistics()` - Obtiene estadísticas generales
- `get_approved_research()` - Lista investigaciones aprobadas
- `get_rejected_research()` - Lista investigaciones rechazadas

#### **Resources (Recursos)**
- `research://reports` - Todos los reportes de investigación
- `research://approved` - Solo reportes aprobados

#### **Prompts**
- `research_prompt(topic)` - Genera prompt para investigar un tema
- `batch_research_prompt(topics)` - Genera prompt para múltiples temas

### Uso Programático

```python
import asyncio
import uuid
from src.models import ResearchTopic
from src.orchestrator import ResearchOrchestrator

async def main():
    # Inicializar orchestrator
    orchestrator = ResearchOrchestrator(approval_threshold=0.7)
    
    # Crear un tema de investigación
    topic = ResearchTopic(
        id=str(uuid.uuid4()),
        topic="Machine Learning in Healthcare",
        keywords=["deep learning", "medical imaging"]
    )
    
    # Ejecutar investigación
    report = await orchestrator.research_topic(topic)
    
    # Acceder a resultados
    print(f"Status: {report.final_status}")
    print(f"Quality: {report.curated.quality_score}")
    print(f"Decision: {report.decision.decision}")

asyncio.run(main())
```

## 📊 Estructura del Proyecto

```
.
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py          # Clase base para agentes
│   │   ├── researcher.py    # Agente investigador
│   │   ├── curator.py       # Agente curador
│   │   └── editor.py        # Agente editor
│   ├── models.py            # Modelos de datos Pydantic
│   ├── orchestrator.py      # Coordinador de agentes
│   └── server.py            # Servidor FastMCP
├── tests/                   # Tests unitarios
├── demo.py                  # Script de demostración
├── requirements.txt         # Dependencias Python
├── pyproject.toml          # Configuración del proyecto
└── README.md               # Esta documentación
```

## 🔧 Configuración

El sistema puede configurarse a través de variables de entorno (.env):

```bash
# Modelos de IA (opcional - usa datos mock por defecto)
RESEARCHER_MODEL=gpt-4
CURATOR_MODEL=gpt-4
EDITOR_MODEL=gpt-4

# Configuración de investigación
MAX_RESEARCH_TOPICS=5
RESEARCH_DEPTH=moderate
```

## 🧪 Testing

Ejecutar tests unitarios:

```bash
pytest tests/
```

## 🎯 Características

- ✅ **Sistema Multi-Agente**: Tres agentes especializados trabajando coordinadamente
- ✅ **Investigación Académica**: Enfoque en temas de IA en contextos académicos
- ✅ **Workflow Completo**: Investigación → Curación → Decisión Editorial
- ✅ **Servidor MCP**: Exposición de herramientas y recursos via FastMCP
- ✅ **Datos Realistas**: Simulación con datos académicos contextuales
- ✅ **Métricas y Estadísticas**: Seguimiento de calidad y aprobación
- ✅ **Categorización Automática**: Organización por áreas de IA
- ✅ **Decisiones Razonadas**: Explicaciones claras de aprobaciones/rechazos

## 📝 Ejemplo de Salida

```
==================================================================================
Starting research workflow for: Natural Language Processing for Academic Research
==================================================================================

[Researcher] Starting research on topic: Natural Language Processing for Academic Research
[Researcher] Completed research: Natural Language Processing Breakthroughs: Natural Language Processing for Academic Research
[Curator] Curating research finding: Natural Language Processing Breakthroughs: Natural Language Processing for Academic Research
[Curator] Curation complete. Quality score: 0.87
[Editor] Reviewing curated content (ID: a1b2c3d4...)
[Editor] Decision: APPROVED (score: 0.89)

==================================================================================
Workflow complete: APPROVED
Final Score: 0.89
==================================================================================
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es un ejemplo educativo y está disponible para uso académico y de aprendizaje.

## 👥 Autores

- Sistema desarrollado como ejemplo de arquitectura multi-agente con FastMCP

## 🔗 Referencias

- [FastMCP](https://github.com/jlowin/fastmcp) - Framework para Model Context Protocol
- [Pydantic](https://docs.pydantic.dev/) - Validación de datos
- [Model Context Protocol](https://modelcontextprotocol.io/) - Protocolo MCP