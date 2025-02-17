import yaml
import subprocess
import pandas as pd
import os

#Script Settings
root_dir = "C:/Users/Jakob/Documents/GitHub/ml-unity-project" # Change this to your script folder
env_name = "Maze0Multi/Smartball"
brain_name = "RollerBallRayBrain"
out_file_name = "big_list_of_results"
base_run_id = "Python"
big_list_of_results = None

#Default settings values
trainer = 'ppo'
batch_size = 1024
beta = 5.0e-3
buffer_size = 10240
epsilon = 0.2
gamma = 0.99
hidden_units = 128
lambd = 0.95
learning_rate = 3.0e-4
max_steps = 5.0e4
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
                         'gamma':gamma, 'hidden_units': hidden_units, "lambd":lambd, "learning_rate": learning_rate, "max_steps": max_steps, "memory_size": memory_size,
                         'normalize':normalize, 'num_epoch':num_epoch, 'num_layers':num_layers, 'time_horizon':time_horizon, 'sequence_length':sequence_length,
                         'summary_freq':summary_freq, 'use_recurrent':use_recurrent, 'use_curiosity':use_curiosity, 'curiosity_strength':curiosity_strength, 'curiosity_enc_size':curiosity_enc_size}}


os.chdir(root_dir)

# If the output file already exists, create another one with an incremented name
if os.path.isdir("./models"):
    print("'models' folder already exists, please do something about it, like saving or removing it.")
    exit()

if os.path.isdir("./summaries"):
     print("'summaries' folder already exists, please do something about it, like saving or removing it.")
     exit()

# If the output file already exists, create another one with an incremented name
out_file_exists = os.path.isfile(out_file_name+ ".csv")
i = 0
while(out_file_exists):
    out_file_name += str(i)
    out_file_exists = os.path.isfile(out_file_name+ ".csv")

out_file = open(out_file_name + ".csv", 'w')

### ------- PARAMETERS TO TEST ------- ###

# Example of parameter list: 
# batch_sizes = [100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
# buffer_sizes = [i*10 for i in batch_sizes]

# -----------------------------------------

# This is the main loop which will run several training scenarios
# It will run for as many times as specified and collect the last result tuple of each run.
# Results are saved each iteration

for i in range(1): # <-- Change this to whatever the length of the main parameter list is, eg. range(len(batch_sizes))

    # Change parameters here
    # Example:
    # settings["default"]["batch_size"] = 1000 + i

    # settings["default"]["batch_size"] = batch_sizes[i]
    # settings["default"]["buffer_size"] = buffer_sizes[i]

    # Write settings to file
    yaml_to_write = yaml.dump(settings)
    stream = open('./settings.yaml', 'w')
    stream.write(yaml_to_write)
    stream.close()

    run_id = f"{base_run_id}{i}"

    # Run training
    subprocess.run(f"train.bat {run_id} {env_name}", shell=True, check=True) 
    filename = f'./summaries/{run_id}-0_{brain_name}.csv'

    # Write final result to csv file
    results = pd.read_csv(filename).tail(1)

    if (big_list_of_results is None):
        big_list_of_results = results
    else:
        big_list_of_results = pd.concat([big_list_of_results, results], ignore_index=True)
    
    out_file.write(big_list_of_results.to_csv())

out_file.close()
