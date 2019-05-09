import yaml
import subprocess
import pandas as pd
import os

#Script Settings
root_dir = "C:/Users/Jakob/Documents/GitHub/ml-unity-project" # Change this to your script folder
env_name = "Maze0Multi/Smartball"
brain_name = "RollerBallRayBrain"
out_file_name = "big_list_of_results"


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
max_steps = 2000#5.0e4
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
out_file_exists = os.path.isfile(out_file_name+ ".csv")
i = 0
while(out_file_exists):
    out_file_name += str(i)
    out_file_exists = os.path.isfile(out_file_name+ ".csv")

out_file = open(out_file_name + ".csv", 'w')

# this is the main loop which will run several training scenarios
# it will run for as many times as specified and collect the last result tuple of each run.
# results are saved each iteration

big_list_of_results = None
for i in range(2): 

    # Change parameters here
    # Example:
    # settings["default"]["batch_size"] = 1000 + i

    # Write settings to file
    yaml_to_write = yaml.dump(settings)
    stream = open('./settings.yaml', 'w')
    stream.write(yaml_to_write)
    stream.close()

    run_id = f"Python{i}"

    subprocess.run(f"train.bat {run_id} {env_name}", shell=True, check=True) 
    filename = f'./summaries/{run_id}-0_{brain_name}.csv'

    results = pd.read_csv(filename).tail(1)

    if (big_list_of_results is None):
        big_list_of_results = results
    else:
        big_list_of_results = pd.concat([results, big_list_of_results], ignore_index=True)
    
    out_file.write(big_list_of_results.to_csv())

out_file.close()
