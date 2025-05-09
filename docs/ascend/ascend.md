# OpenRLHF x Ascend

我们在 OpenRLHF 上增加对华为昇腾设备的支持。**本代码仓由社区进行维护更新，不进行任何商业交付。**

## 硬件支持

* Atlas 800T A2

## 安装

### 配套版本

**下表提供昇腾配套软件版本仅为建议，不作为任何商业交付承诺**。

<table>
  <tr>
    <th align="left">OpenRLHF 主仓Tag</th>
    <td>v0.6.2</td>
  </tr>
  <tr>
    <th align="left">对应的 OpenRLHF NPU 适配分支</th>
    <td>main</td>
  </tr>
  <tr>
    <th align="left">vLLM 版本</th>
    <td>v0.7.3</td>
  </tr>
  <tr>
    <th align="left">vLLM Ascend 版本/分支</th>
    <td>v0.7.3</td>
  </tr>
  <tr>
    <th align="left">torch npu 版本 (pip install 安装)</th>
    <td>2.5.1</td>
  </tr>
  <tr>
    <th align="left">CANN 版本 (参考vllm-ascend)</th>
    <td><a href="https://github.com/vllm-project/vllm-ascend/blob/v0.7.3/docs/source/installation.md?plain=1#L72-L96">CANN 8.1.RC1</a></td>
  </tr>
  <tr>
    <th align="left">不支持功能</th>
    <td>Ring Attention</br>Hybrid Engine</br>Pytorch Compile</br>bitsandbytes</td>
  </tr>
</table>

### vLLM

为了保证能够在 OpenRLHF 上正常使用 vLLM，需要安装 vLLM Ascend 插件（`vllm-ascend`）。vLLM Ascend 插件的安装方式和镜像请参考[安装教程](https://vllm-ascend.readthedocs.io/en/latest/installation.html)。

```shell
git clone -b v0.7.3 https://github.com/vllm-project/vllm.git
cd vllm
pip install -r requirements-build.txt
VLLM_TARGET_DEVICE=empty pip install .

git clone -b v0.7.3 https://github.com/vllm-project/vllm-ascend.git
cd vllm-ascend
pip install -e .
```

### 源码安装

```shell
git clone https://github.com/zhuo97/OpenRLHF.git
cd OpenRLHF
TARGET_DEVICE=NPU pip install -e .
```

### Transformers

当前在 Ascend NPU 进行使用时，可能存在 CPU Memory 不足的情况。该问题已经修复（[PR](https://github.com/huggingface/transformers/pull/37698)），但是 transformers `4.51.4` 版本尚未发布。因此，如果在使用过程中遇到该问题，可以源码编译安装 transformers 库。当 transformers `4.51.4` 版本发布后，我们会第一时间更新 Ascend NPU 的 requirements。

### Ray

可通过如下方式在华为昇腾设备上启动 Ray:
```shell
# launch the master node of ray in container
ray start --head --port 6379

# if you want to launch ray on more nodes, use
ray start --address='MASTER-NODE-ADDRESS:6379'
```

训练脚本提交方式与英伟达 GPU 相同。

### 其他第三方库说明

| 软件            | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| flash_attn      | 原生不支持，通过在 transformers 适配昇腾FA算子进行支持（[PR](https://github.com/huggingface/transformers/pull/36696)）。 |
| ring_flash_attn | 原生不支持。                                                 |
| bitsandbytes    | 原生不支持。                                                 |

## 支持的算法

### 精度对比

根据经验，我们期望在相同配置下，在华为昇腾设备上的 Loss 与英伟达 GPU 的 Loss/Reward 平均绝对误差小于 2%，具体计算方式如下：

```math
Mean Error=\frac{\sum^N_{i=1}|loss_i^{npu}-loss_i^{gpu}|}{N}\times 100 \%
```

其中，N 表示训练的步数。更多信息请参考[精度计算说明](https://www.hiascend.com/document/detail/zh/Pytorch/600/ptmoddevg/trainingmigrguide/LMaccuracy_0001.html)。

### 进展

已支持的算法仅在下表提供的版本进行过测试。

| 算法        | 进展       | 与GPU误差 | torch 版本 | torch_npu 版本 | CANN 版本 | 详细结果                                                     |
| ----------- | ---------- | --------- | ---------- | -------------- | --------- | ------------------------------------------------------------ |
| SFT         | 已支持     | 0.19%     | 2.3.1      | 2.3.1.post2    | 8.0.RC3   | [测试结果](https://github.com/OpenRLHF/OpenRLHF/pull/605#issuecomment-2567488539) |
| DPO         | 已支持     | 1.81%     | 2.3.1      | 2.3.1.post2    | 8.0.RC3   | [测试结果](https://github.com/OpenRLHF/OpenRLHF/pull/605#issuecomment-2735122006) |
| KTO         | 已支持     | 0.37%     | 2.3.1      | 2.3.1.post2    | 8.0.RC3   | [测试结果](https://github.com/OpenRLHF/OpenRLHF/pull/605#issuecomment-2642104300) |
| RM          | 已支持     | 0.85%     | 2.3.1      | 2.3.1.post2    | 8.0.RC3   | [测试结果](https://github.com/OpenRLHF/OpenRLHF/pull/605#issuecomment-2642104300) |
| PRM         | 已支持     | 1.61%     | 2.3.1      | 2.3.1.post2    | 8.0.RC3   | [测试结果](https://github.com/OpenRLHF/OpenRLHF/pull/605#issuecomment-2642104300) |
| PPO         | 精度测试中 |           | 2.5.1      | 2.5.1          | 8.1.RC1   |                                                              |
| REINFORCE++ | 已支持     | 1.94%     | 2.5.1      | 2.5.1          | 8.1.RC1   | [测试结果](https://github.com/OpenRLHF/OpenRLHF/pull/605#issuecomment-2735138695) |
| GRPO        | 已支持     | 0.61%     | 2.5.1      | 2.5.1          | 8.1.RC1   | [测试结果](https://github.com/OpenRLHF/OpenRLHF/pull/605#issuecomment-2764993841) |

## 常见问题

* 使用 `--adam_offload` 参数可能存在长时间卡顿的情况，解决方法是删除 torch_extensions 的缓存文件，参考 [issue](https://github.com/deepspeedai/DeepSpeed/issues/2816#issuecomment-1450095538)。  

## 贡献者

[zhuo97](https://github.com/zhuo97), [zheliuyu](https://github.com/zheliuyu), [FightingZhen](https://github.com/FightingZhen), [obj12](https://github.com/obj12), [tongtong0613](https://github.com/tongtong0613), [Keilo001](https://github.com/Keilo001), [Tonyztj](https://github.com/Tonyztj), [ji-huazhong](https://github.com/ji-huazhong)
