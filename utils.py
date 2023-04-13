import librosa
import numpy as np
import smtplib


senderEmail = "mayaNbridgman@gmail.com"
receiverEmail = ""
password = "lboesehsgspqsxny"
SUBJECT = ""
TEXT = ""
msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
server = smtplib.SMTP("smtp.gmail.com", 587)

def calculateValues(x, fs):
    n_fft = 2048
    hop_length = 1024

    #zero crossing rate
    zcrs = librosa.feature.zero_crossing_rate(x).mean()
    #central spectroid
    cent = librosa.feature.spectral_centroid(y=x, sr=fs).mean()
    #mel scale converted freq
    mel = 2595.0 * np.log10(1.0 + fs / 700.0)

    #loudness in rms
    # Compute the spectrogram (magnitude)
    # Compute the spectrogram (magnitude) and convert the spectrogram into dB
    spec_db = librosa.amplitude_to_db(abs(librosa.stft(x, n_fft=n_fft, hop_length=hop_length)))
    # Compute A-weighting values
    a_weights = librosa.A_weighting(librosa.fft_frequencies(sr=fs, n_fft=n_fft))
    a_weights = np.expand_dims(a_weights, axis=1)
    # Apply the A-weghting to the spectrogram in dB
    spec_dba = spec_db + a_weights
    # Compute the "loudness" value
    loudness = librosa.feature.rms(S=librosa.db_to_amplitude(spec_dba)).mean()
    return zcrs, cent, mel, loudness

def roundValues(zcrs, cent, mel, loudness):
    values = [zcrs, cent, mel, loudness]
    for i in range(len(values)):
        values[i] = round(values[i],2)

    print(values)
    return values[0], values[1], values[2], values[3]

def sendEmail(totalAudio, threshold_total, zcrs, cent, threshold_mel, threshold_loudness, threshold_zcrs, threshold_cent, teacherEmail, studentName):
    server.starttls()
    server.login(senderEmail, password)

    SUBJECT = "Attend to child"
    if totalAudio > threshold_total:
        exceed = "exceeded"
    else:
        exceed = "did not exceed"

    TEXT = f"""The classroom noise level of {round(totalAudio,2)} {exceed} {studentName[0]}'s threshold of {round(threshold_total,2)}, 
    please check on them\n\nRecorded audio values:\nSmoothness (Zero-Crossing Rate): {round(zcrs,2)}\nBrightness (Spectral Centroid): {round(cent,2)}
    \nFrequency (Mel Spectogram): {round(threshold_mel,2)}\nLoudness (Root Mean Squared): {round(threshold_loudness,2)}\n\nThreshold values:
    \nSmoothness (Zero-Crossing Rate): {round(threshold_zcrs,2)}\nBrightness (Spectral Centroid): {round(threshold_cent,2)}
    \nFrequency (Mel Spectogram): {round(threshold_mel,2)}\nLoudness (Root Mean Squared): {round(threshold_loudness,2)}"""

    msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server.sendmail(senderEmail, teacherEmail, msg)
    server.quit()