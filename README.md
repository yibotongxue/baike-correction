# 大百科校正文本

本项目实现了大百科校正文本的切分部分，主要实现了语义切分，按句子切分，相邻的语义相近的合并为同一个主题。也可以直接使用划分的句子，而不根据语义合并。计划支持关键字识别主题。

## 安装依赖

本项目使用 `uv` 管理依赖，可以使用如下命令安装 `uv`

```bash
pip install uv
```

然后运行如下命令安装依赖

```bash
uv sync
```

## 运行

使用如下命令运行切分

```bash
uv run -m baike_correction.splitter --config ./configs/config.yaml --input <待切份文件> --output <输出文件>
```

比如如果待切分文件是 `./input.txt` ，输出文件是 `./output.txt` ，则运行命令

```bash
uv run -m baike_correction.splitter --config ./configs/config.yaml --input ./input.txt --output ./output.txt
```

可以通过修改 `./configs/config.yaml` 实现其他的切分方法。
