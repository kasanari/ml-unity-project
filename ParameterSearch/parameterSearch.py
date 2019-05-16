import yaml
import subprocess
import pandas as pd
import os
import numpy as np
import winsound
import shutil

# Script Settings
# Change this to your script folder
root_dir = "C:/Users/Jakob/Documents/GitHub/ml-unity-project"
env_name = "Maze0Multi/Smartball"
brain_name = "RollerBallRayBrain"
out_file_name = "results"
base_run_id = "Python"
big_list_of_results = None

# Default settings values
trainer = 'ppo'
batch_size = 1024
beta = 5.0e-3
buffer_size = 10240
epsilon = 0.2
gamma = 0.99
hidden_units = 128
lambd = 0.95
learning_rate = 3.0e-4
max_steps = 2000
memory_size = 256
normalize = False
num_epoch = 3
num_layers = 2
time_horizon = 64
sequence_length = 64
summary_freq = 1000
use_recurrent = False
use_curiosity = False
curiosity_strength = 0.01
curiosity_enc_size = 128

settings = {"default": {'trainer': trainer, 'batch_size': batch_size, 'beta': beta, 'buffer_size': buffer_size, 'epsilon': epsilon,
                        'gamma': gamma, 'hidden_units': hidden_units, "lambd": lambd, "learning_rate": learning_rate, "max_steps": max_steps, "memory_size": memory_size,
                        'normalize': normalize, 'num_epoch': num_epoch, 'num_layers': num_layers, 'time_horizon': time_horizon, 'sequence_length': sequence_length,
                        'summary_freq': summary_freq, 'use_recurrent': use_recurrent, 'use_curiosity': use_curiosity, 'curiosity_strength': curiosity_strength, 'curiosity_enc_size': curiosity_enc_size}}


os.chdir(root_dir)

# If the output file already exists, create another one with an incremented name
if os.path.isdir("./models"):
    print("'models' folder already exists, please do something about it, like saving or removing it.")
    exit()

if os.path.isdir("./summaries"):
    print("'summaries' folder already exists, please do something about it, like saving or removing it.")
    exit()

# If the output file already exists, create another one with an incremented name
out_file_exists = os.path.isfile(out_file_name + ".csv")
i = 0
while(out_file_exists):
    out_file_name = out_file_name[:-1] + str(i)
    out_file_exists = os.path.isfile(out_file_name + ".csv")
    i += 1

with open(out_file_name + ".csv", 'w') as f:
    f.write(
    'Parameter Name, Parameter Value, Mean Reward, Overall Maximum\n')
    f.close()
### ------- PARAMETERS TO TEST ------- ###

# Example of parameter list:
# batch_sizes = [100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
# buffer_sizes = [i*10 for i in batch_sizes]
# gammas = [0.8, 0.85, 0.9, 0.95, 0.995, 1.0]
# lambdas = [0.8, 0.85, 0.9, 0.95, 0.995, 1.0]
# learning_rates = [0.0100, 0.1200, 0.2300, 0.3400, 0.4500, 0.5600, 0.6700, 0.7800, 0.8900, 1.0000]
# learning_rates = [i*1e-3 for i in learning_rates]
# time_horizons = [32, 256, 480, 704, 928, 1152, 1376, 1600, 1824, 2048]

number = 5
gammas = {'name': 'gamma', 'values': np.linspace(0.8, 0.995, number)}
lambdas = {'name': 'lambd', 'values': np.linspace(0.9, 0.95, number)}
batch_sizes = {'name': 'batch_size', 'values': np.linspace(512, 5120, number)}
#buffer_sizes = {'name': 'buffer_size', 'values': [i*10 for i in batch_sizes['values'].tolist()]}
number_of_layers = {'name': 'num_layers', 'values': [1, 2, 3]}
hidden_units = {'name': 'hidden_units', 'values': np.linspace(32, 512, number)}
num_epochs = {'name': 'num_epochs', 'values': np.linspace(3, 11, number)}
learning_rates = {'name': 'learning_rate',
                  'values': np.logspace(-5, -3, number)}
time_horizons = {'name': 'time_horizon',
                 'values': np.linspace(32, 2048, number)}
# max_steps = {'name': 'max_steps', 'values': np.linspace(5e5, 1e7, number)}
betas = {'name': 'beta', 'values': np.logspace(-4, -2, number)}
epsilons = {'name': 'epsilon', 'values': np.linspace(0.1, 0.3, number)}
normalizes = {'name': 'normalize', 'values': [True, False]}

parameters_to_test = [gammas, lambdas, batch_sizes, number_of_layers, hidden_units,
                      num_epochs, learning_rates, time_horizons, betas, epsilons, normalizes]

overall_max_reward = -999999

# -----------------------------------------

#current_param = gammas

# This is the main loop which will run several training scenarios
# It will run for as many times as specified and collect the last result tuple of each run.
# Results are saved each iteration

# betas = [0.0001, 0.0012, 0.0023, 0.0034, 0.0045, 0.0056, 0.0067, 0.0078, 0.0089, 0.0100]
maxima = []

for current_param in parameters_to_test:

    big_list_of_results = None
    name = current_param['name']
    try:
        values = current_param['values'].tolist()
    except:
        values = current_param['values']



    for i in range(len(values)):

        settings["default"][name] = values[i]

        # To ensure the condition that buffer_size = 10*batch_size
        settings["default"]["buffer_size"] = 10 * \
            settings["default"]["batch_size"]

        # Write settings to file
        yaml_to_write = yaml.dump(settings)
        stream = open('./settings.yaml', 'w')
        stream.write(yaml_to_write)
        stream.close()

        run_id = f"{base_run_id}{i}"

        # Run training
        subprocess.run(
            f"train.bat {run_id} {env_name}", shell=True, check=True)
        filename = f'./summaries/{run_id}-0_{brain_name}.csv'

        results = pd.read_csv(filename).tail(1)

        if (big_list_of_results is None):
            big_list_of_results = results
        else:
            big_list_of_results = big_list_of_results.append(
                results, ignore_index=True)
            big_list_of_results = big_list_of_results.reset_index(drop=True)
        # End of a single parameter value

    max_index = big_list_of_results['Mean return'].idxmax(axis=1)
    max_reward = big_list_of_results['Mean return'].max()
    maxima.append([max_reward, max_index])

    if max_reward > overall_max_reward: # Check if the best reward from these parameters were better than the overall best
        settings["default"][name] = values[max_index] # If it was, use that parameter going forward
        overall_max_reward = max_reward

    with open(out_file_name + ".csv", 'a') as f:
        f.write(f'{name}, {values[max_index]}, {max_reward}, {overall_max_reward}\n')
        f.close()
             
    with open(f'{name}.csv', 'w') as f: # save the results for all parameters
        f.write(big_list_of_results.to_csv())
        f.close

    subprocess.run(
        f'7z a -tzip output_archives/{name}.zip "summaries" "models"', shell=True, check=True)
    shutil.rmtree('models')
    shutil.rmtree('summaries')
    # End of a single parameter

# Make a noise to indicate that we are done
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)
# End of program