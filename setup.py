from setuptools import setup, find_packages

setup(
    name='plotting',
    version='0.1.0',
    author='Ruben Doerfel',
    author_email='doerfelruben@aol.com',
    description='This is a high-level interface for plotting data for publications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RDoerfel/plotting',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='example package',
    python_requires='>=3.6',
    install_requires=[
        'matplotlib>=3.3.4',
        'seaborn>=0.11.1',
    ],
    extras_require={
        'dev': [
            'pytest',
            'coverage',
        ]
    },
    package_data={
        'plotting': ['bin/fonts/*'],
    },
    include_package_data=True,
)
