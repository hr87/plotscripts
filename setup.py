from distutils.core import setup

setup(
    name='plotsscripts',
    version='0.1',
    packages=['plotscripts',
              'plotscripts.data',
              'plotscripts.base',
              'plotscripts.table',
              'plotscripts.plotter',
              'plotscripts.plotter.svg',
              'plotscripts.plotter.latex',
              'plotscripts.plotter.matplotlib',
              'plotscripts.plotter.util',
              'plotscripts.geometry',
              'plotscripts.geometry.vhtrc',
              'plotscripts.geometry.hexagonal',
              'plotscripts.geometry.rectangular'
              ],
    url='hpcgitlab.inl.gov/hammhans/plotscripts',
    license='',
    author='Hans R Hammer',
    author_email='hans.hammer@tamu.edu',
    description='Package for advance cross section and geometry plotting',
    requires=['numpy', 'matplotlib']
)
