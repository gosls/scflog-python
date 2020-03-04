# -*- coding:utf-8 -*-
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup
from codecs import open
from os import path

# LONG_DESCRIPTION为项目详细介绍，这里取README.md作为介绍
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# 具体的设置
setup(
    name="scflog",
    version='0.0.5',
    description="一款可以实时查看腾讯云SCF Python Runtime日志的工具",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

    ],
    # 指定控制台命令
    entry_points={
        'console_scripts': [
            'scflog = scflog.cmds:ScfPythonLogs'
        ],
    },
    keywords="scf, python, logs, scflogs",
    author="anycodes",
    author_email="service@52exe.cn",
    url="https://github.com/gosls/PythonLogsCli",
    license="Apache License 2.0",
    packages=["scflog"],
    install_requires=["plumbum", "ws4py"],  # 依赖的第三方包
    include_package_data=True,
    zip_safe=True,
)
