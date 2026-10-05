# Home Assistant 部署与智能家居接入

**这份文档解决什么**:在一台 Proxmox VE 虚拟机上,用 Docker 部署 Home Assistant,接入美的空调与南方电网电费,并让家人从外网访问。

**怎么用这份文档**

| 你现在的处境 | 看哪一节 |
|---|---|
| 我要从头做一遍 | [快速开始](#快速开始) |
| 我卡在某个报错上 | [排错索引](#排错索引) |
| 我要加新设备 | [设备接入](#设备接入) |
| 我要从外网访问 | [外网访问](#外网访问) |
| 我要知道哪些地方会踩坑 | [踩坑总结](#踩坑总结) |

**环境**:Proxmox VE 宿主机 + Rocky 9 虚拟机 + Docker
**验证时间**:2026-10-05 ~ 10-06(全部步骤实际执行过)

> **关于占位符**
>
> 本文中的 `<公网IP>`、`<HA虚拟机IP>`、`<缴费号>` 是脱敏后的占位符,请替换成你自己的值:
>
> | 占位符 | 替换为 |
> |---|---|
> | `<公网IP>` | 你云服务器的公网 IP |
> | `<HA虚拟机IP>` | HA 所在虚拟机的内网 IP |
> | `<缴费号>` | 南方电网的缴费户号(12 位) |


---

## 架构

```
公网
 │  http://<公网IP>:8123
 ↓
云服务器(阿里云)          ← frps 服务端 + 防火墙放行 8123
 │  frp 隧道
 ↓
PVE 宿主机                ← frpc 客户端(systemctl 管理)
 │  转发到内网 <HA虚拟机IP>
 ↓
虚拟机 Rocky 9
 ├── Docker: Home Assistant (:8123, --network=host)
 └── Docker: Cloudreve     (:5212)
```

**两个关键设计决定:**

- **frpc 装在 PVE 宿主机,不是装在 HA 虚拟机里。** 因为宿主机能访问整个内网,以后加别的服务不用重新配置隧道。
- **HA 用 `--network=host`。** 它靠广播发现设备,桥接网络会失效。

---

## 快速开始

从零到能打开 HA 界面,大约 20 分钟。

### 1. 启动 HA 容器

```bash
mkdir -p /opt/homeassistant/config

docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v /opt/homeassistant/config:/config \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
```

**这三个参数不能省:**

| 参数 | 为什么必须 |
|---|---|
| `--privileged` | 允许访问硬件(蓝牙 / USB 网关) |
| `--network=host` | **HA 靠广播发现设备,桥接网络会发现不到** |
| `-v .../config:/config` | 配置持久化,否则容器一删全没 |

### 2. 放行防火墙

```bash
firewall-cmd --add-port=8123/tcp --permanent
firewall-cmd --reload
```

**不做的后果**:浏览器打不开,你会以为是容器没起来。

### 3. 打开并初始化

浏览器访问 `http://<HA虚拟机IP>:8123`,创建管理员账号,时区选 `Asia/Shanghai`。

**开头就把密码设强。** 后面要暴露到公网,弱密码等于把家里设备交出去。

### 4. 装 HACS

HACS 是社区集成商店,**HA 官方版不带,必须手动装**。

```bash
cd /tmp
wget https://github.com/hacs/integration/releases/latest/download/hacs.zip

mkdir -p /opt/homeassistant/config/custom_components/hacs
unzip -o /tmp/hacs.zip -d /opt/homeassistant/config/custom_components/hacs

docker restart homeassistant
```

**验证装对了**:这个文件必须存在——

```bash
ls /opt/homeassistant/config/custom_components/hacs/manifest.json
```

**没有这个文件 = 解压多套了一层目录。** 这是最常见的手动安装错误。

然后在 HA 里:设置 → 设备与服务 → 添加集成 → 搜 `HACS` → 授权 GitHub。免责声明 4 项全勾。

---

## 设备接入

### 通用规律

| 设备生态 | 用什么集成 |
|---|---|
| 米家 / 小米 | `Xiaomi Miot Auto` |
| 美的 | `Midea Auto Cloud` |
| 涂鸦 Tuya | `LocalTuya` |
| Zigbee 传感器 | Zigbee2MQTT / ZHA + USB 网关 |
| **只有红外遥控的设备** | 红外发射器(Broadlink RM4 约 60~90 元) |

> **红外是万能兜底方案。** 任何"协议搞不定、账号连不上"的设备,只要能红外遥控,用红外发射器可以直接绕过全部云服务问题。

### 美的空调

**结论:用 `Midea Auto Cloud`,不要在 `Midea AC LAN` 上耗时间。**

`Midea AC LAN` 走"局域网发现 + 美的云取 Token",但它的 App 选项里只有国际版(MSmartHome、Midea Air 等),**没有中国区的"美的美居"**。用中国区账号连国际云,必然报 `3102 账号不存在`。

**接入步骤:**

1. HACS → 集成 → 搜 `Midea Auto Cloud` → 下载
2. `docker restart homeassistant`
3. HA → 设置 → 设备与服务 → 添加集成 → 搜 `Midea Auto Cloud`
4. **选你实际用的 App**(国内用户选"美的美居"对应项)——**这一步选错就是 3102**
5. 输入手机号 + 密码 → 自动拉取设备 → 勾选空调

**接入成功后立刻备份配置文件。** 美的在逐步关闭 Token API,备份了以后重装不用再登录:

```bash
find /opt/homeassistant/config -name "*.json" | grep -i midea
```

把找到的文件复制到 HA 之外的地方。

### 南方电网电费

**用 `chuyu5762/HA-grid-south` 这个 fork,不要用原版 `CubicPill/china_southern_power_grid_stat`。**

原因:原版 v1.2.0 的 `config_flow.py` 有 bug——**点集成的齿轮(选项配置)会报 `500 Internal Server Error`**。fork 版修了这个问题。

**手动安装**(HACS 下载 GitHub 容易超时):

```bash
cd /tmp
wget https://github.com/chuyu5762/HA-grid-south/archive/refs/heads/master.zip
unzip master.zip

# 先确认目录结构对不对
ls HA-grid-south-master/custom_components/

# 删旧版,放新版
rm -rf /opt/homeassistant/config/custom_components/china_southern_power_grid_stat
mv /tmp/HA-grid-south-master/custom_components/china_southern_power_grid_stat \
   /opt/homeassistant/config/custom_components/

docker restart homeassistant
```

> **路径注意**:Docker 版 HA 是 `/opt/homeassistant/config/custom_components`,不是 HA OS 的 `/homeassistant/custom_components`。

**配置**:HA → 设置 → 设备与服务 → 添加集成 → 搜 `China Southern Power Grid` → 输入南网账号密码 → **选"添加已绑定的缴费号"** → 选对户号。

#### ⚠️ 两个最容易误判的坑

**坑 1:选错缴费号**

一个南网账号下可能有多个缴费号(多套房、老家、出租房)。

**如果 HA 数据和南网 App 对不上,第一件事是核对缴费号。** 真实案例:账号下有 2 个户号,先加了错的,HA 显示上月用电 16 度,实际是 2726 度。

**这个坑最容易误判成"集成坏了",其实只是选错了户号。**

**坑 2:"账单口径"和"实际口径"混淆**

这个集成有两组"本年"数据,数字不一样:

| 实体 | 口径 | 用哪个 |
|---|---|---|
| `this_year_bill_cost` / `this_year_bill_usage` | **账单口径**(已出账单) | ✅ **用这个** |
| `this_year_total_cost` / `this_year_total_usage` | 实际口径(含当月未出账) | 不显示,避免混淆 |

**南方电网 App 显示的是账单口径。** HA 里也用账单口径,数字才能对上。

#### 实体清单

实体 ID 前缀是 `sensor.csgaccount_<缴费号>_`

| 后缀 | 含义 |
|---|---|
| `account_balance` | 账户余额 |
| `arrears` | 欠费金额 |
| `this_month_cost` / `this_month_usage` | 本月电费 / 用电量 |
| `this_year_bill_cost` / `this_year_bill_usage` | **本年账单费用 / 用量** ⭐ |
| `last_month_cost` / `last_month_usage` | 上月 |
| `last_year_cost` / `last_year_usage` | 去年 |
| `yesterday_usage` / `latest_day_usage` | 昨日 / 最近一日用电量 |
| `current_ladder_tariff` / `current_ladder_stage` | 阶梯电价 / 当前阶梯 |

#### 仪表盘配置

HA → 概览 → 右上角编辑 → 原始配置编辑器,粘贴下面内容(**把缴费号换成你自己的**):

```yaml
views:
  - title: 电费
    path: dianfei
    icon: mdi:lightning-bolt
    cards:
      - type: heading
        heading: 账户
        heading_style: title
      - type: grid
        columns: 2
        square: false
        cards:
          - type: tile
            entity: sensor.csgaccount_<缴费号>_account_balance
            name: 账户余额
            icon: mdi:wallet
          - type: tile
            entity: sensor.csgaccount_<缴费号>_arrears
            name: 欠费金额
            icon: mdi:alert-circle

      - type: heading
        heading: 本期用电
        heading_style: title
      - type: grid
        columns: 2
        square: false
        cards:
          - type: tile
            entity: sensor.csgaccount_<缴费号>_this_month_cost
            name: 本月电费
            icon: mdi:currency-cny
          - type: tile
            entity: sensor.csgaccount_<缴费号>_this_month_usage
            name: 本月用电量
            icon: mdi:lightning-bolt
          - type: tile
            entity: sensor.csgaccount_<缴费号>_this_year_bill_cost
            name: 本年电费
            icon: mdi:currency-cny
          - type: tile
            entity: sensor.csgaccount_<缴费号>_this_year_bill_usage
            name: 本年用电量
            icon: mdi:lightning-bolt

      - type: heading
        heading: 近期用电
        heading_style: title
      - type: grid
        columns: 2
        square: false
        cards:
          - type: tile
            entity: sensor.csgaccount_<缴费号>_yesterday_usage
            name: 昨日用电量
            icon: mdi:lightning-bolt
          - type: tile
            entity: sensor.csgaccount_<缴费号>_latest_day_usage
            name: 最近一日用电量
            icon: mdi:lightning-bolt

      - type: heading
        heading: 往期对比
        heading_style: title
      - type: grid
        columns: 2
        square: false
        cards:
          - type: tile
            entity: sensor.csgaccount_<缴费号>_last_month_cost
            name: 上月电费
            icon: mdi:currency-cny
          - type: tile
            entity: sensor.csgaccount_<缴费号>_last_month_usage
            name: 上月用电量
            icon: mdi:lightning-bolt
          - type: tile
            entity: sensor.csgaccount_<缴费号>_last_year_cost
            name: 去年电费
            icon: mdi:currency-cny
          - type: tile
            entity: sensor.csgaccount_<缴费号>_last_year_usage
            name: 去年用电量
            icon: mdi:lightning-bolt
```

---

## 外网访问

### 为什么选 frp

需求是**给家人用**——不能要求每个家人都装客户端。

| 方案 | 结果 | 原因 |
|---|---|---|
| **frp** | ✅ 可用 | 纯 TCP 转发,不注入额外 HTTP 头 |
| Cloudflare Tunnel | ❌ 400 Bad Request | 注入 `X-Forwarded-For`,HA 需要 `trusted_proxies` 才接受 |
| Tailscale | 只适合自己用 | 家人得装客户端 |

### 配置

**在 PVE 宿主机的 `frpc.toml` 里加一条:**

```toml
[[proxies]]
name = "homeassistant"
type = "tcp"
localIP = "<HA虚拟机IP>"   # HA 虚拟机
localPort = 8123
remotePort = 8123
```

**重启 frpc,并在云服务器放行端口:**

```bash
# PVE 宿主机
systemctl restart frpc

# 云服务器
sudo firewall-cmd --zone=public --add-port=8123/tcp --permanent
sudo firewall-cmd --reload
```

> **阿里云还要另外配安全组。** 只配 `firewall-cmd` 不够,安全组不放行照样连不上。

**访问地址**:`http://<公网IP>:8123`

### 给家人配 App

1. 手机装官方 **Home Assistant** App
2. 服务器地址填 `http://<公网IP>:8123`
3. 用你分配的账号登录

### ⚠️ 安全提醒

**frp 方案是 HTTP 明文,没有 HTTPS。** 密码在传输中是明文的。而且风险不止密码:

- HA 现在**公网可访问**
- HA 能**控制家里设备**
- HA 里存着**南网账号、美的账号**

**也就是说,拿到 HA 的登录就等于拿到这些。**

**已经做的缓解:**

- [ ] HA 用强密码(不要和别处重复)
- [ ] 家人用独立账号,不要共用管理员

**可以考虑进一步加强:**

- 在云服务器的 8123 前面加一层 Nginx 做 basic auth
- 或改用 frp 的 `stcp` 类型(需要客户端,但更安全)

### 为什么 Cloudflare Tunnel 不行(记录一下,避免以后重复踩)

**现象:**

```
ERROR [homeassistant.components.http.forwarded] A request from a reverse proxy
was received from ::1, but your HTTP integration is not set-up for reverse proxies
```

**试过但无效的:**

- `configuration.yaml` 里加 `http: use_x_forwarded_for: true` + `trusted_proxies: [127.0.0.1, ::1]`
- 试过 `::ffff:127.0.0.1`、`0.0.0.0/0`、各内网段
- 注释掉 `default_config:`
- 重建容器(stop + rm + run)
- 确认配置文件路径正确(标记文件测试通过、`cat -A` 无隐藏字符)

**结论**:配置本身正确,但 HA 始终没加载该 http 配置,原因未查明(可能与 HA 版本对该配置的加载行为有关)。

**教训:遇到这种情况别死磕,换 frp 更省事。**

---

## 排错索引

按报错信息查。**这一节是这份文档最实用的部分。**

| 你看到的 | 原因 | 解决 |
|---|---|---|
| `exec /init: exec format error` | 拉错了架构的镜像(arm 而非 amd64) | 用官方全名 `ghcr.io/home-assistant/home-assistant:stable`;`docker inspect 镜像 \| grep architecture` 应为 `amd64` |
| 浏览器打不开 8123 | 防火墙没放行 | `firewall-cmd --add-port=8123/tcp --permanent && firewall-cmd --reload` |
| 拉镜像特别慢 | ghcr.io 国内慢 | 换 Docker Hub 的 `homeassistant/home-assistant:stable`(注意是下划线) |
| HACS 装了但 HA 里搜不到 | 解压多套了一层目录 | 确认 `custom_components/hacs/manifest.json` 存在 |
| 美的集成报 `3102 账号不存在` | App 选项选错,连了错误的云 | 换成"美的美居"对应项 |
| 美的集成报 `65027 用户在线登录设备已超过上限` | 账号在多台设备登录,超限 | 手机 App 里退出其他设备,或改密码强制下线 |
| 南网集成点齿轮报 `500` | 原版 `config_flow.py` 有 bug | 换 `chuyu5762/HA-grid-south` fork |
| 南网数据对不上 App | 选错了缴费号 | 核对户号,重新添加 |
| HACS 下载 GitHub 超时 | 网络问题 | 手动 `wget` 下载,解压到 `custom_components` |
| Cloudflare Tunnel 报 400 | `X-Forwarded-For` 注入 | 改用 frp |

> **一条排查经验**:美的从 `3102` 变成 `65027` 是**进步**,不是变糟。`3102` 说明 App 选项连错了云;能走到 `65027` 说明账号已被正确识别,只剩登录设备数的问题。**看懂报错的递进关系,比记住单个报错有用。**

---

## 踩坑总结

| # | 坑 | 教训 |
|---|---|---|
| 1 | 镜像架构错(`exec format error`) | 用官方全名镜像,确认 amd64 |
| 2 | 8123 打不开 | Rocky/Debian 默认防火墙要手动放行 |
| 3 | HACS 找不到 | HA 不自带,手动装(不要用失效的 `get.hacs.xyz` 脚本) |
| 4 | 美的 `3102` | App 选项选错,连了错误的云 |
| 5 | 美的 `65027` | 账号登录设备超限,退其他设备 |
| 6 | **美的集成选错** | `Midea AC LAN` 接不上,用 `Midea Auto Cloud` |
| 7 | 南网点齿轮 500 | 原版有 bug,换 fork |
| 8 | **南网数据对不上** | 多个缴费号,选错了 |
| 9 | 南网"账单"vs"实际"混淆 | 用账单口径实体,与 App 一致 |
| 10 | HACS 下载超时 | 手动 wget,放 `custom_components` |
| 11 | 智能家居协议复杂 | 账号区服、App 版本、云 API 关停都会影响接入 |
| 12 | **公网访问是明文 HTTP** | 用强密码;条件允许时加一层认证 |

---

## 常用命令

```bash
# 重启 HA
docker restart homeassistant

# 看日志(排查第一步)
docker logs homeassistant 2>&1 | tail -30

# 实时跟日志
docker logs -f homeassistant

# 配置目录
ls /opt/homeassistant/config/

# 确认 HACS 装对了
ls /opt/homeassistant/config/custom_components/hacs/manifest.json

# 备份美的设备配置
find /opt/homeassistant/config -name "*.json" | grep -i midea

# 重启 frp
systemctl restart frpc
```

---

## 待办

- [ ] **万和热水器**:如果设备绑在米家 App,可用 `Xiaomi Miot Auto` 接入。⚠️ 新版要求 HA ≥ 2025.6.0,先确认 HA 版本够新。
- [ ] **HA 加强访问认证**:在云服务器 8123 前加 Nginx basic auth,或改用 frp `stcp`。
- [ ] **给美的设备配置做定期备份**:美的在逐步关闭 Token API。

---

## 附:关键信息速查

| 项 | 值 |
|---|---|
| HA 访问地址(内网) | `http://<HA虚拟机IP>:8123` |
| HA 访问地址(公网) | `http://<公网IP>:8123` |
| HA 配置目录 | `/opt/homeassistant/config` |
| HA 容器名 | `homeassistant` |
| 云端需放行 | `8123/tcp`(firewall-cmd + 安全组) |
| frpc 位置 | PVE 宿主机 |
| frpc 配置 | `/opt/frp_0.68.1_linux_amd64/frpc.toml` |
