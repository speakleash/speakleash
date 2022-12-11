import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speakleash",
    version="0.0.8",
    author="SpeakLeash Team",
    author_email="team@speakleash.org",
    description="SpeakLeash agnostic dataset for Polish",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/speakleash/speakleash",
    packages = ["speakleash"],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'tqdm',
        'lm_dataformat'
    ]
)
