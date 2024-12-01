import time
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from abc import ABC, abstractmethod
from scripts.document_processing.document_factory import DocumentFactory
from scripts.document_processing.creator_factory import *
from scripts.data_preprocessing.preprocessing import preprocess_data
from utils.visualization import plot_anomaly_pie

# Inicio del pipeline
start_time = time.time()
factory = DocumentFactory()
factory.registerFormat('csv', CreateCSV)
factory.registerFormat('xlsx', CreateExcel)
factory.registerFormat('json', CreateJSON)
