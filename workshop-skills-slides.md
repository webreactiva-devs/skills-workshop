---
marp: true
theme: default
paginate: true
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

:root {
  --color-background: #1f2937;
  --color-foreground: #f0f0f0;
  --color-heading: #FED757;
  --color-accent: #FED757;
  --color-secondary: #9678D3;
  --color-hr: #E56A54;
  --font-default: 'Space Grotesk', 'Noto Sans JP', sans-serif;
}

section {
  background-color: var(--color-background);
  color: var(--color-foreground);
  font-family: var(--font-default);
  font-weight: 400;
  box-sizing: border-box;
  border-bottom: 8px solid var(--color-hr);
  position: relative;
  line-height: 1.7;
  font-size: 28px;
  padding: 56px;
}

section:last-of-type {
  border-bottom: none;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
  color: var(--color-heading);
  margin: 0;
  padding: 0;
}

h1 {
  font-size: 56px;
  line-height: 1.4;
  text-align: left;
  text-shadow: 0 0 20px rgba(254, 215, 87, 0.3);
}

h2 {
  position: absolute;
  top: 40px;
  left: 56px;
  right: 56px;
  font-size: 40px;
  padding-top: 0;
  padding-bottom: 16px;
}

h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 8px;
  width: 60px;
  height: 2px;
  background-color: var(--color-accent);
  box-shadow: 0 0 10px rgba(254, 215, 87, 0.5);
}

h2 + * {
  margin-top: 112px;
}

h3 {
  color: var(--color-accent);
  font-size: 28px;
  margin-top: 32px;
  margin-bottom: 12px;
}

ul, ol {
  padding-left: 32px;
}

li {
  margin-bottom: 10px;
}

footer {
  font-size: 0;
  color: transparent;
  position: absolute;
  left: 56px;
  right: 56px;
  bottom: 40px;
  height: 8px;
  background: linear-gradient(90deg, #E56A54, #9678D3);
  box-shadow: 0 0 20px rgba(229, 106, 84, 0.3);
}

section.lead {
  border-bottom: 8px solid var(--color-hr);
}

section.lead footer {
  display: none;
}

section.lead h1 {
  margin-bottom: 24px;
}

section.lead p {
  font-size: 30px;
  color: var(--color-foreground);
}

code {
  background-color: #3d4451;
  color: #FED757;
  padding: 2px 8px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
}

section pre {
  background-color: #2d2d2d !important;
  border-radius: 12px !important;
  padding: 28px 32px !important;
  font-size: 21px !important;
  line-height: 1.7 !important;
  border: 1px solid #444 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}

section pre code {
  background-color: transparent !important;
  padding: 0 !important;
  font-size: 21px !important;
  color: #e0e0e0 !important;
  line-height: 1.7 !important;
}

section pre code span {
  font-size: 21px !important;
  color: #e0e0e0 !important;
}

section pre code .hljs-section,
section pre code .hljs-strong,
section pre code .hljs-emphasis,
section pre code .hljs-bullet,
section pre code .hljs-attr,
section pre code .hljs-attribute,
section pre code .hljs-symbol,
section pre code .hljs-link,
section pre code .hljs-addition,
section pre code .hljs-variable,
section pre code .hljs-template-variable {
  color: #61dafb !important;
}

section pre code .hljs-string,
section pre code .hljs-title,
section pre code .hljs-name,
section pre code .hljs-type {
  color: #98c379 !important;
}

section pre code .hljs-keyword,
section pre code .hljs-selector-tag,
section pre code .hljs-built_in {
  color: #c678dd !important;
}

section pre code .hljs-comment {
  color: #7f848e !important;
}

section pre code .hljs-number,
section pre code .hljs-literal {
  color: #d19a66 !important;
}

strong {
  color: var(--color-accent);
  font-weight: 700;
}

a {
  color: var(--color-foreground) !important;
  text-decoration: underline;
}

section blockquote {
  border-left: 4px solid var(--color-heading) !important;
  padding: 12px 24px !important;
  margin: 16px 0 !important;
  background-color: rgba(229, 106, 84, 0.1) !important;
}

section blockquote p {
  color: #f0f0f0 !important;
  font-size: 26px !important;
  opacity: 1 !important;
}

section table {
  width: 100% !important;
  border-collapse: separate !important;
  border-spacing: 0 !important;
  font-size: 24px !important;
  margin-top: 16px !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid #444 !important;
}

section table th {
  background-color: #2d2d2d !important;
  color: var(--color-accent) !important;
  padding: 16px 28px !important;
  text-align: left !important;
  font-weight: 700 !important;
  border-bottom: 2px solid var(--color-accent) !important;
  border-right: none !important;
}

section table td {
  padding: 14px 28px !important;
  border-bottom: 1px solid #333 !important;
  background-color: #1a1a1a !important;
  color: #e0e0e0 !important;
  border-right: none !important;
}

section table tr:last-child td {
  border-bottom: none !important;
}

section table tr:nth-child(even) td {
  background-color: #222 !important;
}

section.section-break {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-bottom: 8px solid var(--color-secondary);
}

section.section-break h2 {
  position: static;
  font-size: 44px;
  color: var(--color-secondary);
  text-shadow: 0 0 20px rgba(150, 120, 211, 0.3);
}

section.section-break h2::after {
  display: none;
}
</style>

![bg contain](assets/image.png)

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Skills: Multiplica tu productividad con la IA

## **Masterclass en Web Reactiva Premium**

---

# En dos semanas, ¡agentes!

---

## ¿Qué sabe hacer tu IA?

- ¿Sabe crear y editar un DOC?
- ¿Sabe cómo aplicar tus controles de seguridad?
- ¿Sabe cómo mejorar un diseño en base a tus gustos?

> Sabe, pero poco y con esfuerzo
> **Mala calidad de resultados / Alto consumo de tokens**

---

## ¿Qué es una Skill?

Una **skill** es un paquete de instrucciones —estructurado en una carpeta— que le enseña al agente de IA a manejar flujos de trabajo específicos de manera consistente

> Es la receta que evita que tengamos que explicarle nuestras preferencias y procesos en cada nueva conversación

---

## Agentes compatibles

**¡Más de 30!** — Claude Code, Github Copilot, Gemini CLI, Qwen Code, OpenCode, Codex...

![w:900px](assets/image%201.png)

---

<!-- _class: section-break -->

## Demo: Crear una skill desde cero

---

## Anatomía de una skill

![w:1000px](assets/image%202.png)

```
mi-skill/
├── SKILL.md          # Instrucciones (requerido)
├── scripts/          # Código ejecutable (opcional)
├── references/       # Documentación (opcional)
└── assets/           # Plantillas y recursos (opcional)
```

---

## La clave: `description`

El frontmatter es el **mecanismo de triggering**

```yaml
---
name: name-of-the-skill
description: "[Qué hace] + [Cuándo usarlo] + [Capacidades clave]"
---
```

> No basta con *"Skill para crear dashboards"*
> Sí: *"Usa esta skill cuando el usuario mencione dashboards, métricas, visualización de datos, incluso si no dice 'dashboard'"*

---


![bg contain](assets/image%203.png)

---

## Instalar skills

1. Descargando la skill a la carpeta de la skill
2. Usando [skills.sh](https://skills.sh) — la forma más sencilla

```bash
npx skills add https://github.com/anthropics/skills \
  --skill skill-creator
```

```bash
npx skills add https://github.com/delineas/astro-framework-agents \
  --skill astro-framework
```

```bash
npx skills -h
```

---

<!-- _class: section-break -->

## Demo: Crear una skill con skill-creator

---

## Workflows del cuerpo de una skill

**El problema dicta la estructura, no tu preferencia**

| Patrón | Cuándo | Ejemplo |
|--------|--------|---------|
| **Router+Workflow** | Pipeline con decisiones secuenciales | `docx` |
| **Task** | Operaciones independientes | `pdf` |
| **Reference** | Criterios y estándares | `xlsx` |
| **Capabilities** | Features interrelacionadas | Buenas prácticas para skills |
| **Decision tree** | If / else if / else | Git undo |

---

## Patrón 1 · Router + Workflow

Caso real: skill `docx` — [ver skill](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md)

```
Quick Reference (router)
├── ¿Leer?   → pandoc, raw XML
├── ¿Crear?  → docx-js (Setup → Validate → Styles → Tables)
└── ¿Editar? → Unpack XML → Edit → Pack
```

> Progressive Disclosure aplicado al workflow

---

## Patrón 2 · Task-Based

Caso real: skill `pdf` — [ver skill](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md)

```
Quick Start (5 líneas de código)
├── Merge PDFs          ← autocontenido
├── Split PDF           ← no necesitas leer Merge
├── Extract Tables      ← otra herramienta (pdfplumber)
├── OCR Scanned PDFs    ← otra herramienta (pytesseract)
├── Add Watermark
└── Password Protection
```

Cada tarea es **independiente** y **copiar-pegar**

---

## Patrón 3 · Reference

Caso real: skill `xlsx`

```
Requirements for Outputs (lo primero)
├── Color Coding: azul=inputs, negro=fórmulas
├── Number Formats: currency $#,##0 · percentages 0.0%
└── Formula Rules: assumptions en celdas separadas

❌ WRONG
sheet['B10'] = total

✅ CORRECT
sheet['B10'] = '=SUM(B2:B9)'
```


---

## Patrón 4 · Capabilities

Caso real: skill `skill-best-practices` — [ver skill](https://github.com/webreactiva-devs/skills-workshop/blob/main/skills/skill-best-practices/SKILL.md)

```
Skill Quality Checklist (hub central)
├── 1. Description         → references/descriptions.md
├── 2. No basic knowledge  → references/expert-knowledge.md
├── ...
├── 8. Executable examples ← inline
├── 9. Failure anticipation← inline
└── 10. Naming rules       ← inline
```

> No es lineal: puedes entrar por cualquier criterio

---

## Patrón 5 · Decision Trees [git-undo](https://github.com/webreactiva-devs/skills-workshop/blob/main/skills/git-undo/SKILL.md)

```
¿Los cambios están en staging (git add)?
  ├── NO → ¿Descartar TODO?
  │   ├── SÍ → git checkout -- . && git clean -fd
  │   └── NO → ¿Es archivo nuevo (untracked)?
  │       ├── SÍ → rm <archivo>
  │       └── NO → git checkout -- <archivo>
  └── SÍ → ¿Ya hiciste commit?
      ├── NO → ¿Solo sacar del staging o descartar del todo?
      │   ├── Solo sacar → git reset HEAD <archivo>
      │   └── Descartar → git reset HEAD <archivo> && git checkout -- <archivo>
      └── SÍ → ¿Ya hiciste push?
          ├── NO → git reset --soft HEAD~1
          └── SÍ → git revert HEAD
```

---

## Truco: Workflows con cuestionario

> En el cuerpo de la skill pídele a la IA que te pregunte por lo que deseas

```
- Pregunta al usuario cuáles son sus preferencias de color. El color por defecto es el rojo.
```


---

# Skills vs el ecosistema

---

![bg contain](assets/image%204.png)

---

## Skills vs MCP

- MCP es la cocina — Skill es la **receta**
- MCP gasta **más tokens**
- MCP son más complejos (servidor vs markdown)
- Skills **lanzan** MCP

---

## Skills vs Agents

- Agente es el cocinero — Skill es la **receta**
- El agente tiene su **propia ventana de contexto**
- El agente tiene una **tarea propia**
- El agente se comunica con **otros agentes**
- Skills **lanzan** Agents / Agents **leen** Skills

---

## Skills vs Commands

- Command es solo el salero — Skill es la **receta**
- Los comandos son **prompts reutilizables** (/escribir-commit)
- Los comandos **no tienen scripts**
- Skills son los **sustitutos** de Commands

---

# Más demos

---

## Crea skills desde fuentes de conocimiento

- Documentación oficial de frameworks
- Estándares de seguridad (PCI, OWASP)
- Base de código existente
- Contenido ajeno (ej: karpathy-skills)
- Conversaciones con un chat


---

<!-- _class: section-break -->

## Demo: Skill desde una base de conocimiento

---

<!-- _class: section-break -->

## Demo: Crear una skill desde un problema

---

## Skill Judge

Skill para **evaluar la calidad** de tu skill

- Corrección de patrones
- Puntuación multidimensional
- Sugerencias de mejora accionables

> Idea: Crea tu propia **Skill Doomsday**

---

## Skills recomendadas

- **find-skills** — Descubre skills disponibles
- **frontend-design** — Diseño de interfaces
- **requesting-code-review** — Revisión de código
- **test-driven-development** — TDD con IA
- **skill-creator** — Crea nuevas skills

---

<!-- _class: lead -->

# Fuentes y recursos

[Crea Skills productivas para agentes de IA](https://webreactiva.dev/crea-skills)
[Skills: The Open Agent Skills CLI (vercel-labs)](https://github.com/vercel-labs/skills#supported-agents)
[Agent Skills: guia completa para Claude Code, Codex, Cursor y OpenCode](https://www.webreactiva.com/blog/skills-programadores-agentes-ia)
[Buenas practicas para crear skills de agentes de IA](https://www.webreactiva.com/blog/buenas-practicas-skills)
[Mejores Agent Skills para revisar codigo y seguridad](https://www.webreactiva.com/blog/skills-revision-codigo)
[skills.sh — The Agent Skills Directory](https://skills.sh)
[Skill Creator (Anthropic)](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
[NotebookLM — Recomendaciones oficiales para crear Skills](https://notebooklm.google.com/notebook/fd6d9bf5-7fb3-4383-920f-95a9ac21a4ae)

---

<!-- _class: lead -->
<!-- _paginate: false -->

# ¡Gracias!

**Dani Primo de Web Reactiva Premium**
