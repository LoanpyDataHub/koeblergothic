from setuptools import setup


setup(
    name='cldfbench_koeblergothic',
    py_modules=['cldfbench_koeblergothic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'koeblergothic=cldfbench_koeblergothic:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
