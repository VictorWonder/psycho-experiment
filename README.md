# 安装说明

## Window

建议安装`Python3.7`及以上版本，但不建议安装最新版。

程序运行需要通过命令提示符运行，命令提示符（命令行）可通过`win+R`键打开`运行`程序，再输入`cmd`打开。打开之后，可通过`cd`指令移动到代码所在目录。

运行程序前，建议通过`Python -m venv ENV_DIR`命令创建虚拟环境，其中，ENV_DIR是为配置虚拟环境指定的文件目录。创建好虚拟环境之后，运行`ENV_DIR\Scripts\Activate.bat`程序开启虚拟环境。

开启虚拟环境后，需要使用指令`pip install -r requirements.txt`安装依赖库，如果安装失败，可以复制错误信息到Google或者StackOverflow搜索解决方案，不建议百度搜索解决方案，不要轻易使用CSDN等中文博客提供的解决方法。

## Linux

安装好python之后，通过`pip install -r requirements.txt`安装依赖库，如果安装失败，请同样到Google或者StackOverflow搜索解决方案。

## Mac

安装好python之后，通过`pip install -r requirements.txt`安装依赖库，如果安装失败，请同样到Google或者StackOverflow搜索解决方案。

# 程序运行

切换到`src/`目录下，输入`python main.py`运行程序。

(1) 可选指令`--config=PATH`，用于指定实验的配置文件，默认为同目录下的`config.yml`文件

(2) 可选指令`-m`或`--modify`，表示需要手动调整实验配置，调整后会自动保存。
