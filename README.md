
![Gattfuzz logo](./GATTFuzzing.jpg)

# GattFuzzing
GattFuzzing 是一款针对BLE Gatt的模糊测试工具。

### 环境
Linux

### Requirements
Bleak、Scapy

### 安装与使用
#### 方法一

```
pip install -r requirements.txt
python main.py
```

#### 方法二

```
python setup.py install
gattfuzz 
```

#### 方法三

```
pip install gattfuzz
gattfuzz
```

#### 使用
```
gattfuzz -h
```
支持两个参数，-f 和 -m，-f为可选。 -m为目标的mac地址。-f 就是你抓取到的pcap包，会根据包提取去进行变异fuzz。如果不指定，则直接遍历目标设备gatt，并进行fuzzing 测试。


### 功能描述

#### 支持两种方式：

1. 基于抓到的数据包进行payload变异，具体变异规则待述；
2. 没有数据包的情况下支持随机数Fuzz。


#### 预期结果：

当检测到目标设备结束广播、断连会push error，可进一步人工核实目标设备状态，重放payload

### 可能遇到的一些问题

目前支持手机hci log抓的pcap包（需要自己转格式）和抓取的空中包两种pcap包，其他的包解析出可能欢迎提issue

