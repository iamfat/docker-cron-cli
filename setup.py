from setuptools import setup

setup(
    name='docker-cron',

    version='0.1.1',

    description='Docker Cron',

    url='https://github.com/iamfat/docker-cron',

    author="Jia Huang",
    author_email="iamfat@gmail.com",

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
    ],

    keywords='docker cron crontab',

    packages=['docker_cron'],

    install_requires=["python-crontab"],

    entry_points={
        'console_scripts': [
            'docker-cron=docker_cron:main',
        ],
    },
)
