# This file is for user convenience only and is not used by the model
# Changes to this file will be ignored and overwritten
# Changes to the environment should be made in env_mach_specific.xml
# Run ./case.setup --reset to regenerate this file
source /glade/u/apps/ch/opt/lmod/7.5.3/lmod/lmod/init/sh
module purge 
module load ncarenv/1.2 intel/19.0.2 esmf_libs mkl esmf-7.1.0r-defio-mpi-O mpt/2.19 netcdf-mpi/4.6.1 pnetcdf/1.11.0 ncarcompilers/0.4.1
export OMP_STACKSIZE=256M
export TMPDIR=/glade/scratch/djk2120
export MPI_TYPE_DEPTH=16
export MPI_IB_CONGESTED=1
export MPI_USE_ARRAY=None
export TMPDIR=/glade/scratch/djk2120
export MPI_USE_ARRAY=false