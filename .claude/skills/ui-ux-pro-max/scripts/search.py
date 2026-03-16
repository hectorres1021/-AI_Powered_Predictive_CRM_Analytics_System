#!/usr/bin/env python3
"""
UI/UX Pro Max - Design System Generator
Generates design system guidelines, tokens, and code patterns based on natural language queries.
"""

import argparse
import sys
import textwrap
from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# Design System Knowledge Base
# ─────────────────────────────────────────────────────────────────────────────

DOMAIN_PROFILES = {
    "style": {
        "label": "Visual Style & Layout",
        "tags": ["clean", "professional", "minimal", "card", "sidebar", "dashboard", "admin", "enterprise"],
    },
    "typography": {
        "label": "Typography & Readability",
        "tags": ["font", "readable", "sans-serif", "heading", "body", "size", "weight", "line-height", "accessible"],
    },
    "chart": {
        "label": "Data Visualization & Charts",
        "tags": ["chart", "graph", "progress", "enrollment", "tracking", "metric", "kpi", "bar", "line", "pie"],
    },
    "color": {
        "label": "Color System",
        "tags": ["color", "palette", "primary", "accent", "neutral", "semantic", "dark", "light", "contrast"],
    },
    "component": {
        "label": "Component Patterns",
        "tags": ["button", "input", "form", "table", "modal", "card", "badge", "alert", "nav", "sidebar"],
    },
    "spacing": {
        "label": "Spacing & Grid",
        "tags": ["spacing", "grid", "layout", "margin", "padding", "gap", "responsive", "breakpoint"],
    },
}

STACK_TEMPLATES = {
    "react": {
        "label": "React (JSX + CSS Modules / Tailwind)",
        "imports": "import React from 'react';\nimport styles from './Component.module.css';",
        "component_pattern": """\
// ─── {component_name} ──────────────────────────────────
const {component_name} = ({{ children, variant = 'primary', ...props }}) => (
  <div className={{`{css_class} {css_class}--${{variant}}`}} {{...props}}>
    {{children}}
  </div>
);
export default {component_name};""",
        "tailwind_example": """\
// Tailwind utility example
<div className="flex items-center gap-4 p-6 rounded-2xl bg-white shadow-sm border border-neutral-100">
  <span className="text-sm font-medium text-neutral-700">Label</span>
</div>""",
    },
    "html-tailwind": {
        "label": "HTML + Tailwind CSS",
        "imports": '<link href="https://cdn.tailwindcss.com" rel="stylesheet">',
        "component_pattern": """\
<!-- {component_name} -->
<div class="flex items-center gap-4 p-6 rounded-2xl bg-white shadow-sm border border-neutral-100">
  <p class="text-sm font-medium text-neutral-700">{component_name}</p>
</div>""",
        "tailwind_example": """\
<!-- Responsive admin layout -->
<div class="min-h-screen bg-neutral-50">
  <aside class="fixed inset-y-0 w-64 bg-white border-r border-neutral-200">...</aside>
  <main class="ml-64 p-8">...</main>
</div>""",
    },
    "vue": {
        "label": "Vue 3 (Composition API + Tailwind)",
        "imports": "<script setup>\nimport { ref } from 'vue';\n</script>",
        "component_pattern": """\
<template>
  <div :class="['base-{css_class}', `base-{css_class}--${{variant}}`]">
    <slot />
  </div>
</template>
<script setup>
defineProps({{ variant: {{ type: String, default: 'primary' }} }});
</script>""",
        "tailwind_example": """\
<!-- Vue + Tailwind component -->
<template>
  <div class="flex items-center gap-4 p-6 rounded-2xl bg-white shadow-sm">
    <slot />
  </div>
</template>""",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Token Generators
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class DesignTokens:
    project: str
    query: str
    domain: Optional[str] = None

    # Derived tokens (populated in __post_init__)
    primary_hue: str = ""
    colors: dict = field(default_factory=dict)
    typography: dict = field(default_factory=dict)
    spacing: dict = field(default_factory=dict)
    border_radius: dict = field(default_factory=dict)
    shadows: dict = field(default_factory=dict)
    chart_palette: list = field(default_factory=list)

    def __post_init__(self):
        q = self.query.lower()

        # Determine palette based on query context
        if any(w in q for w in ["health", "medical", "care"]):
            self.primary_hue = "Teal/Green"
            self.colors = {
                "primary-50": "#f0fdf4", "primary-100": "#dcfce7",
                "primary-500": "#22c55e", "primary-600": "#16a34a",
                "primary-700": "#15803d", "primary-900": "#14532d",
                "accent-500": "#0ea5e9", "accent-600": "#0284c7",
                "warning-500": "#f59e0b", "error-500": "#ef4444",
                "success-500": "#22c55e", "neutral-50": "#f8fafc",
                "neutral-100": "#f1f5f9", "neutral-200": "#e2e8f0",
                "neutral-600": "#475569", "neutral-900": "#0f172a",
            }
        elif any(w in q for w in ["workforce", "education", "nonprofit", "apprenticeship", "lead"]):
            self.primary_hue = "Indigo/Blue"
            self.colors = {
                "primary-50": "#eef2ff", "primary-100": "#e0e7ff",
                "primary-500": "#6366f1", "primary-600": "#4f46e5",
                "primary-700": "#4338ca", "primary-900": "#312e81",
                "accent-500": "#06b6d4", "accent-600": "#0891b2",
                "warning-500": "#f59e0b", "error-500": "#ef4444",
                "success-500": "#10b981", "neutral-50": "#f9fafb",
                "neutral-100": "#f3f4f6", "neutral-200": "#e5e7eb",
                "neutral-600": "#4b5563", "neutral-900": "#111827",
            }
        elif any(w in q for w in ["finance", "bank", "crm", "sales", "revenue"]):
            self.primary_hue = "Blue/Navy"
            self.colors = {
                "primary-50": "#eff6ff", "primary-100": "#dbeafe",
                "primary-500": "#3b82f6", "primary-600": "#2563eb",
                "primary-700": "#1d4ed8", "primary-900": "#1e3a8a",
                "accent-500": "#8b5cf6", "accent-600": "#7c3aed",
                "warning-500": "#f59e0b", "error-500": "#ef4444",
                "success-500": "#10b981", "neutral-50": "#f8fafc",
                "neutral-100": "#f1f5f9", "neutral-200": "#e2e8f0",
                "neutral-600": "#475569", "neutral-900": "#0f172a",
            }
        else:
            self.primary_hue = "Violet/Purple"
            self.colors = {
                "primary-50": "#faf5ff", "primary-100": "#f3e8ff",
                "primary-500": "#a855f7", "primary-600": "#9333ea",
                "primary-700": "#7e22ce", "primary-900": "#581c87",
                "accent-500": "#ec4899", "accent-600": "#db2777",
                "warning-500": "#f59e0b", "error-500": "#ef4444",
                "success-500": "#10b981", "neutral-50": "#fafafa",
                "neutral-100": "#f4f4f5", "neutral-200": "#e4e4e7",
                "neutral-600": "#52525b", "neutral-900": "#18181b",
            }

        self.typography = {
            "font-sans": "'Inter', 'DM Sans', system-ui, sans-serif",
            "font-mono": "'JetBrains Mono', 'Fira Code', monospace",
            "text-xs": "0.75rem / 1rem",
            "text-sm": "0.875rem / 1.25rem",
            "text-base": "1rem / 1.5rem",
            "text-lg": "1.125rem / 1.75rem",
            "text-xl": "1.25rem / 1.75rem",
            "text-2xl": "1.5rem / 2rem",
            "text-3xl": "1.875rem / 2.25rem",
            "text-4xl": "2.25rem / 2.5rem",
            "font-normal": "400",
            "font-medium": "500",
            "font-semibold": "600",
            "font-bold": "700",
        }

        self.spacing = {
            "space-1": "0.25rem (4px)",
            "space-2": "0.5rem (8px)",
            "space-3": "0.75rem (12px)",
            "space-4": "1rem (16px)",
            "space-5": "1.25rem (20px)",
            "space-6": "1.5rem (24px)",
            "space-8": "2rem (32px)",
            "space-10": "2.5rem (40px)",
            "space-12": "3rem (48px)",
            "space-16": "4rem (64px)",
        }

        self.border_radius = {
            "rounded-sm": "0.25rem",
            "rounded": "0.375rem",
            "rounded-md": "0.5rem",
            "rounded-lg": "0.75rem",
            "rounded-xl": "1rem",
            "rounded-2xl": "1.5rem",
            "rounded-full": "9999px",
        }

        self.shadows = {
            "shadow-xs": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
            "shadow-sm": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
            "shadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
            "shadow-md": "0 6px 16px -4px rgb(0 0 0 / 0.1)",
            "shadow-lg": "0 10px 25px -5px rgb(0 0 0 / 0.12)",
            "shadow-xl": "0 20px 40px -8px rgb(0 0 0 / 0.15)",
        }

        self.chart_palette = [
            self.colors["primary-500"],
            self.colors["accent-500"],
            self.colors["success-500"],
            self.colors["warning-500"],
            self.colors["error-500"],
            self.colors["primary-300"] if "primary-300" in self.colors else "#a5b4fc",
        ]


# ─────────────────────────────────────────────────────────────────────────────
# ASCII Renderer
# ─────────────────────────────────────────────────────────────────────────────

def box(title: str, width: int = 72) -> str:
    bar = "─" * (width - 2)
    return f"┌{bar}┐\n│ {title:<{width - 4}} │\n└{bar}┘"


def section(title: str, width: int = 72) -> str:
    bar = "─" * (width - len(title) - 5)
    return f"\n┤ {title} ├{bar}"


def kv_row(key: str, val: str, indent: int = 2, key_width: int = 22) -> str:
    prefix = " " * indent
    return f"{prefix}{key:<{key_width}}  {val}"


def swatch(hex_color: str) -> str:
    """Return a text swatch approximation."""
    return f"[{hex_color}]"


def render_ascii(tokens: DesignTokens, project: str, query: str) -> str:
    W = 72
    lines = []

    # Header
    lines.append("╔" + "═" * (W - 2) + "╗")
    title = f"  DESIGN SYSTEM  ·  {project}"
    lines.append(f"║{title:<{W - 2}}║")
    lines.append("╠" + "═" * (W - 2) + "╣")
    lines.append(f"║  Query : {query:<{W - 12}}║")
    lines.append(f"║  Palette: {tokens.primary_hue:<{W - 13}}║")
    lines.append("╚" + "═" * (W - 2) + "╝")

    # Color Tokens
    lines.append(section("COLOR TOKENS", W))
    lines.append("")
    lines.append("  Semantic")
    for key, val in list(tokens.colors.items())[:8]:
        suf = " ← primary" if "primary-600" in key else (" ← accent" if "accent-500" in key else "")
        lines.append(kv_row(key, f"{swatch(val)}{suf}"))
    lines.append("")
    lines.append("  Feedback")
    for key in ["warning-500", "error-500", "success-500"]:
        if key in tokens.colors:
            lines.append(kv_row(key, swatch(tokens.colors[key])))
    lines.append("")
    lines.append("  Neutral Scale")
    for key in ["neutral-50", "neutral-100", "neutral-200", "neutral-600", "neutral-900"]:
        if key in tokens.colors:
            lines.append(kv_row(key, swatch(tokens.colors[key])))

    # Typography
    lines.append(section("TYPOGRAPHY", W))
    lines.append("")
    lines.append("  Font Families")
    for key in ["font-sans", "font-mono"]:
        lines.append(kv_row(key, tokens.typography[key]))
    lines.append("")
    lines.append("  Type Scale  (size / line-height)")
    for key in ["text-xs", "text-sm", "text-base", "text-lg", "text-xl", "text-2xl", "text-3xl", "text-4xl"]:
        lines.append(kv_row(key, tokens.typography[key]))
    lines.append("")
    lines.append("  Font Weights")
    for key in ["font-normal", "font-medium", "font-semibold", "font-bold"]:
        lines.append(kv_row(key, tokens.typography[key]))

    # Spacing
    lines.append(section("SPACING SCALE", W))
    lines.append("")
    for key, val in tokens.spacing.items():
        lines.append(kv_row(key, val))

    # Border Radius
    lines.append(section("BORDER RADIUS", W))
    lines.append("")
    for key, val in tokens.border_radius.items():
        lines.append(kv_row(key, val))

    # Shadows
    lines.append(section("ELEVATION / SHADOWS", W))
    lines.append("")
    for key, val in tokens.shadows.items():
        lines.append(kv_row(key, val))

    # Chart Palette
    lines.append(section("CHART PALETTE", W))
    lines.append("")
    labels = ["Series A", "Series B", "Series C", "Series D", "Series E", "Series F"]
    for i, (color, label) in enumerate(zip(tokens.chart_palette, labels)):
        lines.append(kv_row(label, f"{swatch(color)}"))

    # Component Patterns
    lines.append(section("COMPONENT PATTERNS", W))
    lines.append("")
    components = _generate_component_patterns(query, tokens)
    for comp in components:
        lines.append(f"  ▸ {comp['name']}")
        for rule in comp["rules"]:
            lines.append(f"      • {rule}")
        lines.append("")

    # Accessibility
    lines.append(section("ACCESSIBILITY CHECKLIST", W))
    lines.append("")
    a11y = [
        "Color contrast ≥ 4.5:1 for normal text, 3:1 for large text (WCAG AA)",
        "All interactive elements have visible focus rings",
        "Form inputs paired with <label> or aria-label",
        "Icon-only buttons include aria-label text",
        "Keyboard navigation: Tab, Shift+Tab, Enter, Space, Escape",
        "Error messages linked to inputs via aria-describedby",
        "Loading states announced via aria-live='polite'",
        "Motion respects prefers-reduced-motion media query",
    ]
    for item in a11y:
        lines.append(f"  ✓  {item}")

    lines.append("")
    lines.append("─" * W)
    lines.append(f"  Generated by UI/UX Pro Max  ·  project: {project}")
    lines.append("─" * W)

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Markdown Renderer
# ─────────────────────────────────────────────────────────────────────────────

def render_markdown(tokens: DesignTokens, project: str, query: str) -> str:
    lines = []

    lines.append(f"# Design System — {project}")
    lines.append("")
    lines.append(f"> **Query:** {query}  ")
    lines.append(f"> **Palette family:** {tokens.primary_hue}")
    lines.append("")

    # Colors
    lines.append("## Color Tokens")
    lines.append("")
    lines.append("| Token | Hex | Role |")
    lines.append("|-------|-----|------|")
    roles = {
        "primary-50": "Background tint", "primary-100": "Hover/active bg",
        "primary-500": "Interactive elements", "primary-600": "Primary actions (CTA)",
        "primary-700": "Pressed state", "primary-900": "Deep emphasis",
        "accent-500": "Highlights / links", "accent-600": "Accent hover",
        "warning-500": "Warnings", "error-500": "Errors / destructive",
        "success-500": "Confirmations / success",
        "neutral-50": "Page background", "neutral-100": "Card background",
        "neutral-200": "Borders / dividers", "neutral-600": "Secondary text",
        "neutral-900": "Primary text",
    }
    for key, val in tokens.colors.items():
        role = roles.get(key, "")
        lines.append(f"| `{key}` | `{val}` | {role} |")

    # Typography
    lines.append("")
    lines.append("## Typography")
    lines.append("")
    lines.append("### Font Families")
    lines.append("")
    lines.append("| Token | Value |")
    lines.append("|-------|-------|")
    for key in ["font-sans", "font-mono"]:
        lines.append(f"| `{key}` | {tokens.typography[key]} |")

    lines.append("")
    lines.append("### Type Scale")
    lines.append("")
    lines.append("| Token | Size / Line Height |")
    lines.append("|-------|--------------------|")
    for key in ["text-xs", "text-sm", "text-base", "text-lg", "text-xl", "text-2xl", "text-3xl", "text-4xl"]:
        lines.append(f"| `{key}` | {tokens.typography[key]} |")

    lines.append("")
    lines.append("### Font Weights")
    lines.append("")
    lines.append("| Token | Weight |")
    lines.append("|-------|--------|")
    for key in ["font-normal", "font-medium", "font-semibold", "font-bold"]:
        lines.append(f"| `{key}` | {tokens.typography[key]} |")

    # Spacing
    lines.append("")
    lines.append("## Spacing Scale")
    lines.append("")
    lines.append("| Token | Value |")
    lines.append("|-------|-------|")
    for key, val in tokens.spacing.items():
        lines.append(f"| `{key}` | {val} |")

    # Border Radius
    lines.append("")
    lines.append("## Border Radius")
    lines.append("")
    lines.append("| Token | Value |")
    lines.append("|-------|-------|")
    for key, val in tokens.border_radius.items():
        lines.append(f"| `{key}` | {val} |")

    # Shadows
    lines.append("")
    lines.append("## Elevation / Shadows")
    lines.append("")
    lines.append("| Token | CSS Value |")
    lines.append("|-------|-----------|")
    for key, val in tokens.shadows.items():
        lines.append(f"| `{key}` | `{val}` |")

    # Chart Palette
    lines.append("")
    lines.append("## Chart Palette")
    lines.append("")
    labels = ["Series A", "Series B", "Series C", "Series D", "Series E", "Series F"]
    lines.append("| Series | Hex |")
    lines.append("|--------|-----|")
    for label, color in zip(labels, tokens.chart_palette):
        lines.append(f"| {label} | `{color}` |")

    # Components
    lines.append("")
    lines.append("## Component Patterns")
    lines.append("")
    for comp in _generate_component_patterns(query, tokens):
        lines.append(f"### {comp['name']}")
        lines.append("")
        for rule in comp["rules"]:
            lines.append(f"- {rule}")
        lines.append("")

    # Accessibility
    lines.append("## Accessibility Checklist")
    lines.append("")
    a11y = [
        "Color contrast ≥ 4.5:1 for normal text, 3:1 for large text (WCAG AA)",
        "All interactive elements have visible focus rings",
        "Form inputs paired with `<label>` or `aria-label`",
        "Icon-only buttons include `aria-label` text",
        "Keyboard navigation: Tab, Shift+Tab, Enter, Space, Escape",
        "Error messages linked to inputs via `aria-describedby`",
        "Loading states announced via `aria-live='polite'`",
        "Motion respects `prefers-reduced-motion` media query",
    ]
    for item in a11y:
        lines.append(f"- [ ] {item}")

    lines.append("")
    lines.append("---")
    lines.append(f"*Generated by UI/UX Pro Max · project: {project}*")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Domain-Specific Renderers
# ─────────────────────────────────────────────────────────────────────────────

def render_domain(query: str, domain: str, fmt: str = "ascii") -> str:
    domain_info = DOMAIN_PROFILES.get(domain, {"label": domain.title(), "tags": []})
    label = domain_info["label"]

    if fmt == "markdown":
        return _render_domain_markdown(query, domain, label)
    return _render_domain_ascii(query, domain, label)


def _render_domain_ascii(query: str, domain: str, label: str) -> str:
    W = 72
    lines = []
    lines.append("╔" + "═" * (W - 2) + "╗")
    header = f"  DOMAIN GUIDE  ·  {label}"
    lines.append(f"║{header:<{W - 2}}║")
    lines.append("╠" + "═" * (W - 2) + "╣")
    lines.append(f"║  Query : {query:<{W - 12}}║")
    lines.append("╚" + "═" * (W - 2) + "╝")

    guidelines = _domain_guidelines(query, domain)
    for section_title, items in guidelines.items():
        lines.append(section(section_title, W))
        lines.append("")
        for item in items:
            wrapped = textwrap.wrap(item, width=W - 8)
            for i, wline in enumerate(wrapped):
                prefix = "  •  " if i == 0 else "      "
                lines.append(f"{prefix}{wline}")
        lines.append("")

    lines.append("─" * W)
    return "\n".join(lines)


def _render_domain_markdown(query: str, domain: str, label: str) -> str:
    lines = []
    lines.append(f"# Domain Guide — {label}")
    lines.append(f"> Query: *{query}*")
    lines.append("")

    guidelines = _domain_guidelines(query, domain)
    for section_title, items in guidelines.items():
        lines.append(f"## {section_title}")
        lines.append("")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines)


def _domain_guidelines(query: str, domain: str) -> dict:
    """Return domain-specific guidelines as ordered dict of sections."""
    q = query.lower()

    if domain == "style":
        return {
            "Layout Principles": [
                "Use a fixed left sidebar (240–280px) for primary navigation on desktop",
                "Main content area with max-width 1280px, centered with auto margins",
                "Card-based content grouping with consistent 24px internal padding",
                "Sticky top bar (64px height) for global actions and user menu",
                "Collapsible sidebar on tablet (768px), bottom nav on mobile (<640px)",
            ],
            "Visual Style": [
                "Clean, flat design with subtle depth via shadow-sm on cards",
                "White (#ffffff) card surfaces on neutral-50 page background",
                "Consistent 8px border radius on cards, 4px on inputs and buttons",
                "Minimal use of color: primary for CTAs, neutral for most UI chrome",
                "Micro-borders (1px neutral-200) as dividers instead of heavy rules",
            ],
            "Density Considerations": [
                "Default density: comfortable (16px row padding, 14px font)",
                "Compact mode: 8px row padding for power users / data-heavy tables",
                "Touch targets minimum 44×44px on mobile interfaces",
                "Consistent 16px horizontal page gutters on all breakpoints",
            ],
        }

    elif domain == "typography":
        return {
            "Font Recommendations": [
                "Primary: Inter (Google Fonts) — excellent screen legibility at all sizes",
                "Alternative: DM Sans — slightly more personality while staying professional",
                "Monospace: JetBrains Mono for code, IDs, and numeric data",
                "Fallback stack: system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
            ],
            "Type Scale Usage": [
                "text-xs (12px): Labels, captions, table footnotes",
                "text-sm (14px): Body copy, form fields, table cells — most UI text",
                "text-base (16px): Card bodies, descriptions, paragraph text",
                "text-lg (18px): Section intros, lead paragraphs",
                "text-xl–2xl (20–24px): Card headers, section titles",
                "text-3xl–4xl (30–36px): Page titles, hero metrics",
            ],
            "Readability Rules": [
                "Body text: line-height 1.5–1.6 for comfortable reading",
                "Headings: line-height 1.15–1.25, letter-spacing -0.01em",
                "Max line length: 65–75 characters for prose, no limit for UI labels",
                "Minimum body font size 14px (never 12px for body copy)",
                "Use font-medium (500) for UI labels, font-semibold (600) for emphasis",
                "Avoid ALL CAPS for more than 4-word labels — use title case",
            ],
            "Accessible Typography": [
                "Normal text: minimum 4.5:1 contrast against background (WCAG AA)",
                "Large text (18px+ or 14px bold): minimum 3:1 contrast",
                "Use relative units (rem/em) not px for font sizes",
                "Respect user OS font-size preferences with html { font-size: 100%; }",
            ],
        }

    elif domain == "chart":
        return {
            "Chart Type Selection": [
                "Progress toward goal → Radial gauge or horizontal progress bar",
                "Enrollment over time → Area chart or line chart with fill",
                "Category breakdown → Horizontal bar chart (easier label reading)",
                "Part-to-whole (max 5 segments) → Donut chart",
                "Comparison across groups → Grouped bar chart",
                "Distribution / outliers → Box plot or histogram",
                "KPI snapshot → Stat card with sparkline and trend indicator",
            ],
            "Data Visualization Principles": [
                "Always label axes, include units in axis title not individual labels",
                "Use chart-specific color tokens (not brand colors) for series",
                "Provide text alternatives: data table accessible via toggle",
                "Animate on mount (300–500ms ease-out), no looping animations",
                "Show empty state with meaningful message, not blank chart area",
                "Minimum bar/line height/width for readability: 2px line, 12px bar",
            ],
            "Dashboard Layout": [
                "Top row: 3–4 KPI stat cards spanning full width",
                "Second row: Primary chart (60% width) + secondary metric (40%)",
                "Third row: Table or list view for detail",
                "Use skeleton loaders (not spinners) while data fetches",
                "Provide date range selector affecting all charts simultaneously",
                "Export button (CSV/PNG) on each chart for data portability",
            ],
            "Recommended Libraries": [
                "React: Recharts (simple), Victory (customizable), Nivo (rich)",
                "Vanilla JS: Chart.js (easy), D3.js (maximum control)",
                "Vue: Vue-Chartjs, ApexCharts Vue wrapper",
                "All: ApexCharts has good defaults and accessibility support",
            ],
        }

    elif domain == "color":
        return {
            "Color Role Definitions": [
                "primary-600: Primary action buttons, active nav links, key UI chrome",
                "primary-100: Chip/badge backgrounds, subtle highlights",
                "accent-500: Secondary actions, links, progress indicators",
                "neutral-50: Page background (never pure white for large areas)",
                "neutral-100: Card backgrounds, input backgrounds",
                "neutral-200: Borders, dividers, skeleton loaders",
                "neutral-600: Secondary text, placeholders, helper text",
                "neutral-900: Primary text, headings",
            ],
            "Semantic Colors": [
                "success-500 (#10b981): Completed states, positive trends, confirmations",
                "warning-500 (#f59e0b): Attention needed, approaching limits, cautions",
                "error-500 (#ef4444): Errors, destructive actions, failed states",
                "info-500 (#3b82f6): Informational messages, neutral notifications",
            ],
            "Color Usage Rules": [
                "Never use color as the ONLY differentiator — pair with icon or text",
                "Maximum 3 distinct hues per view to avoid visual noise",
                "Background-to-text contrast: neutral-900 on neutral-50 = ~16:1",
                "Colored text minimum: primary-700 on white meets 4.5:1",
                "Dark mode: invert neutral scale, keep primary-400/500 for accents",
            ],
        }

    elif domain == "component":
        return {
            "Button System": [
                "Primary: primary-600 bg, white text, hover primary-700, active primary-800",
                "Secondary: white bg, primary-600 border+text, hover primary-50 bg",
                "Ghost: transparent bg, neutral-600 text, hover neutral-100 bg",
                "Destructive: error-500 bg, white text — use sparingly",
                "Sizes: sm (32px h, px-3), md (40px h, px-4), lg (48px h, px-6)",
                "Always include loading spinner state for async actions",
            ],
            "Form Inputs": [
                "Height: 40px (md), 36px (sm), border neutral-200, focus ring primary-500",
                "Error state: border-error-500, helper text in error-600 below input",
                "Label above input (not placeholder as label), required asterisk in error-500",
                "Disabled: opacity-50, cursor-not-allowed, no pointer events",
                "Select: custom chevron icon, same sizing as text inputs",
            ],
            "Data Tables": [
                "Sticky header row, zebra striping with neutral-50/white alternation",
                "Row hover: neutral-50 background highlight",
                "Sortable columns: show sort icon (neutral-400), active sort in primary-600",
                "Pagination: show total count, items per page selector, prev/next",
                "Empty state: centered icon + message + optional CTA",
                "Loading: full-table skeleton with animated pulse rows",
            ],
            "Navigation": [
                "Sidebar items: 44px height, 12px px, 8px py, rounded-lg",
                "Active item: primary-50 bg, primary-700 text, primary-600 left border 2px",
                "Hover item: neutral-100 bg, neutral-900 text",
                "Group labels: text-xs font-semibold uppercase tracking-wider neutral-500",
                "Icon size: 20px, consistent stroke-width: 1.5",
            ],
        }

    else:  # spacing
        return {
            "Spacing System (8px base)": [
                "All spacing values are multiples of 4px, primary multiples of 8px",
                "space-1 (4px): Icon-to-label gaps, tight inline spacing",
                "space-2 (8px): Input internal padding (y), badge padding",
                "space-3 (12px): Button padding (y), small card padding",
                "space-4 (16px): Standard component padding, row height padding",
                "space-6 (24px): Card internal padding, section spacing",
                "space-8 (32px): Between major sections",
                "space-12 (48px): Page section separation",
                "space-16 (64px): Hero/header spacing",
            ],
            "Grid System": [
                "12-column grid, 24px gutters, 16px outer margins",
                "Breakpoints: sm 640px, md 768px, lg 1024px, xl 1280px, 2xl 1536px",
                "Dashboard sidebar: fixed 256px, main: fluid remaining width",
                "Cards: 1-col mobile, 2-col tablet, 3–4 col desktop",
                "Max content width: 1280px (dashboard), 768px (forms/articles)",
            ],
        }


# ─────────────────────────────────────────────────────────────────────────────
# Stack-Specific Guidelines
# ─────────────────────────────────────────────────────────────────────────────

def render_stack(query: str, stack: str, fmt: str = "ascii") -> str:
    stack_info = STACK_TEMPLATES.get(stack)
    if not stack_info:
        available = ", ".join(STACK_TEMPLATES.keys())
        return f"Unknown stack '{stack}'. Available: {available}"

    guidelines = _stack_guidelines(query, stack)

    if fmt == "markdown":
        return _render_stack_markdown(query, stack, stack_info, guidelines)
    return _render_stack_ascii(query, stack, stack_info, guidelines)


def _render_stack_ascii(query: str, stack: str, stack_info: dict, guidelines: dict) -> str:
    W = 72
    lines = []
    lines.append("╔" + "═" * (W - 2) + "╗")
    header = f"  STACK GUIDE  ·  {stack_info['label']}"
    lines.append(f"║{header:<{W - 2}}║")
    lines.append("╠" + "═" * (W - 2) + "╣")
    lines.append(f"║  Query : {query:<{W - 12}}║")
    lines.append("╚" + "═" * (W - 2) + "╝")

    for section_title, items in guidelines.items():
        lines.append(section(section_title, W))
        lines.append("")
        for item in items:
            if item.startswith("```") or item.startswith("//") or item.startswith("<") or item.startswith("const ") or item.startswith("import "):
                lines.append(f"  {item}")
            else:
                wrapped = textwrap.wrap(item, width=W - 8)
                for i, wline in enumerate(wrapped):
                    prefix = "  •  " if i == 0 else "      "
                    lines.append(f"{prefix}{wline}")
        lines.append("")

    lines.append("─" * W)
    return "\n".join(lines)


def _render_stack_markdown(query: str, stack: str, stack_info: dict, guidelines: dict) -> str:
    lines = []
    lines.append(f"# Stack Guide — {stack_info['label']}")
    lines.append(f"> Query: *{query}*")
    lines.append("")

    for section_title, items in guidelines.items():
        lines.append(f"## {section_title}")
        lines.append("")
        in_code = False
        for item in items:
            if item.startswith("```"):
                lines.append(item)
                in_code = not in_code
            elif in_code:
                lines.append(item)
            else:
                lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines)


def _stack_guidelines(query: str, stack: str) -> dict:
    q = query.lower()

    if stack == "react":
        is_form = any(w in q for w in ["form", "input", "validation", "enroll"])
        is_layout = any(w in q for w in ["layout", "responsive", "admin", "dashboard"])

        sections = {
            "Project Structure": [
                "src/components/ui/        — primitives (Button, Input, Badge)",
                "src/components/layout/    — Shell, Sidebar, Header, PageContainer",
                "src/components/features/  — domain-specific composite components",
                "src/hooks/                — useDebounce, usePagination, useForm",
                "src/utils/                — formatters, validators, API helpers",
            ],
            "Styling Approach": [
                "Tailwind CSS utility classes as primary styling method",
                "clsx / class-variance-authority (CVA) for conditional class logic",
                "CSS custom properties for design tokens (colors, spacing, radius)",
                "Avoid inline styles except for truly dynamic values (chart colors)",
            ],
        }

        if is_form:
            sections["Form Validation Pattern"] = [
                "Use react-hook-form for performance and DX",
                "Zod schema for validation — colocate schema with component",
                "```",
                "import { useForm } from 'react-hook-form';",
                "import { zodResolver } from '@hookform/resolvers/zod';",
                "import { z } from 'zod';",
                "",
                "const schema = z.object({",
                "  email: z.string().email('Valid email required'),",
                "  name: z.string().min(2, 'Name must be at least 2 characters'),",
                "});",
                "",
                "const { register, handleSubmit, formState: { errors } } = useForm({",
                "  resolver: zodResolver(schema),",
                "});",
                "```",
                "Show inline errors below each field, not in a top banner",
                "Disable submit button while submitting, show loading spinner",
                "Announce form errors to screen readers via aria-live region",
            ]

        if is_layout:
            sections["Responsive Layout"] = [
                "```",
                "// AppShell.jsx",
                "const AppShell = ({ children }) => (",
                "  <div className='flex min-h-screen bg-neutral-50'>",
                "    <Sidebar className='hidden lg:flex w-64 flex-shrink-0' />",
                "    <main className='flex-1 overflow-auto'>",
                "      <Header />",
                "      <div className='p-6 max-w-7xl mx-auto'>",
                "        {children}",
                "      </div>",
                "    </main>",
                "  </div>",
                ");",
                "```",
                "Use CSS Grid for dashboard card layouts: grid-cols-1 md:grid-cols-2 xl:grid-cols-4",
                "Lazy-load route components with React.lazy + Suspense",
                "Use useMediaQuery hook for programmatic breakpoint detection",
            ]

        sections["Performance"] = [
            "Memoize expensive list renders with React.memo",
            "Use useMemo for derived data calculations (filtered/sorted lists)",
            "Virtualize long lists with @tanstack/react-virtual",
            "Debounce search inputs (300ms) before triggering API calls",
            "Code-split at route level, not component level by default",
        ]

        sections["Accessibility"] = [
            "Use semantic HTML: <nav>, <main>, <aside>, <section>, <article>",
            "Focus management on route changes: focus main heading or skip link",
            "Radix UI primitives for dialogs, dropdowns, tooltips (built-in a11y)",
            "Test with axe DevTools browser extension during development",
        ]

        return sections

    elif stack == "html-tailwind":
        is_responsive = any(w in q for w in ["responsive", "admin", "layout", "dashboard"])
        is_form = any(w in q for w in ["form", "input", "validation"])

        sections = {
            "Tailwind Configuration": [
                "```",
                "// tailwind.config.js",
                "module.exports = {",
                "  content: ['./**/*.html', './**/*.js'],",
                "  theme: {",
                "    extend: {",
                "      colors: {",
                "        primary: { 50: '#eef2ff', 500: '#6366f1', 600: '#4f46e5' },",
                "        neutral: { 50: '#f9fafb', 200: '#e5e7eb', 900: '#111827' },",
                "      },",
                "      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },",
                "    },",
                "  },",
                "  plugins: [require('@tailwindcss/forms')],",
                "};",
                "```",
            ],
            "Utility Class Conventions": [
                "Group utilities: layout → spacing → sizing → typography → color → effects",
                "Extract repeated patterns to @apply in a components.css layer",
                "Use gap-* over margin on flex/grid children (easier to manage)",
                "Prefer p-4 over px-4 py-4 unless values differ",
            ],
        }

        if is_responsive:
            sections["Responsive Admin Layout"] = [
                "```",
                "<!-- Admin Shell -->",
                "<div class='min-h-screen bg-neutral-50 flex'>",
                "  <!-- Sidebar (hidden on mobile) -->",
                "  <aside class='hidden lg:flex flex-col w-64 bg-white border-r",
                "               border-neutral-200 p-4 gap-1'>",
                "    <nav><!-- nav items --></nav>",
                "  </aside>",
                "",
                "  <!-- Main -->",
                "  <div class='flex-1 flex flex-col min-h-screen'>",
                "    <header class='h-16 bg-white border-b border-neutral-200",
                "                  flex items-center px-6'>",
                "      <!-- header content -->",
                "    </header>",
                "    <main class='flex-1 p-6'>",
                "      <div class='max-w-7xl mx-auto'>",
                "        <!-- page content -->",
                "      </div>",
                "    </main>",
                "  </div>",
                "</div>",
                "```",
            ]

        if is_form:
            sections["Form Pattern"] = [
                "```",
                "<!-- Accessible form input -->",
                "<div class='flex flex-col gap-1.5'>",
                "  <label for='email'",
                "         class='text-sm font-medium text-neutral-700'>",
                "    Email address <span class='text-error-500'>*</span>",
                "  </label>",
                "  <input id='email' type='email' name='email'",
                "         class='h-10 px-3 rounded-lg border border-neutral-200",
                "                focus:outline-none focus:ring-2 focus:ring-primary-500",
                "                focus:border-transparent text-sm'",
                "         aria-required='true' aria-describedby='email-error' />",
                "  <p id='email-error' role='alert'",
                "     class='text-xs text-error-600 hidden'>",
                "    Please enter a valid email address.",
                "  </p>",
                "</div>",
                "```",
            ]

        sections["Component Snippets"] = [
            "```",
            "<!-- Stat card -->",
            "<div class='bg-white rounded-2xl p-6 shadow-sm border border-neutral-100'>",
            "  <p class='text-sm text-neutral-500 font-medium'>Total Enrolled</p>",
            "  <p class='text-3xl font-bold text-neutral-900 mt-1'>1,284</p>",
            "  <p class='text-xs text-success-600 mt-2'>↑ 12% vs last month</p>",
            "</div>",
            "```",
            "Use @tailwindcss/forms plugin to normalize cross-browser input appearance",
            "Alpine.js for lightweight JS interactions (dropdowns, toggles, modals)",
        ]

        return sections

    else:
        return {"Guidelines": [f"Stack '{stack}' guidelines not yet available."]}


# ─────────────────────────────────────────────────────────────────────────────
# Component Pattern Generator
# ─────────────────────────────────────────────────────────────────────────────

def _generate_component_patterns(query: str, tokens: DesignTokens) -> list:
    q = query.lower()
    components = []

    # Always include core components
    components.append({
        "name": "Button — Primary",
        "rules": [
            f"Background: {tokens.colors.get('primary-600', '#4f46e5')} (primary-600)",
            "Text: white, font-medium, text-sm",
            "Padding: 10px 16px (md), 8px 12px (sm), 12px 20px (lg)",
            "Border radius: rounded-lg (0.5rem)",
            "Hover: darken to primary-700, transition 150ms ease",
            "Focus: 2px ring primary-500 with 2px offset",
            "Disabled: opacity-50, cursor-not-allowed",
        ],
    })

    components.append({
        "name": "Card",
        "rules": [
            f"Background: white, border: 1px {tokens.colors.get('neutral-200', '#e5e7eb')}",
            "Border radius: rounded-2xl (1.5rem)",
            "Padding: 24px (default)",
            "Shadow: shadow-sm on hover → shadow-md (transition)",
            "Header: font-semibold text-neutral-900, body: text-sm text-neutral-600",
        ],
    })

    if any(w in q for w in ["form", "input", "enroll", "student", "user"]):
        components.append({
            "name": "Form Input",
            "rules": [
                "Height: 40px, padding: 10px 12px",
                f"Border: 1px {tokens.colors.get('neutral-200', '#e5e7eb')}, radius: rounded-lg",
                f"Focus ring: 2px {tokens.colors.get('primary-500', '#6366f1')} (primary-500)",
                "Error state: border-error-500, helper text below in error-600",
                "Label: text-sm font-medium text-neutral-700, 6px above input",
            ],
        })

    if any(w in q for w in ["table", "list", "enrollment", "tracking", "data"]):
        components.append({
            "name": "Data Table",
            "rules": [
                "Header: text-xs font-semibold uppercase tracking-wider neutral-500",
                "Row height: 48px default, hover: neutral-50 bg",
                "Zebra stripes: white / neutral-50 alternating",
                "Sticky header on scroll with top shadow indicator",
                "Sort icons: neutral-300 default, primary-600 active",
                "Pagination row: border-top neutral-200, flex space-between",
            ],
        })

    if any(w in q for w in ["dashboard", "analytics", "metric", "kpi", "chart", "progress"]):
        components.append({
            "name": "Stat / KPI Card",
            "rules": [
                "Metric value: text-3xl font-bold neutral-900",
                "Label: text-sm font-medium neutral-500",
                "Trend indicator: success-600 (↑), error-600 (↓), neutral-500 (—)",
                "Sparkline: 64px height, chart palette series A color",
                "Period selector: text-xs dropdown in card top-right corner",
            ],
        })

    if any(w in q for w in ["nav", "sidebar", "menu", "navigation"]):
        components.append({
            "name": "Sidebar Navigation Item",
            "rules": [
                "Height: 44px, padding: 12px, border-radius: rounded-lg",
                f"Active: bg primary-50, text primary-700, left-border 2px primary-600",
                "Hover: bg neutral-100, text neutral-900",
                "Icon: 20px, stroke-width 1.5, aligned left",
                "Label: text-sm font-medium, truncate overflow",
                "Group label: text-xs uppercase tracking-wider neutral-400, px-3 mt-4",
            ],
        })

    return components


# ─────────────────────────────────────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="UI/UX Pro Max — Design System & Guidelines Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          # Full design system (ASCII)
          python3 search.py "workforce apprenticeship management" --design-system -p "I-LEAD AMS V3"

          # Full design system (Markdown)
          python3 search.py "nonprofit education workforce dashboard" --design-system -f markdown

          # Domain-specific guidelines
          python3 search.py "clean professional dashboard" --domain style
          python3 search.py "readable sans-serif accessible" --domain typography
          python3 search.py "progress tracking enrollment" --domain chart

          # Stack-specific code patterns
          python3 search.py "student enrollment form validation" --stack react
          python3 search.py "responsive admin layout" --stack html-tailwind
        """),
    )

    parser.add_argument("query", help="Natural language description of the UI/UX context")
    parser.add_argument("--design-system", action="store_true", help="Generate full design system")
    parser.add_argument("-p", "--project", default="Untitled Project", help="Project name")
    parser.add_argument(
        "-f", "--format",
        choices=["ascii", "markdown"],
        default="ascii",
        help="Output format (default: ascii)",
    )
    parser.add_argument(
        "--domain",
        choices=list(DOMAIN_PROFILES.keys()),
        help="Focus on a specific design domain",
    )
    parser.add_argument(
        "--stack",
        choices=list(STACK_TEMPLATES.keys()),
        help="Generate stack-specific code guidelines",
    )

    args = parser.parse_args()

    # Determine what to generate
    if args.domain:
        output = render_domain(args.query, args.domain, fmt=args.format)
    elif args.stack:
        output = render_stack(args.query, args.stack, fmt=args.format)
    elif args.design_system:
        tokens = DesignTokens(project=args.project, query=args.query)
        if args.format == "markdown":
            output = render_markdown(tokens, args.project, args.query)
        else:
            output = render_ascii(tokens, args.project, args.query)
    else:
        # Default: full design system in ASCII
        tokens = DesignTokens(project=args.project, query=args.query)
        output = render_ascii(tokens, args.project, args.query)

    print(output)


if __name__ == "__main__":
    main()
