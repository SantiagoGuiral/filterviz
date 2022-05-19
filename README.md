# filterviz

Filterviz is a Python application built with Tkinter that allows the user to import an audio file and presents a variety of digital filters with the objective to apply them and analyze their effects in the audio.

The program was developed as the final project for the digital signal processing course from the university of Antioquia.

Authors:

Santiago Ríos Guiral(@SantiagoGuiral)

Emmanuel Gomez Ospina(@Ego2509)

University of Antioquia.

Electronic and Telecommunications department.

Medellin, Colombia.


## Install Python dependencies

The application requires the following dependencies.

```sh
pip install numpy
pip install matplotlib
pip install scipy
pip install pygame
pip install sounddevice
pip install SoundFile
```

## Execute filterviz

To execute the application use the following command

```sh
python filterbank.py
```
## Features

- Apply different digital filters to audio recordings
- Remove noise from unwanted frequencies
- Contains FIR, IIR and ideal filters.

## Filterviz usage

1. Start the application with the corresponding command.
2. In the audio input section, the user can record an audio and generate an audio file. Also, it's possible to listen the previous recording.
3. Fill the form in the input design section that allows the user to choose a digital filter with its corresponding design parameters.
4. Apply the filter to the audio with the calculate button. 
5. Observe the filter effect to the audio with help of the generated graphs corresponding to the audio signal, filter's magnitude and phase, filtered audio signal and the fast Fourier transform for the output audio.
6. Export the filtered audio with the export button.
7. Listen to the filtered audio.
