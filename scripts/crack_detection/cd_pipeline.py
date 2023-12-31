"""

    Example script:
        Crack Detection Pipeline (path, tip, angle)

    Needed:
        - Folder 'DATA_PATH' containing nodemap files

    Output:
        - txt-file 'crack_info_by_nodemap.txt' containing crack information for each nodemap

"""

# imports
import os

from matplotlib import pyplot as plt

from crackpy.crack_detection.model import get_model
from crackpy.crack_detection.pipeline.pipeline import CrackDetectionSetup, CrackDetectionPipeline

plt.rcParams['image.cmap'] = 'coolwarm'
plt.rcParams['figure.dpi'] = 100

# paths
DATA_PATH = os.path.join('..', '..', 'test_data', 'crack_detection', 'Nodemaps')
OUTPUT_PATH = 'Pipeline_Output'

# tip detector
tip_detector = get_model('ParallelNets')

# path detector
path_detector = get_model('UNetPath')

# setup
det_setup = CrackDetectionSetup(
    specimen_size=160,
    sides=['left', 'right'],
    detection_window_size=40,
    detection_boundary=(0, 70, -35, 35),
    start_offset=(5, 0)
)

# pipeline
cd_pipeline = CrackDetectionPipeline(
    data_path=DATA_PATH,
    output_path=OUTPUT_PATH,
    tip_detector_model=tip_detector,
    path_detector_model=path_detector,
    setup=det_setup
)

cd_pipeline.filter_detection_stages(max_force=15000)
cd_pipeline.run_detection()
cd_pipeline.assign_remaining_stages()
cd_pipeline.write_results('crack_info_by_nodemap.txt')
