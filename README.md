# Array-SNR-Computation

Authors: Wenjun WANG, Rasmus Alexander JEPSEN (Technical University of Denmark)

This repository contains the core library and example notebooks for computing 
1. Array noise matching—Findeklee, Christian. "Array noise matching—generalization, proof and analogy to power matching." IEEE Transactions on Antennas and Propagation 59.2 (2010): 452-459.
2. Preamplifier decoupling—Wang, Wenjun, et al. "Trade‐off between preamplifier noise figure and decoupling in MRI detectors." Magnetic Resonance in Medicine 89.2 (2023): 859-871.
and comparing the SNR improvement of array noise match with regard to preamplifier decoupling.

The following publication uses this library:
1. Jepsen, Rasmus Alexander, et al. "Evaluating signal-to-noise ratio (SNR) improvement from cryogenic cooling MRI receive coil arrays using full-wave electromagnetic simulation." 2025 47th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC). IEEE, 2025.


## Overview 
Preamplifier decoupling is a valuable method to decouple in-array coil elements. However, in recent years, preamplifier decoupling has been questioned as inessential or even detrimental to achieving optimal SNR because preamplifier decoupling does not account for extra noise from preamplifiers. Array noise matching (ANM) has been proposed as a method to correct for preamplifier noise, which could yield the practically highest possible SNR. In this abstract, we investigate when array noise matching is feasible for coil arrays, and the shortfall of preamplifier-decoupled image SNR relative to ANM for different array channel counts, sizes, and preamplifiers. We show that the highest SNR can be unreachable in practice. When the highest SNR is reachable, preamplifier decoupling yields SNR close to the highest as long as low-noise preamplifiers are used.

The accompanying unpublished article [`assets/Article_V1.pdf`](https://github.com/wenjunhj/array-noise-match-computation/blob/main/assets/Article_V1.pdf) describes how the code works and defines all symbols and quantities. The notebooks in this repository reproduce the figures. The picture below explains how the code works.

![How the code works](https://raw.githubusercontent.com/wenjunhj/array-noise-match-computation/main/assets/Figure_1.png)

## Installation
Python 3.10, 3.11 or 3.12 is required. `numpy` is deliberately restricted to `<2` because the library still uses `np.float_` and `np.complex_`, which were removed in NumPy 2. 

To use the library only:
```
pip install rx-array-snr-evaluation
```

To run the example notebooks, clone this repository and install the library together with the notebook dependencies:
```
git clone https://github.com/wenjunhj/array-noise-match-computation
cd array-noise-match-computation
pip install .
```
This is an editable install, so edits to the library under `src/` take effect immediately. Then start Jupyter from the repository root.

The CST files can be opened in CST Studio Suite 2023 and later versions.

## File Structure
- `./src/rx_array_snr_evaluation`: library core
- `./simulation_files`: CST simulation files for finding optimal overlapping distance, verifying optimal distance, and extracting impedance matrices. Go to the section on simulation files [below](#simulation-files) for more information.
- `./assets`: an unpublished article together with the figures 
These Jupyter notebook files directly produce the results in [`assets/Article_V1.pdf`](https://github.com/wenjunhj/array-noise-match-computation/blob/main/assets/Article_V1.pdf):
1. `convert_hdf5_data.ipynb`: Converts HDF5 files to `numpy` matrices.
2. `process_array_configs.ipynb`: Processes one array configuration out of nine, just for debugging or focused data view.
3. `draw_admissible_regions.ipynb`: Draw Figure 3, Figure 4, Figure 5.

## Usage
### Inputs and Outputs
Inputs required to run the Jupyter notebook files: 
* Impedance matrix $\mathbf{Z}_\mathrm{a}$
* H field of each in-array coil $\mathbf{H}_l,\quad 1\leq l\leq N$

The input files need to follow a certain structure; see the section on the input and output file structure [below](#input-and-output-file-structure).

> [!Important]
> The input files are not included in this repository because of the large sizes; the field of each antenna at plane $z=0$ takes 571,657,392 bytes (545.2 MiB), and the total dataset of 9 array configurations takes up 76.59 GiB. They can, however, be generated from the simulation files. The impedance matrices can be exported from `matZ_overlap_{x}_loops_loaded_size{y}.cst` as `.s{x}p`, where `{x}` is the channel count and `y=1,2,3`. 
> Size 1 means `outer_radius=134.00`, size 2 means `outer_radius=171.28`, and size 3 means `outer_radius=208.56`. The H field of each in-array coil is can be exported from `verify_overlap_{x}_loops_loaded_size{y}.cst` as HDF5 files. 
> To reproduce the results in the manuscript, export the slice $z=0$.
> Currently, only the data from a two-dimensional slice can be processed by the library. 

Outputs of the Jupyter notebook files:
* Signal vector, computed by $\mathbf{u} = \left[\mathbf{M}\cdot \mathbf{H}_1, \mathbf{M}\cdot \mathbf{H}_2, \dots, \mathbf{M}\cdot \mathbf{H}_N\right]$, where $\mathbf{M} = \left[1, \mathrm{j}, 0\right]^\mathsf{T} / \sqrt{2}$, and $\mathbf{u}$ scaled such that $\left\Vert\mathbf{u}\right\Vert = 1$ at center
* O-1 SNR for $\left(F_\mathrm{opt}, Z_{\mathrm{opt}, \mathcal{P}}, N_\mathrm{L}\right)$
* O-2 admissible regions
* O-2c SNR for $\left(F_\mathrm{opt}, Z_{\mathrm{opt}, \mathcal{P}}, N_\mathrm{L}\right)$
* SNR improvement from O-1 to O-2c
Symbols and the exact definitions of O-1, O-2 and O-2c are given in the manuscript.

### Workflow
To reproduce the results in [`assets/Article_V1.pdf`](https://github.com/wenjunhj/array-noise-match-computation/blob/main/assets/Article_V1.pdf), 
1. Simulate all the CST files and export the following into folders named `{x}ch, outer_radius={r}, loop_xy={l}` (see [below](#input-and-output-file-structure)):
    - The H fields of each antenna on slice $z=0$ as `H_Antenna {a}.h5`;
    - The impedance matrix of each array configuration as `matZ_{x}_size{y}.s{x}p`.
2. Run `convert_hdf5_data.ipynb`. You should get `signal_generator_data` files that sit together with the `.h5` and the `.s{x}p` files.
3. Run `process_array_configs.ipynb`. You should get `snr_mapper_data` and `z_matrix_generator_data` files  sit together with the `.h5` and the `.s{x}p` files. 
4. Run `draw_admissible_regions.ipynb` to generate Figures 3, 4, 5 under [`assets/`](https://github.com/wenjunhj/array-noise-match-computation/tree/main/assets/).

> [!IMPORTANT]
> The file `process_array_configs.ipynb` only processes one of the `{x}ch, outer_radius={r}, loop_xy={l}` folders. You need to manually select which one to process. 

### Input and output file structure

The notebooks expect one directory per array configuration, named `{x}ch, outer_radius={r}, loop_xy={l}` , next to the `.cst` files. `loop_xy={l}` means the separation between adjacent two channels:
```
./simulation_files
├── 8ch, outer_radius=134.00, loop_xy=146.11/
├── 8ch, outer_radius=171.28, loop_xy=181.24/
├── 8ch, outer_radius=208.56, loop_xy=213.48/
├── 12ch, outer_radius=134.00, loop_xy=97.60/
├── 12ch, outer_radius=171.28, loop_xy=120.57/
├── 12ch, outer_radius=208.56, loop_xy=143.93/
├── 16ch, outer_radius=134.00, loop_xy=73.73/
├── 16ch, outer_radius=171.28, loop_xy=91.43/
├── 16ch, outer_radius=208.56, loop_xy=109.02/
├── find_overlap_*.cst
├── verify_overlap_*.cst
└── matZ_overlap_*.cst
```

Inside each directory the CST exports look like (not included because of huge size)
```
./simulation_files/{x}ch, outer_radius={r}, loop_xy={l}/
├── H_Antenna 1.h5
├── H_Antenna 2.h5
├── H_Antenna 3.h5
├── H_Antenna 4.h5
├── H_Antenna 5.h5
├── ...
├── H_Antenna 15.h5
├── H_Antenna 16.h5
└── matZ_{x}_size{y}.s{x}p
```

After running `convert_hdf5_data.ipynb` or `process_array_configs.ipynb`, you'll get these extra files in each folder:
```
./simulation_files/{x}ch, outer_radius={r}, loop_xy={l}/
├── signal_generator_data
├── snr_mapper_data-BFP740-[1,j]
├── snr_mapper_data-BFR35AP-[1,j]
├── snr_mapper_data-Elcry2-u-[1,j]
├── snr_mapper_data-Noiseless-[1,j]
├── z_matrix_generator_data-BFP740-[1,j]
├── z_matrix_generator_data-BFR35AP-[1,j]
├── z_matrix_generator_data-Elcry2-u-[1,j]
└── z_matrix_generator_data-Noiseless-[1,j]
```

### Simulation Files
In folder `simulation_files`. There are in total 27 files used for actual simulation. All are configured for 63.89 MHz operation, the proton Larmor frequency at 1.5 T. Configurations differ in:
* Number of loops: 8, 12, 16;
* Sizes: outer_radius=134.00, 171.28, 208.56 mm, labelled also as size 1, size 2, size 3, respectively
* Functions: finding the overlap (`find_overlap_*`), verifying it (`verify_overlap_*`), and extracting the Z matrix (`matZ_overlap_*`).

Optimal overlap (`loop_xy`, mm) for each configuration:

| Channels | outer_radius = 134.00 | outer_radius = 171.28 | outer_radius = 208.56 |
|---------:|----------------------:|----------------------:|----------------------:|
| 8        | 146.11                | 181.24                | 213.48                |
| 12       | 97.60                 | 120.57                | 143.93                |
| 16       | 73.73                 | 91.43                 | 109.02                |

When changing the number of channels of CST models, apply these modifications:
8-channel → 12-channel: 
```
Step 16 chamfer "30", "45", "False", "4"
Step 21 chamfer "30", "45", "False", "9"
Step 80 transform .Angle "0", "0", "360/n_channel"
Step 81 transform .Angle "0", "0", "720/n_channel"
                  .Repetitions "n_channel/2 - 1"
Step 82 transform .Angle "0", "0", "720/n_channel"
             .Repetitions "n_channel/2 - 1"
Step 80 transform .Angle "0", "0", "360/n_channel"
```
12-channel → 16-channel:
```
Step 16 chamfer "20", "45", "False", "4"
Step 21 chamfer "20", "45", "False", "9"
```

## Library API
### Class `SignalVectorGenerator`
A class that generates signal vectors for a given set of magnetic (H) fields. 

Note that `h_field` should have 3 dimensions, whereof 
- the first dimension (`axis=0`) equals the number of channels, 
- the second dimension (`axis=1`) equals the number of pixels,
- the third dimension (`axis=2`)  is 3, corresponding to vector's x, y, and z components.

Construction is based on Lorentz Reciprocity Theorem. Assume the magnetic moment can be written as $\mathbf{M}^+ = [1, \mathrm{j}, 0]$, which can be equivalently expressed in a complex-number form $m^+ = 1+\mathrm{j}$. Using the vector form, the signal of channel $l$ should equal $c \mathbf{M}^+ \cdot \mathbf{H}_l$, where c is a constant for a particular array geometry, $\mathbf{H}_l$ is the magnetic field generated by channel $l$ when unit current is injected to channel $l$ and every other channel is open-circuited. All signals from each channel form a vector $\mathbf{u} = \left[ \mathbf{M}^+ \cdot \mathbf{H}_1, \mathbf{M}^+ \cdot \mathbf{H}_2, \dots, \mathbf{M}^+ \cdot \mathbf{H}_{N-1} \right]^\mathsf{T}$. Then $\mathbf{u}$ is normalized.

### Class `ImpedanceMatrixGenerator`
A class that generates the SNR core matrices defined by Equation (39) in Christian Findeklee's "Array Noise Matching--Generalization, Proof and Analogy to Power Matching", IEEE Transactions on Antennas and Propagation, Vol. 59, No. 2, Feb 2011. The SNR core matrices can be further used for generating SNR maps.

### Class `SNRMapper`
Generates SNR maps from SNR cores defined in Equation (39) of Christian Findeklee's "Array Noise Matching", and signal vectors. 

## Known issues
1. This whole code piece is designed to handle complex three-dimensional vectors on a three-dimensional grid. As of Apr 8, 2025, the code works for two-dimensional case, but not for the three-dimensional one, because in CST HDF5 exports 3D data have different field names from those of 2D HDF5 exports! Once that gets fixed, the three-dimensional case should work as well. 
2. `grid.py` is meant to contain a dedicated grid class, but it has not been integrated into `field.py` yet. Currently class `SNRMapper` still has its own grid implementation, which is not a good design.

## Authors and Acknowledgement
This repository was created by Wang, Wenjun and Jepsen, Rasmus Alexander for the Technical University of Denmark (DTU).

This project has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement No 856432).

## License
A copy of the MIT license is available in the LICENSE file.

Copyright © 2026 Technical University of Denmark (developed by Wang, Wenjun and Jepsen, Rasmus Alexander)
