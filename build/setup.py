from setuptools import find_namespace_packages, setup, find_packages

setup(
    name='neon-test-framework',
    version='1.3.0',
    description='Neon Core Framework',
    url='https://tfs.engineering.intelligentgaming.net/tfs/Neon-Collection/neon-test-automation',
    author='Neon',
    author_email='neon@playtech.com',
    packages=find_namespace_packages(exclude=["*env*", "*functional_tests*", "*performance_tests*", "*test_data_support*"]),
    classifiers=['Programming Language :: Python :: 3.10'],
)