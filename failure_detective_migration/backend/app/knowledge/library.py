"""Curated mechanical engineering reference notes for retrieval by the agent.
These are general diagnostic prompts, not machine-specific limits or standards."""
from __future__ import annotations

KNOWLEDGE = {
    "gear wear": {
        "aliases": ["gear tooth damage", "gear pitting", "gear backlash"],
        "mechanism": "Repeated tooth contact can cause pitting, scuffing, wear, root cracking or tooth breakage when load, lubrication, alignment or material conditions are unsuitable.",
        "indicators": ["gear-mesh frequency components and sidebands", "cyclic noise that changes with load", "backlash change", "debris in lubricant"],
        "checks": ["identify gear tooth counts and shaft speeds before interpreting gear-mesh frequencies", "inspect lubricant and magnetic/debris filters", "measure backlash and inspect tooth contact pattern under an approved procedure"],
        "cautions": "Gear-mesh vibration is affected by load, tooth geometry and transmission path; it is not a standalone proof of tooth damage.",
    },
    "belt drive problems": {
        "aliases": ["belt slip", "belt tension", "pulley misalignment"],
        "mechanism": "Incorrect tension, wear, contamination or pulley misalignment changes belt traction and dynamic loading.",
        "indicators": ["slip or squeal", "speed variation", "belt dust", "temperature rise", "transverse vibration"],
        "checks": ["inspect belt condition and pulley grooves after isolation", "measure tension using the belt or OEM procedure", "check pulley alignment and driven speed"],
        "cautions": "Do not approach or measure a moving belt unless an approved guarded measurement method is provided.",
    },
    "seal failure": {
        "aliases": ["mechanical seal leakage", "shaft seal wear"],
        "mechanism": "Seal faces, elastomers or auxiliary systems fail due to wear, dry running, misalignment, thermal distortion or incompatible process conditions.",
        "indicators": ["visible leakage", "seal temperature increase", "flush or barrier-fluid abnormalities", "repeat seal failure"],
        "checks": ["identify seal arrangement and OEM leakage limits", "review flush, quench or barrier-fluid conditions", "inspect shaft runout, alignment and seal faces after isolation"],
        "cautions": "Process fluid may be hot, toxic, corrosive or pressurised; follow site isolation and containment procedures.",
    },
    "compressor surge": {
        "aliases": ["compressor instability", "surging compressor", "flow oscillation"],
        "mechanism": "A compressor operating outside its stable flow range can experience oscillatory flow and pressure, potentially causing severe aerodynamic and mechanical loading.",
        "indicators": ["rapid pressure and flow oscillations", "repeated rumbling or banging", "temperature fluctuation", "control valve cycling"],
        "checks": ["review compressor map and operating point with qualified personnel", "trend suction/discharge pressure and flow", "inspect anti-surge control and instrumentation"],
        "cautions": "Surge can damage equipment rapidly. Follow OEM/site procedures; do not adjust protection settings as an experiment.",
    },
    "thermal expansion constraint": {
        "aliases": ["thermal growth", "hot alignment", "pipe strain"],
        "mechanism": "Temperature-driven dimensional growth constrained by supports, piping or foundations can introduce loads and misalignment.",
        "indicators": ["alignment changes between cold and hot states", "bearing or seal distress after warm-up", "support movement"],
        "checks": ["compare cold and operating alignment where specified", "review support, anchor and piping loads", "trend temperatures and displacement"],
        "cautions": "Thermal movement must be evaluated against OEM design allowances and safe operating procedures.",
    },
    "fatigue cracking": {
        "aliases": ["cyclic fatigue", "crack propagation", "high cycle fatigue"],
        "mechanism": "Repeated cyclic stress can initiate and propagate cracks, often below static yield strength, depending on stress concentration, material and environment.",
        "indicators": ["crack at stress concentration", "progressive vibration or deflection", "fracture surface beach marks when visible after failure"],
        "checks": ["remove component from service when a safety-critical crack is suspected", "use an appropriate qualified NDT method", "review load cycles, stress raisers, material and manufacturing history"],
        "cautions": "Do not continue operating safety-critical cracked components; fracture assessment requires qualified engineering review.",
    },
    "corrosion damage": {
        "aliases": ["corrosion", "erosion corrosion", "pitting corrosion"],
        "mechanism": "Chemical or electrochemical reactions degrade material; flow-assisted erosion or galvanic coupling may accelerate local loss.",
        "indicators": ["wall-thickness loss", "pitting", "leakage", "rust products or deposits"],
        "checks": ["identify process chemistry and material compatibility", "measure thickness using qualified inspection", "inspect coating, galvanic couples and flow conditions"],
        "cautions": "Do not infer remaining life from visual appearance alone; use a qualified inspection and applicable engineering code.",
    },
    "motor electrical fault": {
        "aliases": ["motor winding fault", "electrical imbalance", "broken rotor bar"],
        "mechanism": "Supply imbalance, winding insulation damage, rotor defects or connection faults create abnormal electrical and electromagnetic forces and heating.",
        "indicators": ["phase-current imbalance", "abnormal temperature", "electrical frequency sidebands", "reduced torque or abnormal noise"],
        "checks": ["trend phase currents and voltages using qualified electrical personnel", "review insulation test results and protection trips", "compare vibration with electrical and mechanical operating data"],
        "cautions": "Electrical tests and panel access must be performed by authorised personnel using appropriate isolation and PPE.",
    },
    "hydraulic restriction": {
        "aliases": ["blocked strainer", "blocked suction line", "flow restriction"],
        "mechanism": "A restriction increases system resistance and can reduce available flow or suction pressure, potentially causing cavitation in pumps.",
        "indicators": ["reduced flow", "abnormal differential pressure", "low suction pressure", "filter or strainer loading"],
        "checks": ["compare differential pressure across filters and strainers", "inspect valves and lines after safe isolation", "verify liquid level and operating point"],
        "cautions": "Depressurise and isolate the system before opening strainers, lines or pressure boundaries.",
    },
    "structural resonance": {
        "aliases": ["resonance", "natural frequency", "structural vibration"],
        "mechanism": "Excitation near a structural natural frequency amplifies vibration response; supports and boundary conditions influence modal behaviour.",
        "indicators": ["large amplitude near a narrow speed range", "strong phase change through resonance", "vibration sensitive to support or load changes"],
        "checks": ["compare excitation frequencies with measured or calculated natural frequencies", "review run-up/coast-down trends where safe and approved", "inspect foundations and support stiffness"],
        "cautions": "Do not perform speed sweeps on critical machinery without an approved test plan and protection limits.",
    },
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
