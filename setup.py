from distutils.core import setup

setup(
    name='Traffic Gym',
    version='0.1',
    packages=['gym_traffic',],
    license='GNU GPLv3',
    long_description=open('README.txt').read(),
)



# used packages

python -m pip install keyboard
pip install pytorch
pip install tensorboardX
pip install matplotlib
pip install numpy
pip install arcade
