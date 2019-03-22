from setuptools import setup

setup(name='gym_traffic',
      version='0.0.1',
      package_data = {
        'gym_traffic': ['envs/img/*.png'],
      },
      install_requires=['gym',
                        'arcade',
                        'keyboard',
                        'numpy',
                        'matplotlib'],  # And any other dependencies foo needs
)
