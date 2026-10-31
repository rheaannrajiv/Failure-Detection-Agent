"""Mechanical fault ranking engine extracted from the existing Streamlit app.

The initial rules and weights intentionally preserve the legacy behaviour.
Scores are heuristic evidence scores, not calibrated probabilities.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FAILURES = {
    "Shaft Misalignment": {
        "symptoms": [
            "axial vibration",
            "coupling problems",
            "excessive vibration"
        ],
        "checks": [
            "Check shaft alignment",
            "Inspect coupling condition"
        ]
    },
    "Bearing Damage": {
        "symptoms": [
            "abnormal noise",
            "excessive vibration",
            "high bearing temperature"
        ],
        "checks": [
            "Inspect bearing condition",
            "Check vibration measurements"
        ]
    },
    "Rotor Imbalance": {
        "symptoms": [
            "speed-dependent vibration",
            "excessive vibration"
        ],
        "checks": [
            "Measure vibration at different speeds",
            "Inspect rotor balance"
        ]
    },
    "Inadequate Lubrication": {
        "symptoms": [
            "high bearing temperature",
            "lubrication problems",
            "abnormal noise"
        ],
        "checks": [
            "Check lubricant level and condition",
            "Inspect lubrication system"
        ]
    },
    "Mechanical Looseness": {
        "symptoms": [
            "excessive vibration",
            "loose mounting",
            "abnormal noise"
        ],
        "checks": [
            "Inspect mounting bolts",
            "Check foundation and fasteners"
        ]
    },
    "Cooling Problems": {
        "symptoms": [
            "motor overheating",
            "restricted airflow",
            "high operating temperature"
        ],
        "checks": [
            "Inspect cooling passages",
            "Check fan operation and airflow"
        ]
    },
    "Gear Tooth Damage": {
        "symptoms": [
            "gearbox noise",
            "abnormal vibration",
            "metal particles in lubricant"
        ],
        "checks": [
            "Inspect gear teeth",
            "Check gearbox lubricant for metal particles"
        ]
    },
    "Belt Slippage": {
        "symptoms": [
            "belt squealing",
            "reduced driven speed",
            "belt overheating"
        ],
        "checks": [
            "Inspect belt tension",
            "Inspect belt wear and pulley alignment"
        ]
    },
    "Chain Wear": {
        "symptoms": [
            "chain noise",
            "chain elongation",
            "irregular chain movement"
        ],
        "checks": [
            "Measure chain elongation",
            "Inspect chain links and sprockets"
        ]
    },
    "Pump Cavitation": {
        "symptoms": [
            "crackling pump noise",
            "fluctuating flow",
            "pump vibration"
        ],
        "checks": [
            "Check pump suction pressure",
            "Inspect impeller for cavitation damage"
        ]
    },
    "Pump Blockage": {
        "symptoms": [
            "low flow rate",
            "high discharge pressure",
            "reduced pump output"
        ],
        "checks": [
            "Inspect suction strainer and inlet",
            "Check discharge line for blockage"
        ]
    },
    "Seal Failure": {
        "symptoms": [
            "fluid leakage",
            "pressure loss",
            "seal overheating"
        ],
        "checks": [
            "Inspect mechanical seal",
            "Check seal flushing and operating conditions"
        ]
    },
    "Motor Electrical Fault": {
        "symptoms": [
            "unbalanced motor current",
            "motor electrical noise",
            "motor overheating"
        ],
        "checks": [
            "Measure current in each motor phase",
            "Inspect motor winding insulation"
        ]
    },
    "Motor Overload": {
        "symptoms": [
            "high motor current",
            "motor overheating",
            "reduced motor speed"
        ],
        "checks": [
            "Measure motor current under load",
            "Check driven equipment for excessive load"
        ]
    },
    "Fan or Impeller Damage": {
        "symptoms": [
            "reduced airflow",
            "fan vibration",
            "abnormal fan noise"
        ],
        "checks": [
            "Inspect fan blades or impeller",
            "Measure airflow and check rotation"
        ]
    },
    "Foundation Failure": {
        "symptoms": [
            "foundation cracks",
            "loose anchor bolts",
            "structural vibration"
        ],
        "checks": [
            "Inspect foundation and grout",
            "Check anchor bolts and mounting"
        ]
    },
    "Lubricant Contamination": {
        "symptoms": [
            "cloudy lubricant",
            "lubricant particles",
            "abnormal bearing wear"
        ],
        "checks": [
            "Inspect a lubricant sample",
            "Check lubricant filtration and ingress"
        ]
    },
    "Corrosion or Material Degradation": {
        "symptoms": [
            "visible corrosion",
            "surface pitting",
            "material cracking"
        ],
        "checks": [
            "Inspect the affected surface",
            "Assess material thickness and crack indications"
        ]
    }
}


CHECK_TARGETS = {
    "Check shaft alignment": "Shaft Misalignment",
    "Inspect coupling condition": "Shaft Misalignment",
    "Inspect bearing condition": "Bearing Damage",
    "Check vibration measurements": "Bearing Damage",
    "Measure vibration at different speeds": "Rotor Imbalance",
    "Inspect rotor balance": "Rotor Imbalance",
    "Check lubricant level and condition": "Inadequate Lubrication",
    "Inspect lubrication system": "Inadequate Lubrication",
    "Inspect mounting bolts": "Mechanical Looseness",
    "Check foundation and fasteners": "Mechanical Looseness",
    "Inspect cooling passages": "Cooling Problems",
    "Check fan operation and airflow": "Cooling Problems",
    "Inspect gear teeth": "Gear Tooth Damage",
    "Check gearbox lubricant for metal particles": "Gear Tooth Damage",
    "Inspect belt tension": "Belt Slippage",
    "Inspect belt wear and pulley alignment": "Belt Slippage",
    "Measure chain elongation": "Chain Wear",
    "Inspect chain links and sprockets": "Chain Wear",
    "Check pump suction pressure": "Pump Cavitation",
    "Inspect impeller for cavitation damage": "Pump Cavitation",
    "Inspect suction strainer and inlet": "Pump Blockage",
    "Check discharge line for blockage": "Pump Blockage",
    "Inspect mechanical seal": "Seal Failure",
    "Check seal flushing and operating conditions": "Seal Failure",
    "Measure current in each motor phase": "Motor Electrical Fault",
    "Inspect motor winding insulation": "Motor Electrical Fault",
    "Measure motor current under load": "Motor Overload",
    "Check driven equipment for excessive load": "Motor Overload",
    "Inspect fan blades or impeller": "Fan or Impeller Damage",
    "Measure airflow and check rotation": "Fan or Impeller Damage",
    "Inspect foundation and grout": "Foundation Failure",
    "Check anchor bolts and mounting": "Foundation Failure",
    "Inspect a lubricant sample": "Lubricant Contamination",
    "Check lubricant filtration and ingress": "Lubricant Contamination",
    "Inspect the affected surface": "Corrosion or Material Degradation",
    "Assess material thickness and crack indications": "Corrosion or Material Degradation"
}


ALL_SYMPTOMS = sorted({
    symptom
    for failure in FAILURES.values()
    for symptom in failure["symptoms"]
})


SYMPTOM_KEYWORDS = {
    "axial vibration": ["axial vibration", "vibrating along the shaft", "axial movement"],
    "coupling problems": ["coupling problem", "coupling issue", "coupling", "misaligned coupling"],
    "excessive vibration": ["excessive vibration", "too much vibration", "strong vibration", "vibrating excessively", "heavy vibration"],
    "abnormal noise": ["abnormal noise", "unusual noise", "strange noise", "loud noise", "grinding noise", "noise"],
    "high bearing temperature": ["high bearing temperature", "hot bearing", "bearing overheating"],
    "speed-dependent vibration": ["speed-dependent vibration", "vibration changes with speed", "vibrates at certain speeds"],
    "lubrication problems": ["lubrication problem", "lubrication issue", "poor lubrication", "low lubrication"],
    "loose mounting": ["loose mounting", "loose mount", "loose bolts", "loose mounting bolts"],
    "motor overheating": ["motor overheating", "motor is overheating", "motor gets hot", "motor too hot"],
    "restricted airflow": ["restricted airflow", "blocked airflow", "poor airflow", "airflow restriction"],
    "high operating temperature": ["high operating temperature", "running too hot", "high temperature", "overheating"],
    "gearbox noise": ["gearbox noise", "gear noise", "noisy gearbox", "gearbox is noisy"],
    "abnormal vibration": ["abnormal vibration", "unusual vibration"],
    "metal particles in lubricant": ["metal particles in lubricant", "metal in oil", "metal particles in oil", "metal flakes in lubricant"],
    "belt squealing": ["belt squealing", "squealing belt", "belt squeaks", "belt squeal"],
    "reduced driven speed": ["reduced driven speed", "driven speed is low", "output speed dropped", "speed has dropped"],
    "belt overheating": ["belt overheating", "hot belt", "belt is hot"],
    "chain noise": ["chain noise", "noisy chain", "chain is noisy"],
    "chain elongation": ["chain elongation", "stretched chain", "elongated chain"],
    "irregular chain movement": ["irregular chain movement", "chain jumps", "jerky chain movement"],
    "crackling pump noise": ["crackling pump noise", "pump crackling", "gravel sound in pump", "sounds like gravel", "crackling noise"],
    "fluctuating flow": ["fluctuating flow", "flow fluctuates", "flow is unstable", "inconsistent flow"],
    "pump vibration": ["pump vibration", "pump is vibrating", "pump vibrates"],
    "low flow rate": ["low flow rate", "low flow", "reduced flow", "less water", "flow rate has dropped", "delivering less water", "reduced water delivery"],
    "high discharge pressure": ["high discharge pressure", "discharge pressure is high"],
    "reduced pump output": ["reduced pump output", "pump output is low", "pump output dropped"],
    "fluid leakage": ["fluid leakage", "fluid leak", "leaking fluid", "oil leak", "water leak", "leakage"],
    "pressure loss": ["pressure loss", "pressure dropped", "loss of pressure", "low pressure"],
    "seal overheating": ["seal overheating", "hot seal", "mechanical seal is hot"],
    "unbalanced motor current": ["unbalanced motor current", "current imbalance", "unequal phase current"],
    "motor electrical noise": ["motor electrical noise", "electrical humming", "electrical buzzing"],
    "high motor current": ["high motor current", "motor draws high current", "overcurrent"],
    "reduced motor speed": ["reduced motor speed", "motor speed dropped", "motor running slowly"],
    "reduced airflow": ["reduced airflow", "low airflow", "fan airflow is low"],
    "fan vibration": ["fan vibration", "fan is vibrating", "fan vibrates"],
    "abnormal fan noise": ["abnormal fan noise", "fan noise", "noisy fan"],
    "foundation cracks": ["foundation cracks", "cracked foundation", "cracks in foundation"],
    "loose anchor bolts": ["loose anchor bolts", "anchor bolts are loose"],
    "structural vibration": ["structural vibration", "structure vibrates", "vibration in the frame"],
    "cloudy lubricant": ["cloudy lubricant", "milky oil", "cloudy oil"],
    "lubricant particles": ["lubricant particles", "particles in lubricant", "debris in oil"],
    "abnormal bearing wear": ["abnormal bearing wear", "bearing wear"],
    "visible corrosion": ["visible corrosion", "rust", "corrosion"],
    "surface pitting": ["surface pitting", "pitting on the surface", "pitted surface"],
    "material cracking": ["material cracking", "crack in the material", "cracked component", "material crack"],
}


def extract_symptoms_from_text(text):
    """Return known symptom labels suggested by a free-text description."""
    lowered = text.lower()
    found = []
    for symptom in ALL_SYMPTOMS:
        phrases = SYMPTOM_KEYWORDS.get(symptom, [symptom])
        if any(phrase in lowered for phrase in phrases):
            found.append(symptom)
    return found


def window_features(values, window_size=2048):
    """Calculate comparable time-domain features on non-overlapping windows."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size < 16:
        return pd.DataFrame()
    # Keep windows large enough for stable descriptive statistics; use the
    # entire signal as one window for shorter recordings.
    size = min(window_size, max(128, values.size // 2)) if values.size < window_size else window_size
    chunks = [values[i:i + size] for i in range(0, values.size, size) if len(values[i:i + size]) >= min(128, size)]
    rows = []
    for chunk in chunks:
        rms = float(np.sqrt(np.mean(np.square(chunk))))
        mean_abs = float(np.mean(np.abs(chunk)))
        rows.append({
            'RMS': rms,
            'Standard deviation': float(np.std(chunk)),
            'Peak absolute amplitude': float(np.max(np.abs(chunk))),
            'Crest factor': float(np.max(np.abs(chunk)) / rms) if rms > 1e-12 else 0.0,
            'Mean': float(np.mean(chunk)),
        })
    return pd.DataFrame(rows)


def build_baseline(channels):
    """Build empirical reference statistics from user-supplied healthy data."""
    output = {}
    for channel, values in channels.items():
        feats = window_features(values)
        if not feats.empty:
            output[channel] = {
                name: {'mean': float(feats[name].mean()),
                       'std': float(feats[name].std(ddof=0)),
                       'lower': float(feats[name].quantile(0.01)),
                       'upper': float(feats[name].quantile(0.99))}
                for name in feats.columns
            }
    return output


def assess_against_baseline(test_channels, baseline):
    """Compare test feature windows to empirical healthy 1st–99th percentiles."""
    rows = []
    for channel, values in test_channels.items():
        if channel not in baseline:
            continue
        feats = window_features(values)
        if feats.empty:
            continue
        for feature in feats.columns:
            if feature not in baseline[channel]:
                continue
            ref = baseline[channel][feature]
            test_median = float(feats[feature].median())
            # Use the healthy-data 1st/99th percentiles; these are empirical
            # dataset thresholds, not universal machine safety limits.
            abnormal = test_median < ref['lower'] or test_median > ref['upper']
            rows.append({
                'Channel': channel,
                'Feature': feature,
                'Healthy reference mean': ref['mean'],
                'Healthy 1st percentile': ref['lower'],
                'Healthy 99th percentile': ref['upper'],
                'Test median': test_median,
                'Assessment': 'Outside healthy reference' if abnormal else 'Within healthy reference',
                'Test windows': int(len(feats)),
            })
    return pd.DataFrame(rows)


def symptoms_from_sensor_assessment(assessment):
    """Conservatively translate vibration-feature deviations into symptoms.

    This does not classify a specific bearing fault. It only adds generic
    vibration symptoms when amplitude/dispersion features are outside baseline.
    """
    if assessment is None or assessment.empty:
        return [], []
    outside = assessment[assessment["Assessment"] == "Outside healthy reference"]
    if outside.empty:
        return [], []
    abnormal_features = set(outside["Feature"].astype(str))
    symptoms = []
    evidence = []
    amplitude_features = {"RMS", "Standard deviation", "Peak absolute amplitude"}
    if abnormal_features & amplitude_features:
        symptoms.append("excessive vibration")
        evidence.append("Recorded vibration amplitude/dispersion differs from the healthy reference.")
    if "Crest factor" in abnormal_features:
        evidence.append("Recorded vibration crest factor differs from the healthy reference; impulsive behaviour may warrant investigation. This alone is not mapped to a specific fault symptom.")
    if "Mean" in abnormal_features:
        evidence.append("Signal mean differs from the healthy reference; check sensor offset and preprocessing before interpreting it as a fault.")
    return sorted(set(symptoms)), evidence


def rank_failures(symptoms, inspection_results):
    results = []

    for name, details in FAILURES.items():
        known = set(details["symptoms"])
        matches = set(symptoms) & known

        # Each matching symptom contributes evidence.
        # These are heuristic weights, not probabilities.
        score = sum(
            2 for symptom in matches
        )

        reasons = []

        if matches:
            reasons.append(
                "Matching symptoms: " + ", ".join(sorted(matches))
            )

        # Inspection evidence is interpreted separately.
        for check, outcome in inspection_results.items():
            if CHECK_TARGETS.get(check) != name:
                continue

            if outcome == "Finding observed":
                score += 3
                reasons.append(
                    f"Supporting evidence: {check}"
                )

            elif outcome == "Finding not observed":
                score -= 3
                reasons.append(
                    f"Expected finding not observed: {check}"
                )

            else:
                reasons.append(
                    f"Inconclusive inspection: {check}"
                )

        results.append({
            "failure": name,
            "score": max(0, score),
            "matches": sorted(matches),
            "checks": details["checks"],
            "reasons": reasons
        })

    # Higher evidence scores appear first.
    results.sort(
        key=lambda item: (
            item["score"],
            len(item["matches"])
        ),
        reverse=True
    )

    return results


def select_next_check(ranked, inspection_results):
    # Prefer an uncompleted check for the highest-ranked
    # candidate. If none remain, consider other candidates.
    for candidate in ranked:
        # Do not recommend checks for candidates with no supporting evidence.
        if candidate["score"] <= 0:
            continue
        for check in candidate["checks"]:
            if check not in inspection_results:
                return check

    return None
