"""Curated mechanical engineering reference notes for retrieval by the agent.
These are general diagnostic prompts, not machine-specific limits or standards."""
from __future__ import annotations

KNOWLEDGE = {
    "cavitation": {
        "aliases": ["pump cavitation", "suction starvation", "low suction pressure"],
        "mechanism": "Local pressure falls below the liquid vapour pressure, forming bubbles that collapse as pressure recovers.",
        "indicators": ["gravel-like or crackling noise", "unstable discharge pressure or flow", "vibration", "pitting on impeller surfaces"],
        "checks": ["compare measured suction pressure with the pump's required NPSH conditions", "check suction strainer and line for blockage", "verify liquid temperature and level", "inspect impeller for pitting when safely isolated"],
        "cautions": "Do not infer cavitation from noise alone; confirm hydraulic conditions and inspect safely under lockout/tagout.",
    },
    "shaft misalignment": {
        "aliases": ["coupling misalignment", "angular misalignment", "parallel misalignment"],
        "mechanism": "The connected shaft centre-lines or angular axes are not within the coupling and machine alignment tolerances.",
        "indicators": ["axial vibration may be prominent", "coupling heating or wear", "repeat bearing or seal failures", "vibration changes after thermal growth"],
        "checks": ["measure cold and, where required, hot alignment using laser or dial indicators", "inspect coupling element and fasteners", "review soft foot and pipe strain"],
        "cautions": "Vibration direction alone is not conclusive; use machine-specific alignment tolerances.",
    },
    "bearing damage": {
        "aliases": ["rolling element bearing fault", "inner race defect", "outer race defect", "ball defect"],
        "mechanism": "Surface damage, fatigue, contamination, poor fit, incorrect preload or lubrication problems disrupt rolling contact.",
        "indicators": ["bearing-related spectral peaks when speed and geometry are known", "increased high-frequency vibration", "temperature rise", "roughness or noise"],
        "checks": ["confirm bearing designation and shaft speed before calculating characteristic frequencies", "collect repeatable vibration at bearing housings", "check lubrication type, quantity and contamination", "inspect fit and installation procedure"],
        "cautions": "Do not label a bearing defect from an FFT peak without speed, bearing geometry, sampling details and corroborating evidence.",
    },
    "rotor imbalance": {
        "aliases": ["unbalance", "mass imbalance"],
        "mechanism": "The rotor mass centre does not coincide with its rotational axis, producing a speed-related rotating force.",
        "indicators": ["often elevated radial vibration near 1x running speed", "response changes with speed", "possible phase consistency"],
        "checks": ["measure vibration and phase at known RPM", "inspect for deposits, missing balance weights or damage", "rule out looseness and resonance before balancing"],
        "cautions": "A 1x component is not uniquely diagnostic of imbalance.",
    },
    "mechanical looseness": {
        "aliases": ["loose foundation", "loose fasteners", "soft foot"],
        "mechanism": "Insufficient clamping, cracked supports or fit clearance permits relative motion and impacts.",
        "indicators": ["multiple harmonics", "intermittent impacts", "movement at feet or supports"],
        "checks": ["inspect foundation, hold-down bolts and baseplate after isolation", "check soft foot and structural cracks", "review pipe strain"],
        "cautions": "Never tighten or probe components while equipment is running unless an approved procedure explicitly permits it.",
    },
    "lubrication failure": {
        "aliases": ["oil starvation", "grease degradation", "wrong lubricant"],
        "mechanism": "The lubricant film is insufficient or degraded because of incorrect grade, quantity, contamination or delivery failure.",
        "indicators": ["temperature rise", "noise and vibration", "discoloured or contaminated lubricant", "repeat bearing distress"],
        "checks": ["verify lubricant specification and quantity against OEM instructions", "check delivery paths, seals and contamination", "review relubrication interval and operating temperature"],
        "cautions": "More lubricant is not always better; over-greasing can also cause heating.",
    },
}


def search_knowledge(query: str, limit: int = 3) -> list[dict]:
    terms = {t.lower() for t in query.replace("/", " ").replace(",", " ").split() if len(t) > 2}
    scored = []
    for topic, item in KNOWLEDGE.items():
        text = " ".join([topic, *item["aliases"], item["mechanism"], *item["indicators"], *item["checks"]]).lower()
        score = sum(1 for term in terms if term in text)
        if score:
            scored.append((score, topic, item))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [{"topic": topic, **item} for _, topic, item in scored[:max(1, min(limit, 5))]]
