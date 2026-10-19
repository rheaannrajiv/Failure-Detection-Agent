# Sensor dataset workflow for Failure Detective AI

## Recommended first test

Use the Case Western Reserve University (CWRU) Bearing Data Center. Download one healthy/normal recording and one faulty recording from the same operating condition. Upload both `.mat` files in the app's **Healthy baseline vs. test recording** panel. Use the same channel (normally drive-end `DE_time`) in both files.

Official dataset page: https://engineering.case.edu/bearingdatacenter/download-data-file

The CWRU page states that the recordings include normal bearings and single-point bearing defects; the data include drive-end/fan-end/base vibration signals and motor speed. It is laboratory data from a specific test motor, not universal limits for industrial equipment.

## Alternative

Paderborn University provides vibration and motor-current signals from healthy and damaged bearings. Its dataset is larger and has licence/citation conditions; check these before using it in a report:
https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter/data-sets-and-download

## What to demonstrate

1. Upload a healthy recording as the reference.
2. Upload a recording to assess.
3. Explain that the app calculates RMS, standard deviation, peak absolute amplitude, crest factor, and mean in signal windows.
4. Show which test features fall outside the empirical 1st–99th percentile range from the healthy recording.
5. Explain that this is anomaly screening. A deviation is evidence to investigate, not a confirmed diagnosis.

## Data quality checklist

- Same dataset and sensor location for both recordings.
- Same or comparable machine speed/load/operating condition.
- Use the same MATLAB variable/channel name where possible; known CWRU DE/FE/BA names are normalized by the app.
- Cite the dataset source in your presentation/report.
- Do not describe public laboratory data as live readings from your own hardware.
