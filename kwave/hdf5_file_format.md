# From k-wave_user_manual_1.1.pdf

## Table B.1: List of datasets that may be present in the input HDF5 file.

Note, MATLAB automatically converts HDF5 files from column-major to row-major ordering. If creating files outside MATLAB, dataset dimensions should be given as (Nz, Ny, Nx).

1. Simulation Flags (implemented = False)

| Name                   | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions       |
| ---------------------- | ----------------- | --------- | ----------- | ---------------- |
| ux_source_flag         | (1, 1, 1)         | long      | real        |                  |
| uy_source_flag         | (1, 1, 1)         | long      | real        |                  |
| uz_source_flag         | (1, 1, 1)         | long      | real        |                  |
| p_source_flag          | (1, 1, 1)         | long      | real        |                  |
| p0_source_flag         | (1, 1, 1)         | long      | real        |                  |
| transducer_source_flag | (1, 1, 1)         | long      | real        |                  |
| nonuniform_grid_flag   | (1, 1, 1)         | long      | real        | must be set to 0 |
| nonlinear_flag         | (1, 1, 1)         | long      | real        |                  |
| absorbing_flag         | (1, 1, 1)         | long      | real        |                  |

2. Grid Properties (implemented = False)

| Name | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions |
| ---- | ----------------- | --------- | ----------- | ---------- |
| Nx   | (1, 1, 1)         | long      | real        |            |
| Ny   | (1, 1, 1)         | long      | real        |            |
| Nz   | (1, 1, 1)         | long      | real        |            |
| Nt   | (1, 1, 1)         | long      | real        |            |
| dt   | (1, 1, 1)         | float     | real        |            |
| dx   | (1, 1, 1)         | float     | real        |            |
| dy   | (1, 1, 1)         | float     | real        |            |
| dz   | (1, 1, 1)         | float     | real        |            |

3. Medium Properties (implemented = False)

3.1 Regular Medium Properties (implemented = False)

| Name     | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions    |
| -------- | ----------------- | --------- | ----------- | ------------- |
| rho0     | (Nx, Ny, Nz)      | float     | real        | heterogeneous |
|          | (1, 1, 1)         | float     | real        | homogeneous   |
| rho0_sgx | (Nx, Ny, Nz)      | float     | real        | heterogeneous |
|          | (1, 1, 1)         | float     | real        | homogeneous   |
| rho0_sgy | (Nx, Ny, Nz)      | float     | real        | heterogeneous |
|          | (1, 1, 1)         | float     | real        | homogeneous   |
| rho0_sgz | (Nx, Ny, Nz)      | float     | real        | heterogeneous |
|          | (1, 1, 1)         | float     | real        | homogeneous   |
| c0       | (Nx, Ny, Nz)      | float     | real        | heterogeneous |
|          | (1, 1, 1)         | float     | real        | homogeneous   |
| c_ref    | (1, 1, 1)         | float     | real        |               |

3.2 Nonlinear Medium Properties (defined if `nonlinear_flag = 1`) (implemented = False)

| Name | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions    |
| ---- | ----------------- | --------- | ----------- | ------------- |
| BonA | (Nx, Ny, Nz)      | float     | real        | heterogeneous |
|      | (1, 1, 1)         | float     | real        | homogeneous   |

3.3 Absorbing Medium Properties (defined if `absorbing_flag = 1`) (implemented = False)

| Name        | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions    |
| ----------- | ----------------- | --------- | ----------- | ------------- |
| alpha_coeff | (Nx, Ny, Nz)      | float     | real        | heterogeneous |
|             | (1, 1, 1)         | float     | real        | homogeneous   |
| alpha_power | (1, 1, 1)         | float     | real        |               |

4. Sensor Properties (implemented = False)

| Name                | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions           |
| ------------------- | ----------------- | --------- | ----------- | -------------------- |
| sensor_mask_type    | (1, 1, 1)         | long      | real        |                      |
| sensor_mask_index   | (Nsens, 1, 1)     | long      | real        | sensor_mask_type = 0 |
| sensor_mask_corners | (Ncubes, 6, 1)    | long      | real        | sensor_mask_type = 1 |

5. Source Properties (implemented = False)

5.1 Velocity Source Terms (defined if `ux_source_flag = 1` or `uy_source_flag = 1` or `uz_source_flag = 1`) (implemented = False)

| Name            | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions        |
| --------------- | ----------------- | --------- | ----------- | ----------------- |
| u_source_mode   | (1, 1, 1)         | long      | real        |                   |
| u_source_many   | (1, 1, 1)         | long      | real        |                   |
| u_source_index  | (Nsrc, 1, 1)      | long      | real        |                   |
| ux_source_input | (1, Nt_src, 1)    | float     | real        | u_source_many = 0 |
|                 | (Nsrc, Nt_src, 1) | float     | real        | u_source_many = 1 |
| uy_source_input | (1, Nt_src, 1)    | float     | real        | u_source_many = 0 |
|                 | (Nsrc, Nt_src, 1) | float     | real        | u_source_many = 1 |
| uz_source_input | (1, Nt_src, 1)    | float     | real        | u_source_many = 0 |
|                 | (Nsrc, Nt_src, 1) | float     | real        | u_source_many = 1 |

5.2 Pressure Source Terms (defined if `p_source_flag = 1`) (implemented = False)

| Name           | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions        |
| -------------- | ----------------- | --------- | ----------- | ----------------- |
| p_source_mode  | (1, 1, 1)         | long      | real        |                   |
| p_source_many  | (1, 1, 1)         | long      | real        |                   |
| p_source_index | (Nsrc, 1, 1)      | long      | real        |                   |
| p_source_input | (1, Nt_src, 1)    | float     | real        | p_source_many = 0 |
|                | (Nsrc, Nt_src, 1) | float     | real        | p_source_many = 1 |

5.3 Transducer Source Terms (defined if `transducer_source_flag = 1`) (implemented = False)

| Name                    | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions |
| ----------------------- | ----------------- | --------- | ----------- | ---------- |
| u_source_index          | (Nsrc, 1, 1)      | long      | real        |            |
| transducer_source_input | (Nt_src, 1, 1)    | float     | real        |            |
| delay_mask              | (Nsrc, 1, 1)      | float     | real        |            |

5.4 IVP Source Terms (defined if `p0_source_flag = 1`) (implemented = False)

| Name            | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions |
| --------------- | ----------------- | --------- | ----------- | ---------- |
| p0_source_input | (Nx, Ny, Nz)      | float     | real        |            |

6. k-space and Shift Variables (implemented = False)

| Name              | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions |
| ----------------- | ----------------- | --------- | ----------- | ---------- |
| ddx_k_shift_pos_r | (Nx/2 + 1, 1, 1)  | float     | complex     |            |
| ddx_k_shift_neg_r | (Nx/2 + 1, 1, 1)  | float     | complex     |            |
| ddy_k_shift_pos   | (1, Ny, 1)        | float     | complex     |            |
| ddy_k_shift_neg   | (1, Ny, 1)        | float     | complex     |            |
| ddz_k_shift_pos   | (1, 1, Nz)        | float     | complex     |            |
| ddz_k_shift_neg   | (1, 1, Nz)        | float     | complex     |            |
| x_shift_neg_r     | (Nx/2 + 1, 1, 1)  | float     | complex     |            |
| y_shift_neg_r     | (1, Ny/2 + 1, 1)  | float     | complex     |            |
| z_shift_neg_r     | (1, 1, Nz/2 + 1)  | float     | complex     |            |

7. PML Variables (implemented = False)

| Name        | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions |
| ----------- | ----------------- | --------- | ----------- | ---------- |
| pml_x_size  | (1, 1, 1)         | long      | real        |            |
| pml_y_size  | (1, 1, 1)         | long      | real        |            |
| pml_z_size  | (1, 1, 1)         | long      | real        |            |
| pml_x_alpha | (1, 1, 1)         | float     | real        |            |
| pml_y_alpha | (1, 1, 1)         | float     | real        |            |
| pml_z_alpha | (1, 1, 1)         | float     | real        |            |
| pml_x       | (Nx, 1, 1)        | float     | real        |            |
| pml_x_sgx   | (Nx, 1, 1)        | float     | real        |            |
| pml_y       | (1, Ny, 1)        | float     | real        |            |
| pml_y_sgy   | (1, Ny, 1)        | float     | real        |            |
| pml_z       | (1, 1, Nz)        | float     | real        |            |
| pml_z_sgz   | (1, 1, Nz)        | float     | real        |            |

## Table B.2: List of datasets present in the checkpoint HDF5 file.

## Table B.3: List of datasets present in the output HDF5 file.

1. Simulation Flags (implemented = False)

| Name                   | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions  |
| ---------------------- | ----------------- | --------- | ----------- | ----------- |
| ux_source_flag         | (1, 1, 1)         | long      | real        |             |
| uy_source_flag         | (1, 1, 1)         | long      | real        |             |
| uz_source_flag         | (1, 1, 1)         | long      | real        |             |
| p_source_flag          | (1, 1, 1)         | long      | real        |             |
| p0_source_flag         | (1, 1, 1)         | long      | real        |             |
| transducer_source_flag | (1, 1, 1)         | long      | real        |             |
| nonuniform_grid_flag   | (1, 1, 1)         | long      | real        |             |
| nonlinear_flag         | (1, 1, 1)         | long      | real        |             |
| absorbing_flag         | (1, 1, 1)         | long      | real        |             |
| u_source_mode          | (1, 1, 1)         | long      | real        | if u_source |
| u_source_many          | (1, 1, 1)         | long      | real        | if u_source |
| p_source_mode          | (1, 1, 1)         | long      | real        | if p_source |
| p_source_many          | (1, 1, 1)         | long      | real        | if p_source |

2. Grid Properties (implemented = False)

| Name | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions |
| ---- | ----------------- | --------- | ----------- | ---------- |
| Nx   | (1, 1, 1)         | long      | real        |            |
| Ny   | (1, 1, 1)         | long      | real        |            |
| Nz   | (1, 1, 1)         | long      | real        |            |
| Nt   | (1, 1, 1)         | long      | real        |            |
| dt   | (1, 1, 1)         | float     | real        |            |
| dx   | (1, 1, 1)         | float     | real        |            |
| dy   | (1, 1, 1)         | float     | real        |            |
| dz   | (1, 1, 1)         | float     | real        |            |

3. PML Variables (implemented = False)

| Name        | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions |
| ----------- | ----------------- | --------- | ----------- | ---------- |
| pml_x_size  | (1, 1, 1)         | long      | real        |            |
| pml_y_size  | (1, 1, 1)         | long      | real        |            |
| pml_z_size  | (1, 1, 1)         | long      | real        |            |
| pml_x_alpha | (1, 1, 1)         | float     | real        |            |
| pml_y_alpha | (1, 1, 1)         | float     | real        |            |
| pml_z_alpha | (1, 1, 1)         | float     | real        |            |
| pml_x       | (Nx, 1, 1)        | float     | real        |            |
| pml_x_sgx   | (Nx, 1, 1)        | float     | real        |            |
| pml_y       | (1, Ny, 1)        | float     | real        |            |
| pml_y_sgy   | (1, Ny, 1)        | float     | real        |            |
| pml_z       | (1, 1, Nz)        | float     | real        |            |
| pml_z_sgz   | (1, 1, Nz)        | float     | real        |            |

4. Sensor Variables (defined if --copy_sensor_mask) (implemented = False)

| Name                | Size (Nx, Ny, Nz) | Data Type | Domain Type | Conditions           |
| ------------------- | ----------------- | --------- | ----------- | -------------------- |
| sensor_mask_type    | (1, 1, 1)         | long      | real        |                      |
| sensor_mask_index   | (Nsens, 1, 1)     | long      | real        | sensor_mask_type = 0 |
| sensor_mask_corners | (Ncubes, 6, 1)    | long      | real        | sensor_mask_type = 1 |

5. Simulation Results

5.1 Binary Sensor Mask (defined if sensor_mask_type = 0) (implemented = False)

| Name             | Size (Nx, Ny, Nz)  | Data Type | Domain Type | Conditions        |
| ---------------- | ------------------ | --------- | ----------- | ----------------- |
| p                | (Nsens, Nt-s+1, 1) | float     | real        | -p or --p_raw     |
| p_rms            | (Nsens, 1, 1)      | float     | real        | --p_rms           |
| p_max            | (Nsens, 1, 1)      | float     | real        | --p_max           |
| p_min            | (Nsens, 1, 1)      | float     | real        | --p_min           |
| p_max_all        | (Nx, Ny, Nz)       | float     | real        | --p_max_all       |
| p_min_all        | (Nx, Ny, Nz)       | float     | real        | --p_min_all       |
| p_final          | (Nx, Ny, Nz)       | float     | real        | --p_final         |
| ux               | (Nsens, Nt-s+1, 1) | float     | real        | -u or --u_raw     |
| uy               | (Nsens, Nt-s+1, 1) | float     | real        | -u or --u_raw     |
| uz               | (Nsens, Nt-s+1, 1) | float     | real        | -u or --u_raw     |
| ux_non_staggered | (Nsens, Nt-s+1, 1) | float     | real        | --u_non_staggered |
| uy_non_staggered | (Nsens, Nt-s+1, 1) | float     | real        | --u_non_staggered |
| uz_non_staggered | (Nsens, Nt-s+1, 1) | float     | real        | --u_non_staggered |
| ux_rms           | (Nsens, 1, 1)      | float     | real        | --u_rms           |
| uy_rms           | (Nsens, 1, 1)      | float     | real        | --u_rms           |
| uz_rms           | (Nsens, 1, 1)      | float     | real        | --u_rms           |
| ux_max           | (Nsens, 1, 1)      | float     | real        | --u_max           |
| uy_max           | (Nsens, 1, 1)      | float     | real        | --u_max           |
| uz_max           | (Nsens, 1, 1)      | float     | real        | --u_max           |
| ux_min           | (Nsens, 1, 1)      | float     | real        | --u_min           |
| uy_min           | (Nsens, 1, 1)      | float     | real        | --u_min           |
| uz_min           | (Nsens, 1, 1)      | float     | real        | --u_min           |
| ux_max_all       | (Nx, Ny, Nz)       | float     | real        | --u_max_all       |
| uy_max_all       | (Nx, Ny, Nz)       | float     | real        | --u_max_all       |
| uz_max_all       | (Nx, Ny, Nz)       | float     | real        | --u_max_all       |
| ux_min_all       | (Nx, Ny, Nz)       | float     | real        | --u_min_all       |
| uy_min_all       | (Nx, Ny, Nz)       | float     | real        | --u_min_all       |
| uz_min_all       | (Nx, Ny, Nz)       | float     | real        | --u_min_all       |
| ux_final         | (Nx, Ny, Nz)       | float     | real        | --u_final         |
| uy_final         | (Nx, Ny, Nz)       | float     | real        | --u_final         |
| uz_final         | (Nx, Ny, Nz)       | float     | real        | --u_final         |

5.2 Opposing Cuboid Corners Sensor Mask (defined if sensor_mask_type = 1) (implemented = False)

Note, each output group (e.g., /p) contains a dataset for each cuboid defined in
sensor_mask_corners, where /1 indicates the first dataset, /2 indicates the second
dataset, and so on up to Ncubes.

| Name               | Size (Nx, Ny, Nz)    | Data Type | Domain Type | Conditions            |
| ------------------ | -------------------- | --------- | ----------- | --------------------- |
| p/1                | (Cx, Cy, Cz, Nt-s+1) | float     | real        | -p or --p_raw         |
| p_rms/1            | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --p_rms               |
| p_max/1            | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --p_max               |
| p_min/1            | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --p_min               |
| p_max_all          | (Nx, Ny, Nz)         | float     | real        | --p_max_all           |
| p_min_all          | (Nx, Ny, Nz)         | float     | real        | --p_min_all           |
| p_final            | (Nx, Ny, Nz)         | float     | real        | --p_final             |
| ux/1               | (Cx, Cy, Cz, Nt-s+1) | float     | real        | -u or--u_raw          |
| uy/1               | (Cx, Cy, Cz, Nt-s+1) | float     | real        | -u or--u_raw          |
| uz/1               | (Cx, Cy, Cz, Nt-s+1) | float     | rea         | -u or--u_raw          |
| ux_non_staggered/1 | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_non_staggered_raw |
| uy_non_staggered/1 | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_non_staggered_raw |
| uz_non_staggered/1 | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_non_staggered_raw |
| ux_rms/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_rms               |
| uy_rms/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_rms               |
| uz_rms/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_rms               |
| ux_max/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_max               |
| uy_max/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_max               |
| uz_max/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_max               |
| ux_min/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_min               |
| uy_min/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_min               |
| uz_min/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_min               |
| ux_max_all         | (Nx, Ny, Nz)         | float     | real        | --u_max_all           |
| uy_max_all         | (Nx, Ny, Nz)         | float     | real        | --u_max_all           |
| uz_max_all         | (Nx, Ny, Nz)         | float     | real        | --u_max_all           |
| ux_min_all         | (Nx, Ny, Nz)         | float     | real        | --u_min_all           |
| uy_min_all         | (Nx, Ny, Nz)         | float     | real        | --u_min_all           |
| uz_min_all         | (Nx, Ny, Nz)         | float     | real        | --u_min_all           |
| ux_final           | (Nx, Ny, Nz)         | float     | real        | --u_final             |
| uy_final           | (Nx, Ny, Nz)         | float     | real        | --u_final             |
| uz_final           | (Nx, Ny, Nz)         | float     | real        | --u_final             |
