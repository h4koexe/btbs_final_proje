from utils import resource_path
import pandas as pd

def load_demands(demand_csv):
    return pd.read_csv(resource_path(demand_csv), sep=";")
