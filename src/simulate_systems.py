# Importing required libraries

import torch
import numpy as np
import matplotlib.pyplot as plt
import torch
import os
import subprocess
import sys
# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, '../utils'))    # Add the utils directory to the path
from simulate import SimulationDataset   # Import the simulation code defined in the same directory
import argparse

# Import the module required for simulations
subprocess.run(['pip', 'install', 'celluloid'])

# Import the module required for the neural network
version_nums = torch.__version__.split('.')
# Torch Geometric seems to always build for *.*.0 of torch :
version_nums[-1] = '0' + version_nums[-1][1:]
os.environ['TORCH'] = '.'.join(version_nums)

subprocess.run(['pip', 'install', '--upgrade', 'torch-scatter', '-f', 'https://pytorch-geometric.com/whl/torch-${TORCH}.html'])
subprocess.run(['pip', 'install', '--upgrade', 'torch-sparse', '-f', 'https://pytorch-geometric.com/whl/torch-${TORCH}.html'])
subprocess.run(['pip', 'install', '--upgrade', 'torch-geometric'])


# Checking if the NVIDIA GPU is available (on the cloud service if run on Colab)
if torch.cuda.is_available():
  device = torch.device("cuda")
  x = torch.rand(3)
  x = x.to(device)
  print(x)
elif torch.backends.mps.is_available():
  device = torch.device("mps")
  print("Using the Mac's GPU")
else:
  device = torch.device("cpu")
  print("CUDA or MPS is not available using CPU")
  
  
  
##################################################################
################## Experiment & Simulation #######################
##################################################################

# Number of simulations to run - Number of data points (can increase to 100,000 if trapazoidal rule is used instead of RK4)
ns = 10000
# Potential (see below for options)
parser = argparse.ArgumentParser(description='Select the simulation type.')
parser.add_argument('--sim', type=str, help='Simulation type (e.g., r1, r2, spring, charge)', default='r2')
args = parser.parse_args()
sim = args.sim
# Number of nodes
n_particles = 4
# Dimension
dim = 2
# Number of time steps & proportional to the duration of the simulation
nt = 1000


#Standard simulation sets:
n_set = [4, 8]
sim_sets = [
 {'sim': 'r1', 'dt': [5e-3], 'nt': [1000], 'n': n_set, 'dim': [2, 3]},
 {'sim': 'r2', 'dt': [1e-3], 'nt': [1000], 'n': n_set, 'dim': [2, 3]},
 {'sim': 'spring', 'dt': [1e-2], 'nt': [1000], 'n': n_set, 'dim': [2, 3]},
 {'sim': 'string', 'dt': [1e-2], 'nt': [1000], 'n': [30], 'dim': [2]},
 {'sim': 'charge', 'dt': [1e-3], 'nt': [1000], 'n': n_set, 'dim': [2, 3]},
 {'sim': 'superposition', 'dt': [1e-3], 'nt': [1000], 'n': n_set, 'dim': [2, 3]},
 {'sim': 'damped', 'dt': [2e-2], 'nt': [1000], 'n': n_set, 'dim': [2, 3]},
 {'sim': 'discontinuous', 'dt': [1e-2], 'nt': [1000], 'n': n_set, 'dim': [2, 3]},
]


#Select the hand-tuned dt value for a smooth simulation
# (since scales are different in each potential):
dt = [ss['dt'][0] for ss in sim_sets if ss['sim'] == sim][0]
title = '{}_n={}_dim={}'.format(sim, n_particles, dim)

s = SimulationDataset(sim, n=n_particles, dim=dim, nt=nt//2, dt=dt)
# Update this to your own dataset, or regenerate:
base_str = './'
data_str = title
s.simulate(ns, key = 42)

# Save the data
data = s.data
s.data.shape

# Save the data to a file
# Create a new directory called data if it does not exist and save the data
if not os.path.exists('data'):
  os.mkdir('data')
  
# Save the data to a file named after the simulation
script_dir = os.path.dirname(__file__)  
np.save(os.path.join(script_dir, '..', 'data', '{}_data.npy'.format(title)), data)
np.save(os.path.join(script_dir, '..', 'data', '{}_acc.npy'.format(title)), s.get_acceleration())
  
  
  
