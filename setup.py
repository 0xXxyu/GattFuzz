from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fp:
    description = fp.read()

setup(
    name='gattfuzz',
    version='0.0.10',
    description= "A tool for fuzzing BLE GATT",
    long_description=description,
    packages=find_packages(),
    #packages=['gattfuzz'],
    zip_safe=False,
    install_requires=[
        'bluepy==1.3.0',
        'scapy==2.4.5',
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'gattfuzz=gattfuzz.GattFuzz:main',
        ]
    }
)
