import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='register-emoji',
        author='Yakov Nesterov',
        author_email='pixy2001@gmail.com',
        url='https://github.com/zaltoprofen/register-emoji',
        version='0.1.1',
        packages=setuptools.find_packages(),
        install_requires=[
            'selenium',
            'toml',
        ],
        entry_points={
            'console_scripts': [
                'register-emoji = register_emoji.main:main'
            ]
        }
    )
