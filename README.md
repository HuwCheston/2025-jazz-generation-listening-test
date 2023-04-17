# Analyzing the success of networked musical performances

Experiment code for small-scale perceptual study of the factors that contribute to a successful musical performance 
over a network. The video data used in this study comes from our corpus of networked performances by professional
jazz duos (keyboard and drums); see the DOI. 

Participants are shown a randomised sequence of performances from the corpus and asked simply to rate how successful 
they are, on a linear scale of 1 to 9 (with 1 = extremely unsuccessful, 9 = extremely successful). 

---

## Install

1. Clone this repository into a new directory:
```
git clone https://github.com/HuwCheston/2023-duo-success-analysis
```
2. Download the complete set of video files (perceptual_study_videos.rar) from one of the following locations:
    - [Google Drive](https://drive.google.com/file/d/1KV1gEgpNmrv68Q7ynlQvCDOBY_DcBAep/view?usp=sharing)
    - Zenodo (forthcoming, when paper is published)
3. Extract the .mp4 files (there should be 130) inside perceptual_study_videos.rar into `./assets/videos` .
   You may need to install a tool to open RAR files: options include
   [WinRAR](https://www.win-rar.com/start.html?&L=0) for Windows,  
   [Unar](https://theunarchiver.com/command-line) for Ubuntu,
   and Unarchiver for Mac.

4. Follow the instructions inside docs/INSTALL.md to build and run as with any other PsyNet experiment.

---

This experiment is implemented using the [PsyNet framework](https://www.psynet.dev/).

For installation instructions, see docs/INSTALL.md.

For a list of run commands, see docs/RUN.md.

For more information about PsyNet, see the [documentation website](https://psynetdev.gitlab.io/PsyNet/).
