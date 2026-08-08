# HMAC 认证模块
#
# middleware.py: Flask before_request 中间件，拦截所有 API 请求进行签名验证
# signer.py:    HMAC-SHA256 签名生成与验证逻辑
