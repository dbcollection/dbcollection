# Only need to change these two variables
PKG_NAME=dbcollection
USER=farrajota

OS=$TRAVIS_OS_NAME-64
mkdir ~/conda-bld
conda config --set anaconda_upload no
export CONDA_BLD_PATH=~/conda-bld
conda build conda-recipe --quit
anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME*.tar.bz2 --force

# Note:
# CONDA_UPLOAD_TOKEN expires in 2018/06/05