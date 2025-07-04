"""
简单环境测试
"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_environments():
    """测试不同环境"""
    
    environments = ['dev', 'acc', 'prod']
    
    for env in environments:
        print(f"\n=== 测试 {env.upper()} 环境 ===")
        
        # 设置环境变量
        os.environ['DJANGO_ENV'] = env
        
        # 清理已导入的模块
        modules_to_clear = ['utils.logger', 'django.conf']
        for module in modules_to_clear:
            if module in sys.modules:
                del sys.modules[module]
        
        try:
            from utils.logger import get_logger
            logger = get_logger()
            
            logger.info(f"{env}环境测试", env=env, test=True)
            logger.error(f"{env}环境错误测试", env=env, test=True)
            
            print(f"✅ {env}环境配置正常")
            
        except Exception as e:
            print(f"❌ {env}环境配置失败: {e}")
    
    print(f"\n📁 生成的日志文件:")
    logs_dir = project_root / 'logs'
    if logs_dir.exists():
        for log_file in sorted(logs_dir.glob('*.log')):
            print(f"  - {log_file.name}")

if __name__ == "__main__":
    test_environments()