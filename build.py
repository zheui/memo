import PyInstaller.__main__
import shutil
import os

# 打包配置
APP_NAME = "柘记"
ICON_PATH = "app.ico"
ADD_DATA = [
    ("memo.ico", "."),  # (源文件, 目标目录)
]

def build():
    # 清理旧构建
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    # 基本参数
    args = [
        "memo.py",
        "--name", APP_NAME,
        "--icon", ICON_PATH,
        "--onefile",
        "--windowed",
        "--upx-dir", "upx-5.0.0-win64",
        "--exclude-module", "tkinter",
        "--exclude-module", "test",
        "--clean"
    ]

    # 处理附加数据
    for src, dest in ADD_DATA:
        args += ["--add-data", f"{src}{os.pathsep}{dest}"]

    # 执行打包
    PyInstaller.__main__.run(args)

    # 复制配置文件模板
    shutil.copy("memo.ico", f"dist/{APP_NAME}.ico")
    print("\nBuild completed! Check /dist directory")

if __name__ == "__main__":
    build()