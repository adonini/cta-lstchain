import numpy as np
from lstchain.calib.camera.calib import gain_selection
from astropy.utils import deprecated
from lstchain.calib import load_calibrator_from_config, load_gain_selector_from_config, load_image_extractor_from_config


@deprecated('28/06/2019', message='gain selection is now performed at <= R1 calibration level')
def test_gain_selection():
    """
    test gain selection
    """
    # Let's generate a fake waveform from a camera of 3 samples and 10 pixels
    n_samples = 3
    w1 = np.transpose([np.concatenate([np.ones(5), 3 * np.ones(5)]) for i in range(n_samples)])
    w2 = np.transpose([10 * np.ones(10) for i in range(n_samples)])
    waveform = np.array([w1, w2])
    image = waveform.mean(axis=2)

    threshold = 2
    combined_image, _ = gain_selection(waveform, image, image, threshold)

    # with a threshold of 2, the 5 first pixels should be selected in the first channel and 5 others in the second \
    # channel

    np.testing.assert_array_equal(combined_image, np.array([1, 1, 1, 1, 1, 10, 10, 10, 10, 10]))


def test_load_calibrator_from_config():
    from lstchain.io.config import get_standard_config
    from ctapipe.calib import CameraCalibrator
    from ctapipe.image import NeighborPeakWindowSum
    from ctapipe.calib.camera.gainselection import ThresholdGainSelector
    config = get_standard_config()
    cal = load_calibrator_from_config(config)

    assert isinstance(cal.image_extractor, NeighborPeakWindowSum)
    assert isinstance(cal.gain_selector, ThresholdGainSelector)
    assert isinstance(cal, CameraCalibrator)

def test_load_calibrator_from_config_LocalPeakWindowSum():
    from ctapipe.image import LocalPeakWindowSum
    config = {"image_extractor": "LocalPeakWindowSum"}

    cal = load_calibrator_from_config(config)

    assert isinstance(cal.image_extractor, LocalPeakWindowSum)

def test_load_calibrator_from_config_GlobalPeakWindowSum():
    from ctapipe.image import GlobalPeakWindowSum
    config = {"image_extractor": "GlobalPeakWindowSum"}

    cal = load_calibrator_from_config(config)

    assert isinstance(cal.image_extractor, GlobalPeakWindowSum)


def test_load_calibrator_from_config_ThresholdGainSelector():

    config = {"gain_selector": "ThresholdGainSelector",
              "gain_selector_config": {"threshold": 300}}
    cal = load_calibrator_from_config(config)

    assert cal.gain_selector.threshold == 300


def test_load_calibrator_from_config_ManualGainSelector():
    from ctapipe.calib.camera.gainselection import ManualGainSelector

    for chan in ["HIGH", "LOW"]:
        config = {"gain_selector": "ManualGainSelector",
                  "gain_selector_config": {"channel": chan}
        }

        cal = load_calibrator_from_config(config)

        assert isinstance(cal.gain_selector, ManualGainSelector)
        assert cal.gain_selector.channel == chan


def test_load_image_extractor_from_config():
    from ctapipe.image import LocalPeakWindowSum

    config = {'image_extractor': 'LocalPeakWindowSum',
              'image_extractor_config': {
                          "window_shift": 1,
                          "window_width": 10,
                      }
    }

    image_extractor = load_image_extractor_from_config(config)

    assert isinstance(image_extractor, LocalPeakWindowSum)
    assert image_extractor.window_shift == 1
    assert image_extractor.window_width == 10


def test_load_gain_selector_from_config_ManualGainSelector():
    from ctapipe.calib.camera.gainselection import ManualGainSelector

    for chan in ["HIGH", "LOW"]:
        config = {"gain_selector": "ManualGainSelector",
                  "gain_selector_config": {"channel": chan}
        }

        gain_selector = load_gain_selector_from_config(config)

        assert isinstance(gain_selector, ManualGainSelector)
        assert gain_selector.channel == chan