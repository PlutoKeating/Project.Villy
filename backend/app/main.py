# Flask 入口
import os
from flask import Flask
from app.api import api_bp
from app.auth.middleware import require_hmac_auth

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), '..', 'config', 'default.py'))

    # HMAC 认证中间件
    app.before_request(require_hmac_auth)

    # 注册 API 蓝图
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
