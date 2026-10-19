# Failure Detective AI

A Streamlit-based mechanical fault troubleshooting prototype combining a transparent rule-based knowledge base, a Groq-hosted chat assistant, inspection tracking, and recorded sensor-data anomaly screening.

## Features

- 18 mechanical fault categories, symptom matching, heuristic evidence scores, and recommended inspections.
- Groq-hosted AI chat. The API key is read from Streamlit Secrets, not stored in source code.
- Manual/simulated sensor inputs for demonstrations, explicitly labelled as simulated.
- **Built-in recorded sensor dataset:** no upload is needed. The app automatically fetches a preconfigured pair of public CWRU MATLAB recordings (healthy bearing and inner-race fault) on first analysis, then caches them for 24 hours. It calculates RMS, standard deviation, peak amplitude, crest factor, and mean, then compares the fault recording against the healthy reference range.
- Downloadable sensor-assessment CSV and diagnostic report.
- Public web access through a public Streamlit deployment; visitors generally do not need a Streamlit account to use a public app.

## Run locally

1. Install Python 3.10 or newer.
2. Download `app.py`, `requirements.txt`, and this README into the same folder.
3. Open a terminal in that folder and run:

   ```bash
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```

4. To enable the hosted chatbot locally, create `.streamlit/secrets.toml`:

   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   GROQ_MODEL = "openai/gpt-oss-20b"
   ```

   Never commit the API key or `secrets.toml` to GitHub. On Streamlit Community Cloud, add these values in the app's Settings → Secrets.

## Using the built-in real recorded dataset

1. Open **Real bearing data — ready to analyse**.
2. Select **Load built-in dataset and analyse**. No upload or manual download is required.
3. The app fetches two preconfigured CWRU samples from a public GitHub dataset mirror: `97_Normal_0.mat` (healthy, 0 HP) and `105_0.mat` (inner-race fault, 0 HP). Both use drive-end vibration (`DE_time`) at 12 kHz.
4. The app derives healthy reference statistics and displays which features of the faulty recording fall outside the healthy range. You can download the results as a CSV.

The first analysis needs an internet connection to retrieve the public recordings. Streamlit caches the recordings for 24 hours, so repeat analysis generally does not need to download them again during that cache period. If the data source is temporarily unavailable, the app will show an error and can be retried later.

### Dataset source

- Official Case Western Reserve University Bearing Data Center: https://engineering.case.edu/bearingdatacenter/download-data-file
- Public dataset mirror containing the preconfigured files: https://github.com/s-whynot/CWRU-dataset

The recordings are real laboratory vibration measurements with seeded bearing faults. They are not live readings from your own machine, and they do not provide universal temperature or motor-current thresholds.

## How the baseline works

The app divides each recorded signal into windows and computes time-domain features. It builds the healthy reference range from the built-in healthy recording's 1st and 99th percentiles, then checks whether the test recording's median feature falls outside that range. The reference is empirical and specific to the uploaded data.

This is a **statistical anomaly screen**, not a trained classifier and not proof of a mechanical fault. A single healthy file may not represent all speeds, loads, machine types, or normal variation. Use multiple healthy recordings across relevant operating conditions for stronger results. Sensor units are not inferred reliably from every public file, so the feature values are compared in the original signal scale.

## Public deployment

The app can be hosted publicly on Streamlit Community Cloud. Viewers normally do not need to create or sign in to a Streamlit account when the app is public. To deploy:

1. Push `app.py`, `requirements.txt`, and `README.md` to the GitHub repository.
2. In Streamlit Community Cloud, deploy or reboot the app from that repository.
3. Add `GROQ_API_KEY` and, optionally, `GROQ_MODEL` under the app's Secrets settings.
4. Test the public URL in a private/incognito browser window. If the deployment is configured as private, change its sharing/visibility settings.

The host still requires an owner account to manage deployment. Public visitors should not need that account.

## Limitations and safety

- This is a student decision-support prototype, not a certified condition-monitoring system.
- The current knowledge-base scores are heuristic evidence scores, not probabilities.
- The built-in recorded-data module detects statistical deviations in recorded signals; it does not automatically prove which failure caused them.
- The manual sensor panel is simulated/manual input. It is not a live hardware connection.
- Do not use the output as the sole basis for safety-critical maintenance decisions. Follow site safety procedures and consult qualified personnel.

## Project structure

- `app.py` — Streamlit application and diagnostic logic.
- `requirements.txt` — Python dependencies.
- `README.md` — setup, dataset workflow, deployment, and limitations.
