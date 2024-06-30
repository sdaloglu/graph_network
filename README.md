# [Re] Discovering Symbolic Models from Deep Learning with Inductive Biases

## Description

This project contains the code for the reproduction of the paper "Discovering Symbolic Models from Deep Learning with Inductive Biases" by Cranmer et al. (2020). The code is implemented in Python and uses the PyTorch Geometric library for the implementation of message passing Graph Network architecture, and the PySR library for symbolic regression. The main goal of this reproduction work is to demonstrate the intersection of symbolic regression and deep learning to extract the physical intuition behind black-box models. In the pursuit of this, both explicit (architecture bottlenecks) and implicit (regularization) inductive biases were used to create sparse latent representations of the messages to which symbolic regression was applied to. The pairwise forces between particles in various classical mechanical systems were found to be correponding to the learned message vectors, and the correct force laws were able to be recovered succesfully for L1 regularization and Bottleneck models.



## Installation
The first step is to login to CSD3, and clone the remote GitLab repository on your account. Then, the conda environment provided in the environment.yaml file can be created by the running the following command at the root directory:


```bash
conda env create -f environment.yaml
```

To activate the conda environment, the following command should be run:

```bash
conda activate project
```

## Data Generation

The data for the systems under study are generated by a simulation script adopted from the original paper located in `src/simulate_systems.py`. To generate all the systems used in this study: charge, spring, r1 and r2, the automated run script located in `src/automated_runs/automate_sims.py` can be used with the following command:

```bash
python src/automated_runs/automate_sims.py
```
This python scripts iterates over all the simulations and runs the simulation script for each simulation. The data is saved in the `data` directory.


## Training of the Graph Network

The training of the Graph Network is implemented in the `src/training.py` script which takes two arguments: the simulation type (--data) and the regularizer type (--regularizer). The automated run script for training all the models with the different regularizers and simulations used in the study is located in `src/automated_runs/automate_training.py`, which iterates over all the possible combinations of simulations and regularizers. This script is run by the following command:

```bash
python src/automated_runs/automate_training.py
```

The generated models are saved in the `models` directory, under 4 different subdirectories corresponding to the simulation type: charge:`ch`, spring:`sp`, r1:`r1`, r2:`r2`. Under each of these, final trained GN model and learned message vectors over training epochs are saved to be used in the message analysis and symbolic regression.


## Edge Model Analysis
The analysis of the learned message vectors is implemented in the `src/analyze.py` script which creates a gif of the scatter plots showing the correspondence between message vectors and the linear combination fits of true forces. Below each scatter plot, standard deviation of the most variant 15 message components is shown. The gifs are saved in the `data/gifs` directory. This script takes two arguments: the simulation type (--data) and the regularizer type (--regularizer), and similarly automated run script for analyzing all the models with the different regularizers and simulations used in the study is provided in the same script as above `src/automated_runs/automate_training.py`. So runing this automation script as above will both train and analyze all models.


## Symbolic Regression
The symbolic distillation of the edge and node models are implemented in the `src/symbolic_fit.py` script. This script takes two arguments: the simulation type (--data) and the regularizer type (--regularizer). The automated run script for symbolic regression of all the models with the different regularizers and simulations used in the study is located in `src/automated_runs/automate_fits.py`, which iterates over all the possible combinations of simulations and regularizers. This script is run by the following command:

```bash
python src/automated_runs/automate_fits.py
```
The resulted symbolic equations for both dimensions of the node and edge models are saved in a text file inside the `symbolic_fit_results` directory. The comparison of the test loss for the trained GN and the combined symbolic expressions is also saved in the same text file. Morover, this script also makes a plot of the test and train losses over training epochs for each model that is saved in the `symbolic_fit_results` directory.


## HPC Job Submission

Two example Slurm bash scripts are included for easy submission and execution of the project on the CSD3 computer cluster. The `training_slurm_submit.wilkes3` scipt is for the automated training of the Graph Network followed by the edge model analysis for all the systems and regularizers used in the study. This script can be used to submit a job to the cluster with the following command:

```bash
sbatch training_slurm_submit.wilkes3
```

The `symbolic_slurm_submit.wilkes3` script is for the automated symbolic regression of the edge and node models for all the systems and regularizers used in the study. This script can be used to submit a job to the cluster with the following command:

```bash
sbatch PySR_slurm_submit.wilkes3
```

Note that Slurm scripts should be adjusted for runtime, desired number of ranks and number of threads per rank. The full path to application executable should also be adjusted with correct account name. For example the correct path might look like this:

`application="python"`
`options="/home/CRSID/src/automated_runs/automate_fits.py"`



## The use of generative A.I.

ChatGPT 4o was used for suggesting alternative wordings, grammar suggestions, and proofreading while writing the report. The following prompts were used during this process


```
How to represent/write <input symbol> in LaTeX?
```
```
What is another word for <input word>?
```
```
Detect the grammar mistakes in this paragraph. <input paragraph>
```
```
Does this sound logical to a reader? <input paragraph>
```
```
How can I write this in a more clear and direct way? <input sentence>
```
The outputs were selectively adapted, incorporating only alternative wordings and not the entire output while rephrasing the discussion parts of the report.

Furthermore, the suggestions from the autocomplete feature of `GitHub Copilot`, as well as the Cursor tool, were utilized during the documentation of the software and code development of the project. These tools were particularly helpful in editing and adjusting plotting settings for images and figures, as well as writing the LaTeX format labels for the plots generated. Moreover, the sections below are adapted from Dr. Miles Cranmer's public repository for the original paper for the sake of this reproduction study:

- `utils/simulate.py`: Contains functions and classes for particle simulations.
- Functions `linear_transformation_2d()`, `out_linear_transformation_2d()`, and `percentile_sum()` in the `src/analyze.py` script.


## Authors
Sabahattin Mert Daloglu

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.
