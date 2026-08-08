# 默认配置

SECRET_KEY = 'change-me-in-production'

# API 认证：key:secret 对列表
# 格式: "key1:secret1,key2:secret2"
# 从环境变量 VILLY_API_KEYS 读取，默认值仅用于开发
import os
API_KEYS = {}
_raw = os.environ.get('VILLY_API_KEYS', 'dev:dev-secret-do-not-use-in-production')
for pair in _raw.split(','):
    if ':' in pair:
        k, s = pair.split(':', 1)
        API_KEYS[k.strip()] = s.strip()

# 签名时间窗口（秒），允许时钟偏差
SIGNATURE_WINDOW = 300

# Nonce 缓存大小
NONCE_CACHE_SIZE = 10000
