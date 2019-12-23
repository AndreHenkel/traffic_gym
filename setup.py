from setuptools import setup

setup(name='gym_traffic',
      version='0.0.1',
      package_data = {
        'gym_traffic': ['envs/img/*.png'],
      },
      install_requires=['gym==0.12.1',
                        'pyglet==1.4.0b1',
                        'arcade==1.3.7',
                        'keyboard',
                        'numpy'],  # And any other dependencies foo needs
)
