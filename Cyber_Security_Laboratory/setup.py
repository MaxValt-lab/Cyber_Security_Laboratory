from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read().strip()

setup(
    name="cyber-security-laboratory",
    version=version,
    author="Олег Журавлёв",
    author_email="skrusich2000@gmail.com",
    description="Интеллектуальная система безопасности нового поколения",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaxValt-lab/Cyber_Security_Laboratory",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "opencv-python>=4.5.3",
        "tensorflow>=2.6.0",
        "torch>=1.9.0",
        "pillow>=8.3.1",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "cryptography>=3.4.7",
        "pydantic>=1.8.2",
    ],
)