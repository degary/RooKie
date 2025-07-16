"""
钉钉回调基础处理器
"""
import hashlib
import hmac
import base64
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from django.http import HttpRequest, HttpResponse
from utils.logger import get_logger

logger = get_logger()

class BaseCallbackHandler(ABC):
    """钉钉回调处理器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.app_secret = config.get('app_secret') or config.get('client_secret')
        self.token = config.get('token')
        self.aes_key = config.get('aes_key')
    
    @property
    @abstractmethod
    def event_type(self) -> str:
        """事件类型"""
        pass
    
    @abstractmethod
    def handle(self, request: HttpRequest, data: Dict[str, Any]) -> HttpResponse:
        """处理回调事件"""
        pass
    
    def verify_signature(self, request: HttpRequest, nonce: str, timestamp: str, encrypt_msg: str) -> bool:
        """验证钉钉签名"""
        try:
            if not self.token:
                logger.warning("缺少token配置")
                return False
            
            # 按照钉钉规则计算签名
            sort_list = [self.token, timestamp, nonce, encrypt_msg]
            sort_list.sort()
            sha1 = hashlib.sha1()
            sha1.update(''.join(sort_list).encode('utf-8'))
            signature = sha1.hexdigest()
            
            return signature
            
        except Exception as e:
            logger.error(f"签名验证异常: {str(e)}")
            return False
    
    def decrypt_data(self, encrypt_msg: str) -> Optional[str]:
        """解密钉钉数据"""
        try:
            from Crypto.Cipher import AES
            import struct
            
            if not self.aes_key:
                logger.warning("缺少aes_key配置")
                return None
            
            # Base64解码
            encrypt_msg = base64.b64decode(encrypt_msg)
            
            # AES解密
            key = base64.b64decode(self.aes_key + '=')
            cipher = AES.new(key, AES.MODE_CBC, key[:16])
            decrypted = cipher.decrypt(encrypt_msg)
            
            # 去除padding
            pad = decrypted[-1]
            if isinstance(pad, str):
                pad = ord(pad)
            decrypted = decrypted[:-pad]
            
            # 提取数据
            msg_len = struct.unpack('!I', decrypted[16:20])[0]
            msg = decrypted[20:20+msg_len].decode('utf-8')

            logger.info(f"解密成功", msg=msg)
            
            return msg
            
        except Exception as e:
            logger.error(f"数据解密失败: {str(e)}")
            return None
    
    def dingtalk_response(self, message: str = "success") -> HttpResponse:
        """钉钉标准响应格式"""
        if not self.token or not self.aes_key:
            # 如果没有配置加密参数，返回简单响应
            return HttpResponse(
                json.dumps({"errcode": 0, "errmsg": "ok"}),
                content_type='application/json',
                status=200
            )
        
        # 使用加密响应
        encrypted_map = self._get_encrypted_map(message)
        return HttpResponse(
            json.dumps(encrypted_map),
            content_type='application/json',
            status=200
        )
    
    def _get_encrypted_map(self, contents: str) -> dict:
        """生成加密响应数据（参考DingCallbackCrypto3.getEncryptedMap）"""
        import time
        import random
        import string
        
        encrypt_content = self._encrypt(contents)
        timestamp = str(int(time.time()))
        nonce = self._generate_random_key(16)
        signature = self._generate_signature(nonce, timestamp, self.token, encrypt_content)
        
        return {
            'msg_signature': signature,
            'encrypt': encrypt_content,
            'timeStamp': timestamp,
            'nonce': nonce
        }
    
    def _encrypt(self, contents: str) -> str:
        """加密（参考DingCallbackCrypto3.encrypt）"""
        import struct
        import binascii
        import io
        from Crypto.Cipher import AES
        
        try:
            # 获取client_id作为key
            key = self.config.get('client_id')
            
            # 计算消息长度
            msg_len = struct.pack('>l', len(contents))

            # 组装数据：随机字符串 + 消息长度 + 消息 + key
            contents = ''.join([self._generate_random_key(16), msg_len.decode('latin-1'), contents, key])
            content_encode = self._pks7encode(contents)
            
            # AES加密
            aes_key = base64.b64decode(self.aes_key + '=')
            iv = aes_key[:16]
            aes_encode = AES.new(aes_key, AES.MODE_CBC, iv)
            aes_encrypt = aes_encode.encrypt(content_encode.encode('UTF-8'))
            return base64.encodebytes(aes_encrypt).decode('UTF-8')

            
        except Exception as e:
            logger.error(f"加密失败: {str(e)}")
            return contents
    
    def _generate_signature(self, nonce: str, timestamp: str, token: str, msg_encrypt: str) -> str:
        """生成签名（参考DingCallbackCrypto3.generateSignature）"""
        sign_list = ''.join(sorted([nonce, timestamp, token, msg_encrypt]))
        return hashlib.sha1(sign_list.encode()).hexdigest()
    
    def _pks7encode(self, content: str) -> str:
        """安装PKCS#7标准填充字符串（参考DingCallbackCrypto3.pks7encode）"""
        import binascii
        import io
        
        l = len(content)
        output = io.StringIO()
        val = 32 - (l % 32)
        for _ in range(val):
            output.write('%02x' % val)
        return content + binascii.unhexlify(output.getvalue()).decode('latin-1')
    
    def _generate_random_key(self, size: int) -> str:
        """生成随机字符串（参考DingCallbackCrypto3.generateRandomKey）"""
        import string
        import random
        
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    
    def success_response(self, message: str = "success") -> HttpResponse:
        """成功响应（使用钉钉格式）"""
        return self.dingtalk_response(message)
    
    def error_response(self, message: str = "error", status: int = 400) -> HttpResponse:
        """错误响应（使用钉钉格式）"""
        return self.dingtalk_response(message)