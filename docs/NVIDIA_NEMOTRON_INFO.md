# NVIDIA-Nemotron-3-Super-120B-A12B

Información técnica y características del modelo usado como "cerebro" para el `AI_Agent_Basic`.

## Resumen del Modelo

| Característica | Detalle |
|---|---|
| **Tipo de Arquitectura** | LatentMoE - Mamba-2 + MoE + Attention hybrid con MTP (Multi-Token Prediction) |
| **Parámetros** | 120B en total (12B activos al mismo tiempo) |
| **Longitud de Contexto** | Hasta 1 Millón de tokens |
| **Requisito Mínimo GPU** | 8× H100-80GB (para uso local) |
| **Idiomas Soportados** | Inglés, Francés, Alemán, Italiano, Japonés, Español, Chino |
| **Mejor uso para** | Workflows para agentes (Agentic workflows), razonamiento de largo contexto, alta automatización, uso de herramientas (Tool Use), RAG |
| **Modo Razonamiento** | Configurable ON/OFF (usando `enable_thinking=True/False`) |
| **Licencia** | NVIDIA Nemotron Open Model License (Listo para uso comercial) |
| **Desarrollador** | NVIDIA Corporation |
| **Corte de Datos** | Febrero de 2026 (Post-training) / Junio de 2025 (Pre-training) |
| **Fecha de Lanzamiento** | 11 de Marzo de 2026 |

---

## ¿Qué es Nemotron?
NVIDIA Nemotron™ es una familia de modelos abiertos (pesos abiertos, datos de entrenamiento y recetas) que entrega eficiencia y precisión líderes para la construcción de agentes de IA especializados.

El modelo **Nemotron-3-Super-120B-A12B-BF16** es un LLM entrenado por NVIDIA diseñado para tener capacidades fuertes de agente, razonamiento y conversación (ideal para agentes colaborativos y alta carga de procesamiento como automatización de tickets IT). 

A diferencia de modelos clásicos, este responde a consultas **generando primero un hilo o trazo de razonamiento (pensamiento estructurado)** antes de dar su respuesta final.

---

## Patrones Óptimos de Configuración

Para obtener el mejor rendimiento del modelo (ya sea en chat general, agentes con herramientas o RAG), NVIDIA recomienda estrictamente estos parámetros de generación:

- **Temperature:** `1.0`
- **Top P:** `0.95`
- **Reasoning Mode:** Añadir en el payload de OpenAI: `extra_body={"chat_template_kwargs": {"enable_thinking": True}}`

---

## Arquitectura y Eficiencia 
El modelo usa una mezcla LatentMoE (Latent Mixture-of-Experts) intercalada con capas Mamba-2 y MTP (Multi-Token Prediction). Esta estructura MTP no solo permite una generación de texto más veloz, sino que usa cuantización `NVFP4`, haciéndolo inmensamente eficiente computacionalmente para su tamaño.

## Capacidades como Agente (Agentic Benchmarks)
Al ser diseñado para Agentic Workflows, puntúa extraordinariamente bien en pruebas como:
- **Terminal Bench Core 2.0:** 31.00
- **SWE-Bench (OpenHands):** 60.47
- **SWE-Bench (OpenCode):** 59.20
- **TauBench (Airline, Retail, Telecom):** Promedio de 61.15

## Citación Oficial
```bibtex
@misc{nvidia_nemotron_3_2025,
  title  = {NVIDIA Nemotron 3: Efficient and Open Intelligence},
  author = {{NVIDIA}},
  year   = {2025},
  url    = {https://arxiv.org/abs/2512.20856},
  note   = {White Paper}
}
```
