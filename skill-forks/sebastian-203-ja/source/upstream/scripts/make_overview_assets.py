#!/usr/bin/env python
"""Generate GitHub README overview images for Academic Review Decksmith."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "gallery"
OUT.mkdir(parents=True, exist_ok=True)
MPL_CACHE = ROOT / ".matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


NAVY = "#0B3A5B"
BLUE = "#1D70B7"
CYAN = "#62B6CB"
GREEN = "#248F73"
ORANGE = "#D9731F"
RED = "#C8102E"
PALE = "#F4F8FB"
TEXT = "#202A33"
MUTED = "#5D6B78"


def clean(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def box(ax, xy, wh, title, body, color):
    x, y = xy
    w, h = wh
    rect = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        fc="white",
        ec=color,
        lw=1.7,
    )
    ax.add_patch(rect)
    ax.text(x + 0.03, y + h - 0.06, title, fontsize=13, fontweight="bold", color=color, va="top")
    ax.text(x + 0.03, y + h - 0.13, body, fontsize=9.4, color=TEXT, va="top", linespacing=1.25)


def arrow(ax, start, end, color=BLUE):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=15,
            lw=1.8,
            color=color,
            connectionstyle="arc3,rad=0.0",
        )
    )


def make_banner():
    fig, ax = plt.subplots(figsize=(14, 6))
    clean(ax)
    fig.patch.set_facecolor("white")
    ax.add_patch(FancyBboxPatch((0.015, 0.05), 0.97, 0.90, boxstyle="round,pad=0.02,rounding_size=0.045", fc=PALE, ec="#D6E4EF", lw=1.0))
    ax.text(0.065, 0.82, "Academic Review Decksmith", fontsize=32, fontweight="bold", color=NAVY)
    ax.text(0.067, 0.735, "From scholarly review drafts to citation-aware, presentation-ready academic decks.", fontsize=15, color=MUTED)
    ax.text(0.067, 0.655, "A Codex skill for rigorous structure, figure/formula explanation, template fidelity, and export-based QA.", fontsize=12.5, color=TEXT)

    nodes = [
        ("Sources", "papers\nreview draft\ntemplate", BLUE),
        ("Argument", "background\nmechanism\nmodel/control", GREEN),
        ("Visuals", "literature figures\nredrawn diagrams\neditable tables", ORANGE),
        ("Deck QA", "PNG export\ntext scan\nsource check", RED),
    ]
    x0 = 0.07
    for i, (title, body, color) in enumerate(nodes):
        x = x0 + i * 0.225
        box(ax, (x, 0.22), (0.17, 0.25), title, body, color)
        if i < len(nodes) - 1:
            arrow(ax, (x + 0.17, 0.345), (x0 + (i + 1) * 0.225, 0.345), color=CYAN)

    ax.text(0.07, 0.12, "Designed for research talks, thesis defenses, journal-club reviews, and course presentations.", fontsize=11.5, color=NAVY, fontweight="bold")
    fig.savefig(OUT / "project-overview.png", dpi=220, bbox_inches="tight")
    fig.savefig(OUT / "project-overview.svg", bbox_inches="tight")
    plt.close(fig)


def make_safe_deck_preview():
    fig, axes = plt.subplots(3, 4, figsize=(14, 8))
    fig.patch.set_facecolor("white")
    titles = [
        "Title",
        "Structure",
        "Background",
        "Mechanism",
        "Taxonomy",
        "Modeling",
        "Dynamics",
        "Control",
        "Applications",
        "Limitations",
        "Summary",
        "QA",
    ]
    colors = [BLUE, GREEN, ORANGE, RED]
    for i, ax in enumerate(axes.flat):
        clean(ax)
        ax.add_patch(FancyBboxPatch((0.02, 0.05), 0.96, 0.88, boxstyle="round,pad=0.01,rounding_size=0.02", fc="white", ec="#D6E4EF", lw=1.0))
        ax.add_patch(FancyBboxPatch((0.05, 0.79), 0.90, 0.08, boxstyle="round,pad=0.005,rounding_size=0.004", fc=NAVY, ec=NAVY, lw=0.0))
        ax.text(0.07, 0.62, titles[i], fontsize=13, fontweight="bold", color=NAVY)
        ax.text(0.07, 0.51, "one claim", fontsize=8, color=MUTED)
        ax.add_patch(FancyBboxPatch((0.07, 0.26), 0.38, 0.16, boxstyle="round,pad=0.01,rounding_size=0.01", fc=PALE, ec=colors[i % 4], lw=1.0))
        ax.add_patch(FancyBboxPatch((0.53, 0.23), 0.34, 0.26, boxstyle="round,pad=0.01,rounding_size=0.01", fc="#FFFFFF", ec="#C9D8E6", lw=1.0))
        ax.plot([0.57, 0.83], [0.34, 0.39], color=colors[i % 4], lw=1.6)
        ax.plot([0.57, 0.83], [0.30, 0.25], color=CYAN, lw=1.3)
        ax.add_patch(FancyBboxPatch((0.07, 0.12), 0.80, 0.06, boxstyle="round,pad=0.005,rounding_size=0.006", fc="#F8FAFC", ec="#D8E3EC", lw=0.8))
        ax.text(0.08, 0.14, "figure/formula explanation", fontsize=6.5, color=MUTED)
    fig.suptitle("Synthetic Academic Deck Preview", fontsize=20, fontweight="bold", color=NAVY, y=0.98)
    fig.savefig(OUT / "snake-robot-demo-overview.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_banner()
    make_safe_deck_preview()
    print(OUT / "project-overview.png")
