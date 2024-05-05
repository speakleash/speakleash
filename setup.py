from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="speakleash",
    version="0.3.5",
    author="SpeakLeash Team",
    author_email="team@speakleash.org",
    description="SpeakLeash agnostic dataset for Polish",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/speakleash/speakleash",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'tqdm',
        'lm_dataformat'
    ],
    package_data={
        'speakleash': ['config.json', 'config_loader.py']
    }
)
