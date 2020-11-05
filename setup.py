import setuptools

description='''Routing and wavelength assignment simulator over WDM networks

More information on https://rwa-wdm.readthedocs.io/en/latest/index.html
'''

setuptools.setup(
    name='rwa_wdm',
    version='0.2.2',
    license='GPL',
    author='Cassio Batista',
    author_email='cassiotb@ufpa.br',
    description='Routing and wavelength assignment simulator over WDM networks',
    long_description=description.strip(),
    url='https://github.com/cassiobatista/rwa-wdm-sim',
    packages=setuptools.find_packages(),
    install_requires=['argcomplete', 'networkx', 'numpy', 'matplotlib'],
    python_requires='>=3.7'
)
