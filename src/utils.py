import pathlib
import yaml
import torch
import random

import numpy as np
from omegaconf  import OmegaConf


def set_random_seed(seed, is_gpu=False):
    """Set random seeds for reproducability"""

    max_seed_value = np.iinfo(np.uint32).max
    min_seed_value = np.iinfo(np.uint32).min

    if not (min_seed_value <= seed <= max_seed_value):
        raise ValueError("seed {} is not in bounds, numpy accepts seeds from {} to {}".format(seed, min_seed_value, max_seed_value))

    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

    if torch.cuda.is_available() and is_gpu:
        torch.cuda.manual_seed_all(seed)


def get_device(is_gpu=True, gpu_number=0):
    """
    Set the backend for model training
    """
    gpu_count = torch.cuda.device_count()
    if gpu_count < gpu_number:
        raise ValueError("number of cuda devices: '{}'".format(gpu_count))
    else:
        if torch.cuda.is_available() and is_gpu:
            device = torch.device("cuda:{}".format(gpu_number))
        else:
            device = torch.device("cpu")

    return device


def create_dirs(run_id, prefix):
    """
    Create directories for a experiment run
    """

    run_id = "-".join(map(str, filter(None, [prefix, run_id])))
    
    models_dir = pathlib.Path("./models")
    models_dir = models_dir / run_id
    models_dir.mkdir(parents=True)

    results_dir = pathlib.Path("./results")
    results_dir = results_dir / run_id
    results_dir.mkdir(parents=True)

    return models_dir, results_dir


def load_config(filepath="./config.yaml"):
    """
    Load config file
    """
    try:
        config = OmegaConf.load(filepath)

        return config
    
    except:
        raise IOError("cannot load: '{}'".format(filepath))


def save_config(config, save_dir, filename="config.yaml"):
    """
    Save config file
    """
    try:
        filepath = save_dir  /  filename
        
        if isinstance(config, dict):
            with open(save_dir  /  filename, "w") as outfile:
                yaml.dump(config, outfile)
        
        else:
            OmegaConf.save(config, filepath)
    
    except:
        raise IOError("cannot save: '{}'".format(file_path))


