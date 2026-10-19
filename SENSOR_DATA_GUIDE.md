# Built-in sensor dataset for Failure Detective AI

## Run the analysis

1. Open **Real bearing data — ready to analyse** in the app.
2. Click **Load built-in dataset and analyse**. No file upload is needed.
3. The app fetches a healthy CWRU recording (`97_Normal_0.mat`) and an inner-race fault recording (`105_0.mat`) from the public dataset mirror.
4. It extracts the drive-end vibration signal, computes RMS, standard deviation, peak amplitude, crest factor, and mean, and compares the faulty recording with the healthy reference range.
5. Review the feature table and download the CSV report.

## Dataset provenance

- Official source/project: https://engineering.case.edu/bearingdatacenter/download-data-file
- Public mirror used by the app: https://github.com/s-whynot/CWRU-dataset
- Preconfigured recordings: `Normal/97_Normal_0.mat` and `12k_Drive_End_Bearing_Fault_Data/IR/007/105_0.mat`
- Sampling: 12 kHz drive-end vibration; the pair is from the 0 HP operating condition.

The app retrieves the files automatically on first use and caches them for 24 hours. Internet access is required for the initial fetch. These are real laboratory measurements, not live readings from the user's machine. The statistical baseline is an anomaly screen, not a trained universal classifier or proof of a particular fault.

## What to say in your presentation

"The application includes a preconfigured real sensor-data workflow using publicly available CWRU bearing recordings. It compares a healthy bearing reference with a known inner-race fault recording. The system extracts time-domain features and flags deviations without requiring the user to upload data. The recordings are laboratory data, so results should not be treated as universal machine limits."
