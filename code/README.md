# iSTTC Pipeline - Intrinsic Timescale Analysis

Intrinsic Spike Time Tiling Coefficient (iSTTC) analysis pipeline for computing neuronal timescales from spike train data.

**Reference**: Pochinok et al. (2025), Shi et al. (2025)

---

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Access to International Brain Laboratory (IBL) data (optional, for IBL-specific usage)

---

## Installation

### Step 1: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv isttc_env

# Activate virtual environment
# On Windows:
isttc_env\Scripts\activate
# On macOS/Linux:
source isttc_env/bin/activate
```

### Step 2: Install Required Packages

```bash
pip install -r requirements.txt
```

**Package Descriptions:**
- `ONE-api`: International Brain Laboratory data access (required for IBL sessions)
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computing
- `scipy`: Scientific computing (curve fitting, statistics)
- `matplotlib`: Plotting and visualization
- `seaborn`: Statistical data visualization
- `tqdm`: Progress bars
- `numba`: JIT compilation for performance
- `joblib`: Parallel processing

### Step 3: Verify Installation

```bash
python -c "import numpy, pandas, scipy, matplotlib, numba, joblib, tqdm; print('All packages installed successfully!')"
```

For IBL data access:
```bash
python -c "from one.api import ONE; print('ONE-api installed successfully!')"
```

---

## Quick Start

### Option A: Using IBL Data (Requires ONE-api and IBL credentials)

1. **Configure your sessions** in `isttc_pipeline.py`:

```python
if __name__ == '__main__':
    from one.api import ONE

    # Add your session tuples: (eid, pid, probe_name)
    SESSIONS = [
        ('eid-12345', 'pid-67890', 'probe00'),
        ('eid-abcde', 'pid-fghij', 'probe01'),
    ]

    one = ONE(
        base_url='https://openalyx.internationalbrainlab.org',
        username='intbrainlab',
        password='international',
        silent=True,
    )

    results = run_sessions(one, pids=SESSIONS, output_csv='good_isttc.csv')
```

2. **Run the pipeline**:

```bash
python isttc_pipeline.py
```

### Option B: Using Custom Spike Data (Standalone, No ONE-api Required)

If you have your own spike time data and don't need IBL access:

```python
from isttc_pipeline import analyze_single_neuron
import numpy as np

# Your spike times (in seconds)
spike_times = np.array([0.1, 0.3, 0.5, 0.8, 1.2, 1.5, ...])
recording_duration = 600.0  # seconds

# Analyze
result = analyze_single_neuron(
    spike_times=spike_times,
    recording_duration=recording_duration,
    neuron_id='MyNeuron_001'
)

# Print results
print(f"Effective timescale: {result['tau_effective_ms']:.2f} ms")
print(f"Number of components: {result['n_timescales']}")
print(f"R²: {result['r_squared']:.3f}")
print(f"Passed QC: {result['passed_quality_filter']}")
```


## Output

### CSV Output (`good_isttc.csv`)
Contains neurons that passed quality criteria:
- `tau_effective_ms`: Effective timescale (milliseconds)
- `n_timescales`: Number of exponential components (1-4)
- `tau_1_ms`, `tau_2_ms`, etc.: Individual timescale components
- `r_squared`: Goodness of fit
- `firing_rate_hz`: Mean firing rate
- `local_variance_lv`: Local variance (regularity metric)
- Quality flags: `passed_quality_filter`, `ci_excludes_zero`, etc.

### Plots (`isttc_summary_plots/`)
- iSTTC autocorrelation curves
- Multi-exponential fits
- Quality control indicators

---

## Quality Criteria

Neurons pass QC if ALL conditions are met:
1. **ACF decline (50-200ms)**: Autocorrelation decreases in this window
2. **CI excludes zero**: 95% confidence interval for τ_eff > 0
3. **R² ≥ 0.5**: Good fit quality
4. **Spike count ≥ 100**: Sufficient data
5. **τ not at bound**: Timescale not hitting upper limit

---

## Troubleshooting

### Error: Numba compilation warnings

**Solution**: This is normal on first run. Numba compiles functions for speed. Subsequent runs will be faster.

### Error: `No passive epoch found`

**Solution**: For IBL sessions, ensure the session has trials or `passivePeriods` data. Check session metadata.

---

## Configuration

Edit these parameters in `isttc_pipeline.py`:

```python
OUTPUT_CSV = 'good_isttc.csv'        # Output filename
OUTPUT_DIR = 'isttc_summary_plots'   # Plot directory
MIN_SPIKE_COUNT = 100                 # Minimum spikes for analysis

# iSTTC parameters
delta_t = 0.005      # Coincidence window (5ms)
nlags = 600          # Number of lag points
lag_shift = 0.01     # Lag increment (10ms)
max_components = 4   # Maximum exponential components
```

---

## Example: Complete Workflow

```python
from isttc_pipeline import analyze_single_neuron, plot_single_neuron
import numpy as np
import matplotlib.pyplot as plt

# Generate or load your spike times
spike_times = np.random.exponential(scale=0.1, size=1000).cumsum()
recording_duration = spike_times[-1]

# Analyze
result = analyze_single_neuron(
    spike_times=spike_times,
    recording_duration=recording_duration,
    neuron_id='ExampleNeuron'
)

# Visualize
fig = plot_single_neuron(result, title='Example Neuron Analysis')
plt.savefig('example_neuron.png', dpi=150, bbox_inches='tight')
plt.show()

# Check results
print(f"τ_effective: {result['tau_effective_ms']:.1f} ms")
print(f"Quality: {'PASSED' if result['passed_quality_filter'] else 'FAILED'}")
```

---

## Citation

If you use this pipeline, please cite:
- Pochinok et al. (2026) - iSTTC methodology
- Shi et al. (2025) - Multi-timescale fitting approach

---

## Support

For issues or questions:
1. Check this README first
2. Verify all dependencies are installed: `pip list`
3. Test with minimal example (Option B above)
4. Report specific error messages with Python version and OS

---

## License

Copyright (c) 2026 Decisive Times
Licensed under the MIT License