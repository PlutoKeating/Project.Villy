# HMAC-SHA256 认证方案

> 本文档设计 Project.Villy 的 API 认证体系，平衡安全性与 Allwinner R16 的硬件资源约束。

---

## 选型依据

| 方案 | CPU 开销 | 内存开销 | 防重放 | 防篡改 | 结论 |
|------|---------|---------|--------|--------|------|
| 无认证 | 零 | 零 | ❌ | ❌ | 不可接受 |
| API Key 明文 | 极低 | 低 | ❌ | ❌ | 易被截获 |
| JWT (HS256) | 中 | 中 | ⚠️ | ✅ | 需管理 token 生命周期 |
| JWT (RS256) | 高 | 高 | ⚠️ | ✅ | 非对称加密，R16 负担重 |
| **HMAC-SHA256 + Nonce** | 低 | 低 | ✅ | ✅ | **选定方案** |
| mTLS | 中 | 中 | ✅ | ✅ | 证书管理复杂 |

**决策：HMAC-SHA256 + Timestamp + Nonce**，基于 Python `hmac` 标准库实现，零外部依赖。

---

## 认证流程

```
Client                               Server
  │                                    │
  │ 1. 准备请求                         │
  │   method = "POST"                   │
  │   path   = "/api/v1/motors"         │
  │   body   = '{"left": 100, ...}'    │
  │   ts     = str(int(time()))         │
  │   nonce  = random_hex(16)           │
  │   body_hash = SHA256(body)          │
  │   msg    = method + path + ts      │
  │          + nonce + body_hash        │
  │   sig    = HMAC-SHA256(secret, msg) │
  │                                    │
  │ 2. 发送请求                         │
  │   Headers:                          │
  │     X-API-Key: <key>               │
  │     X-Timestamp: <ts>               │
  │     X-Nonce: <nonce>                │
  │     X-Signature: <sig>              │
  │   Body: <body>                      │
  │ ──────────────────────────────────> │
  │                                    │
  │                    3. 验证请求       │
  │                     • |now - ts| < 300s ?
  │                     • nonce 未使用过？
  │                     • key 存在且有效？
  │                     • 重新计算签名是否一致？
  │                                    │
  │                    4. 标记 nonce 已用 │
  │                    5. 执行请求        │
  │ <────────────────────────────────── │
  │                                    │
```

## 请求头规范

| 头名称 | 类型 | 说明 |
|--------|------|------|
| `X-API-Key` | string | API 密钥标识符（不参与签名，仅用于查找 secret） |
| `X-Timestamp` | integer | Unix 时间戳（秒），允许 ±5 分钟偏差 |
| `X-Nonce` | string(32) | 16 字节随机 hex，单次有效 |
| `X-Signature` | string(64) | HMAC-SHA256 签名 hex |

## 签名算法

```
signing_string = HTTP_METHOD + "\n"
               + REQUEST_PATH + "\n"
               + TIMESTAMP + "\n"
               + NONCE + "\n"
               + SHA256(REQUEST_BODY)

signature = HMAC-SHA256(API_SECRET, signing_string)
```

### 示例

```
method  = "POST"
path    = "/api/v1/motors"
ts      = "1754678423"
nonce   = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
body    = '{"left_motor": 50, "right_motor": 50}'

body_hash = SHA256(body)
          = "f8a9d3c2..."

signing_string = "POST\n/api/v1/motors\n1754678423\na1b2c3d4...\nf8a9d3c2..."

signature = HMAC-SHA256(secret_key, signing_string)
          = "7b3e91a2..."
```

## Nonce 管理

- Server 侧维护一个基于时间的 LRU 缓存
- Nonce 有效期 = Timestamp 窗口（300s）
- 过期 Nonce 自动清除
- 大约占用：`(请求频率/s × 300s) × 32 bytes` 内存
- 以 10 req/s 计：约 96KB，R16 完全可承受

## 密钥管理

- Server 侧从环境变量 `VILLY_API_KEYS` 读取，格式：`key1:secret1,key2:secret2`
- 支持多组 key/secret，实现细粒度权限控制（可选）
- 前端 dashboard 使用专用 key
- 开发者脚本可使用独立 key

## 前端实现

`frontend/src/lib/api.ts` 封装签名逻辑：

```typescript
async function signedFetch(path: string, options: RequestInit): Promise<Response> {
  const ts = Math.floor(Date.now() / 1000).toString();
  const nonce = crypto.randomUUID().replace(/-/g, '');
  const body = options.body?.toString() || '';
  const bodyHash = await sha256(body);
  const signingString = `${options.method}\n${path}\n${ts}\n${nonce}\n${bodyHash}`;
  const signature = await hmacSha256(API_SECRET, signingString);

  return fetch(path, {
    ...options,
    headers: {
      ...options.headers,
      'X-API-Key': API_KEY,
      'X-Timestamp': ts,
      'X-Nonce': nonce,
      'X-Signature': signature,
    },
  });
}
```

---

## 安全特性总结

| 威胁 | 防护 |
|------|------|
| 重放攻击 | Timestamp 窗口 + Nonce 一次性 |
| 请求篡改 | Body SHA-256 参与签名 |
| 密钥泄露 | 环境变量注入，不入库 |
| 暴力破解 | HMAC-SHA256 不可逆 |
| 中间人 | 建议生产环境启用 TLS（可选） |

---

*最后更新：2026-08-08*
