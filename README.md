# Failure Detective AI

A Streamlit-based mechanical fault troubleshooting prototype combining a transparent rule-based knowledge base, a Groq-hosted chat assistant, inspection tracking, and recorded sensor-data anomaly screening.

## Features

- 18 mechanical fault categories, symptom matching, heuristic evidence scores, and recommended inspections.
- Groq-hosted AI chat. The API key is read from Streamlit Secrets, not stored in source code.
- Manual/simulated sensor inputs for demonstrations, explicitly labelled as simulated.
- **Recorded sensor dataset analysis:** upload a healthy reference and a test recording as CSV or MATLAB `.mat`. The app calculates time-domain features (RMS, standard deviation, peak amplitude, crest factor, mean) and compares test medians with the 1st–99th percentile range observed in the healthy recording.
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

## Using real recorded sensor data

1. Open **Healthy baseline vs. test recording** in the app.
2. Upload a healthy/normal recording and a test recording from the same sensor location and operating condition.
3. Supported formats:
   - **CSV/TXT:** numeric sensor channels should be in columns, with at least 128 numeric samples per channel.
   - **MATLAB `.mat`:** numeric arrays of at least 128 samples are extracted. Common CWRU variables ending in `DE_time`, `FE_time`, and `BA_time` are normalized to comparable channel names.
4. Select **Build baseline and analyse recording**.
5. Review the feature table and download the CSV report.

### Public datasets

- Case Western Reserve University Bearing Data Center: https://engineering.case.edu/bearingdatacenter/download-data-file
  - Provides actual laboratory vibration recordings for normal and faulty bearings, typically in MATLAB format.
- Paderborn University Bearing Data Center: https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter/data-sets-and-download
  - Provides vibration and motor-current data for healthy and damaged bearing states. Check the dataset's licence and citation requirements before reuse.

For a meaningful comparison, choose healthy and test recordings from the **same dataset, sensor position/channel, sampling setup, and operating condition**. Do not compare unrelated channels or machines. CWRU's recordings are laboratory bearing-test signals; they are not general-purpose temperature/current baselines for all machines.

## How the baseline works

The app divides each uploaded signal into windows and computes time-domain features. It builds the healthy reference range from the uploaded healthy recording's 1st and 99th percentiles, then checks whether the test recording's median feature falls outside that range. The reference is empirical and specific to the uploaded data.

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
- The uploaded-data module detects statistical deviations in recorded signals; it does not automatically prove which failure caused them.
- The manual sensor panel is simulated/manual input. It is not a live hardware connection.
- Do not use the output as the sole basis for safety-critical maintenance decisions. Follow site safety procedures and consult qualified personnel.

## Project structure

- `app.py` — Streamlit application and diagnostic logic.
- `requirements.txt` — Python dependencies.
- `README.md` — setup, dataset workflow, deployment, and limitations.
