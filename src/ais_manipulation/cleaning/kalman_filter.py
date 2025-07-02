"""Kalman filtering module.
Returns:
    _type_: _description_
"""

import os
import sys
import csv
import time
import copy
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
import pyproj
import pandas as pd
from haversine import haversine
from shapely.geometry import Point, shape, Polygon, MultiPolygon
from shapely.ops import transform
from shapely.strtree import STRtree
from shapely.validation import make_valid
import numpy as np
from filterpy.kalman import KalmanFilter


CONFIG = None

def kalman_init(_config):
    global CONFIG
    CONFIG = copy.deepcopy(_config)

def create_vessel_kalman_filter(initial_x_m, initial_y_m,
                                  measurement_noise_std_pos=5.0, # meters
                                  process_noise_std_accel=0.5,   # m/s^2
                                  initial_pos_uncertainty=100.0, # meters
                                  initial_vel_uncertainty=10.0   # m/s
                                 ):
    """
    Initializing a KalmanFilter instance for a vessel. 
    For its movement, the constant velocity model is used.
    """
    kf = KalmanFilter(dim_x=4, dim_z=2)
    kf.x = np.array([initial_x_m, initial_y_m, 0., 0.]).T
    kf.P = np.diag([initial_pos_uncertainty**2, initial_pos_uncertainty**2,
                    initial_vel_uncertainty**2, initial_vel_uncertainty**2])
    kf.F = np.array([[1., 0., 0., 0.],
                     [0., 1., 0., 0.],
                     [0., 0., 1., 0.],
                     [0., 0., 0., 1.]])
    kf.H = np.array([[1., 0., 0., 0.],
                     [0., 1., 0., 0.]])
    kf.R = np.diag([measurement_noise_std_pos**2, measurement_noise_std_pos**2])
    Q_var = process_noise_std_accel**2
    kf.Q = np.array([[.25*Q_var, 0, .5*Q_var, 0],
                     [0, .25*Q_var, 0, .5*Q_var],
                     [.5*Q_var, 0, Q_var, 0],
                     [0, .5*Q_var, 0, Q_var]])
    return kf


def kalman_filter_mmsi(file_path,
                        measurement_noise_std_pos = 5.0,
                        process_noise_std_accel = 0.5,
                        initial_pos_uncertainty = 100.0,
                        initial_vel_uncertainty = 10.0,
                        outlier_threshold_chi2 = 20,
                        max_dt_reinitialize = 1800
                        ):
    """
    Applies a Kalman filter to trajectory data of a single vessel, to remove outliers.
    The Kalman filter is re-initialized in the case of long data gaps.
    """

    # HEADER: TIMESTAMP,MMSI,LON,LAT,X,Y,HEADING,COURSE,SPEED,TYPE
    TS, MMSI, LON, LAT, X, Y, HEAD, COG, SOG, TYPE = (0,1,2,3,4,5,6,7,8,9)
    
    with open(file_path, "r",encoding="utf-8") as in_file:
        reader = csv.reader(in_file)

        next(reader) # header
        row = next(reader)
        file_mmsi = row[MMSI]     
        
        ts = 0
        pt = int(row[TS])
        
        kf = create_vessel_kalman_filter(float(row[X]), float(row[Y]),
                                     measurement_noise_std_pos, process_noise_std_accel,
                                     initial_pos_uncertainty, initial_vel_uncertainty)

        filtered_output_path = os.path.join(CONFIG["ais_cleaned_path"], str(file_mmsi) + "_kalmanClean.csv") 
        with open(filtered_output_path, "w",encoding="utf-8") as out_file:
            out_file.write(
                "TIMESTAMP,MMSI,LON,LAT,X,Y,HEADING,COURSE,SPEED,TYPE\n"
            )
            out_file.write(
                f"{row[TS]},{row[MMSI]},{row[LON]},{row[LAT]},{row[X]},{row[Y]},{row[HEAD]},{row[COG]},{row[SOG]},{row[TYPE]}\n"
                )

            discarded_rows = 0
            rows = 1

            for row in reader: # The 'reader' object continues from where 'next()' left off
                rows += 1

                ts = int(row[TS])
                cur_x = float(row[X])
                cur_y = float(row[Y])
                cur_position = np.array([cur_x, cur_y])

                dt = ts - pt # seconds
                if dt > max_dt_reinitialize:
                    kf = create_vessel_kalman_filter(cur_x, cur_y,
                                                    measurement_noise_std_pos, process_noise_std_accel,
                                                    initial_pos_uncertainty, initial_vel_uncertainty)
                    out_file.write(
                        f"{row[TS]},{row[MMSI]},{row[LON]},{row[LAT]},{row[X]},{row[Y]},{row[HEAD]},{row[COG]},{row[SOG]},{row[TYPE]}\n"
                    )
                    pt = ts
                else:
                    kf.F[0, 2] = dt
                    kf.F[1, 3] = dt
                    kf.predict()

                    y = cur_position - (kf.H @ kf.x) 
                    S = kf.H @ kf.P @ kf.H.T + kf.R 
                    mahalanobis_distance_sq = y.T @ np.linalg.inv(S) @ y

                    if mahalanobis_distance_sq <= outlier_threshold_chi2:
                        kf.update(cur_position)
                        out_file.write(
                            f"{row[TS]},{row[MMSI]},{row[LON]},{row[LAT]},{row[X]},{row[Y]},{row[HEAD]},{row[COG]},{row[SOG]},{row[TYPE]}\n"
                        )
                        pt = ts
                    else:
                        discarded_rows += 1

    return [file_mmsi, rows, discarded_rows]


def kalman_filter_data(_config):
    """_summary_

    Args:
        _config (_type_): _description_
        _seas_tree (list, optional): _description_. Defaults to [].
        grid_edge_length (int, optional): _description_. Defaults to -1.

    Returns:
        _type_: _description_
    """
    ais_files_dir = _config["ais_path"]

    # Default data parameters initialization
    maxThreads = _config.get("max_threads", 4)
    
    t_0 = time.time()
    stats_list = []
    futures = {}
    with ProcessPoolExecutor(
        max_workers=maxThreads,
        initializer=kalman_init,
        initargs=(_config,),
    ) as executor:
        for f in os.listdir(ais_files_dir):
            if f.endswith(".csv"):
                file_mmsi = f.split("/")[-1].split("_")[-2]
                futures[executor.submit(kalman_filter_mmsi, (ais_files_dir+f))] = file_mmsi

        for future in as_completed(futures):
            try:
                res = future.result()
                # res.append(futures[future])
                stats_list.append(res)
            except Exception as exc:
                logging.error("Thread exception (%s): %s" , futures[future], exc)

    logging.warning("\t\tCleaning time: %s",time.time() - t_0)
    stats_df = pd.DataFrame(
        stats_list,
        columns=[
            "mmsi",
            "total_rows",
            "discarded_rows_kalman"
        ],
    )
    stats_df.set_index(["mmsi"], inplace=True)
    stats_df.to_csv(_config["ais_stats_path"] + "kalman_stats.csv")

    logging.debug("\n")
    tstats = stats_df.sum()
    trows = tstats["total_rows"]
    
    if trows != 0:
        for column, value in tstats.items():
            logging.debug("\t%s: %.2f %%" ,column, 100 * value / trows)
    else:
        logging.debug("\tEmpty files given. Exiting..")
    return stats_list


if __name__ == "__main__":
  
    import json

    config_file = open(sys.argv[1], "r",encoding="utf-8")
    CONFIG = json.load(config_file)
    kalman_filter_data(CONFIG)
