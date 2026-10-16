# Failure Detective AI

**An AI-assisted mechanical fault diagnosis agent built with Python and Streamlit.**

Failure Detective AI is an interactive web application that helps users investigate possible mechanical faults from symptom descriptions, simulated or manually entered machine readings, and recorded inspection findings. It combines a transparent rule-based diagnostic engine with a hosted conversational AI assistant.

**Live application:** https://failure-detection-agent-9s8mqmdpmcvakjtfbqzky.streamlit.app  
**Repository:** https://github.com/rheaannrajiv/Failure-Detection-Agent

---

## Features

- **Conversational troubleshooting:** Describe equipment behaviour, unusual sounds, overheating, vibration, or performance changes in natural language.
- **Rule-based fault ranking:** Compare detected symptoms and inspection outcomes against a predefined mechanical-fault knowledge base.
- **18 fault categories:** Shaft misalignment, bearing damage, rotor imbalance, lubrication and cooling problems, gear damage, belt slippage, chain wear, pump cavitation or blockage, seal failure, motor electrical faults or overload, fan/impeller damage, foundation failure, lubricant contamination, and corrosion/material degradation.
- **Inspection guidance:** Suggests follow-up checks based on the current ranked candidates.
- **Iterative reassessment:** Record whether an inspection finding was observed, not observed, or inconclusive, then update the evidence ranking.
- **Simulated sensor input:** Enter illustrative vibration, temperature, and motor-current readings to demonstrate a device-data classification workflow without physical sensors.
- **Diagnostic report export:** Review inspection history and download a text report.
- **Browser-based access:** Deployed through Streamlit Community Cloud; users do not need to install the application locally to use the hosted version.

## How it works

```text
User describes symptoms or enters readings
                    |
                    v
        Streamlit application interface
                    |
          +---------+----------+
          |                    |
          v                    v
 Natural-language        Simulated sensor
 symptom matching        threshold evaluation
          |                    |
          +---------+----------+
                    |
                    v
        Rule-based diagnostic engine
                    |
                    v
    Rank candidate faults using evidence
                    |
          +---------+----------+
          |                    |
          v                    v
 Hosted AI explanation   Recommended inspection
          |                    |
          +---------+----------+
                    |
                    v
       Record findings and reassess
                    |
                    v
          Downloadable report
```

The hosted AI provides conversational explanations and troubleshooting guidance. The rule-based engine calculates the diagnostic evidence scores and ranks candidates; the AI does not independently change those scores.

## Knowledge base and scoring

The diagnostic knowledge base is defined directly in `app.py`, rather than retrieved from an external database.

- `FAILURES` defines each fault category, its associated symptoms, and inspection checks.
- `SYMPTOM_KEYWORDS` maps common phrases to the symptom labels used by the rule engine.
- `CHECK_TARGETS` associates inspection checks with fault categories.
- `rank_failures()` calculates heuristic evidence scores and sorts the candidates.

Scores are **heuristic rankings, not probabilities**. The app does not automatically learn from previous conversations or persistently add new fault categories.

## Technology stack

- **Python** — application and diagnostic logic
- **Streamlit** — interactive web interface
- **Groq API** — hosted conversational AI
- **Streamlit Community Cloud** — application hosting
- **GitHub** — source-code repository and version control

## Run locally

1. Install Python 3.10 or later.
2. Clone the repository:

   ```bash
   git clone https://github.com/rheaannrajiv/Failure-Detection-Agent.git
   cd Failure-Detection-Agent
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the hosted AI API key as described below.
5. Start the application:

   ```bash
   streamlit run app.py
   ```

## Configure the hosted AI

Create an API key in the [Groq Console](https://console.groq.com/keys). For local use, create `.streamlit/secrets.toml` with:

```toml
GROQ_API_KEY = "your_actual_api_key"
```

If your version of the app supports a `GROQ_MODEL` setting, set it only to a model currently available to your Groq account, for example:

```toml
GROQ_MODEL = "openai/gpt-oss-20b"
```

The application must use a model identifier supported by the provider at the time of use. Availability and free-tier limits can change.

**Security:** Never commit API keys or `secrets.toml` to GitHub. For Streamlit Community Cloud, add the same secret through the app's **Settings → Secrets** page. Keep credentials out of source code and screenshots.

## Simulated sensor data

The sensor feature is intended for software demonstration. Readings may be entered manually or generated for test scenarios and are evaluated using configured illustrative thresholds.

- No physical sensors are required for the demonstration.
- The readings are not real-time measurements from connected equipment.
- Thresholds are illustrative and are not universal machine safety limits.
- Classification results should be verified before being used for any real maintenance decision.

## Example demonstration scenarios

1. **Motor overheating:** high temperature with restricted airflow.
2. **Vibration and bearing symptoms:** excessive vibration, abnormal noise, and elevated bearing temperature.
3. **Pump flow problem:** low flow rate with high discharge pressure.

Use the sensor panel and chat independently, then record an inspection outcome to demonstrate how the rule-based ranking changes.

## Project structure

```text
Failure-Detection-Agent/
├── app.py
├── requirements.txt
├── README.md
├── DEVELOPMENT_SCHEMA.md
└── DEVELOPMENT_SCHEMA_UPDATED.pdf   # optional project documentation
```

The exact files in the repository may vary depending on which documentation versions you upload.

## Limitations and safety

- This is an educational decision-support prototype, not a certified industrial diagnostic system.
- The knowledge base is predefined and only covers the faults and symptoms encoded in the application.
- Natural-language symptom detection relies on keyword mapping and may miss alternative wording.
- Heuristic scores are not calibrated probabilities and do not prove a fault exists.
- Simulated sensor readings do not establish the condition of real equipment.
- Hosted AI requires internet connectivity, a valid API key, and an available model/API quota.
- Follow site safety procedures and consult qualified personnel before inspecting rotating, electrical, hot, or pressurized machinery.

## Future improvements

- Connect real sensor hardware and validated data-acquisition interfaces.
- Expand the knowledge base using verified maintenance records and technical references.
- Validate and tune classification thresholds against labelled machine data.
- Add persistent storage for inspection histories, with appropriate access controls.
- Evaluate diagnostic performance using a documented test dataset.

## License

No license is specified here. Add a `LICENSE` file if you intend to publish the project under a particular open-source license.
