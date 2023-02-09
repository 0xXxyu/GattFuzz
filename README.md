# GattFuzz

### 环境
Linux

### Requirements
Bluepy、scapy

### 功能描述

#### 支持两种方式：

1. 基于抓到的数据包进行pyload变异，具体变异规则待述；
2. 没有数据包的情况下支持随机数Fuzz。

#### 预期结果：

当检测到目标设备结束广播、断连会push error，可进一步人工核实目标设备状态，重放pyload

### Update

#### 2023.2.8 update
1. add new pyload
2. add device status scan

#### 2022.7.19 update
abstract functional class
