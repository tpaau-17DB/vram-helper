from setuptools import setup

setup(
    name='vram_helper',
    version='1.0.1',
    author_email='mikolaj_archusr@tutamail.com',
    description='Little python script that displays warnings when VRAM exceeds specified limit. Useful when doing some VRAM-intensive tasks on low-end devices (nvidia gpus only).',
    url='https://github.com/tpaau-17DB/vram-helper.git',
    packages=['vram_helper'],
    install_requires=[]
)
