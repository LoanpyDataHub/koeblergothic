from setuptools import setup


setup(
    name='cldfbench_koeblergothic',
    py_modules=['cldfbench_koeblergothic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'koeblergothic=cldfbench_koeblergothic:Dataset',
        ],
        'cldfbench.commands': ['koeblergothic=koeblergothiccommands']
    },
    install_requires=[
        'cldfbench>=1.13.0', 'pylexibank>=3.4.0', 'epitran>=1.24',
        'pysem>=0.6.0', 'spacy>=3.5.1', "tqdm<=4.65.0", "lingpy<=2.6.9"
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
