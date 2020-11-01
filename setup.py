import setuptools

setuptools.setup(
    name='rwa_wdm',
    version='0.2',
    license='MIT',
    author='Cassio Batista',
    author_email='cassiotb@ufpa.br',
    description='Routing and wavelength assignment simulator over WDM networks',
    url='https://github.com/cassiobatista/rwa-wdm-sim',
    packages=setuptools.find_packages(),
    install_requires=['networkx', 'numpy', 'matplotlib'],
    python_requires='>=3.6'
)
