from setuptools import find_packages, setup

setup(
    name="runeseal-core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "passlib[argon2]",
        "python-jose",
        "cryptography",
        "python-dotenv",
    ],
)
