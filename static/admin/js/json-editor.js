// JSON配置编辑器增强功能
document.addEventListener('DOMContentLoaded', function() {
    const configTextarea = document.querySelector('.json-config-field');
    
    if (configTextarea) {
        // 页面加载时自动格式化JSON
        setTimeout(function() {
            const jsonText = configTextarea.value.trim();
            if (jsonText) {
                try {
                    const parsed = JSON.parse(jsonText);
                    configTextarea.value = JSON.stringify(parsed, null, 2);
                } catch (e) {
                    // 如果解析失败，保持原样
                }
            }
        }, 100);
        // 格式化JSON按钮
        const formatButton = document.createElement('button');
        formatButton.type = 'button';
        formatButton.textContent = '格式化JSON';
        formatButton.className = 'button';
        formatButton.style.marginLeft = '10px';
        
        formatButton.addEventListener('click', function() {
            try {
                const jsonText = configTextarea.value.trim();
                if (jsonText) {
                    const parsed = JSON.parse(jsonText);
                    configTextarea.value = JSON.stringify(parsed, null, 2);
                    showMessage('JSON格式化成功', 'success');
                }
            } catch (e) {
                showMessage('JSON格式错误: ' + e.message, 'error');
            }
        });
        
        // 验证JSON按钮
        const validateButton = document.createElement('button');
        validateButton.type = 'button';
        validateButton.textContent = '验证JSON';
        validateButton.className = 'button';
        validateButton.style.marginLeft = '5px';
        
        validateButton.addEventListener('click', function() {
            try {
                const jsonText = configTextarea.value.trim();
                if (jsonText) {
                    JSON.parse(jsonText);
                    showMessage('JSON格式正确', 'success');
                } else {
                    showMessage('请输入JSON配置', 'warning');
                }
            } catch (e) {
                showMessage('JSON格式错误: ' + e.message, 'error');
            }
        });
        
        // 添加按钮到页面
        const fieldWrapper = configTextarea.closest('.form-row');
        if (fieldWrapper) {
            const buttonContainer = document.createElement('div');
            buttonContainer.style.marginTop = '10px';
            buttonContainer.appendChild(formatButton);
            buttonContainer.appendChild(validateButton);
            fieldWrapper.appendChild(buttonContainer);
        }
        
        // 实时验证
        configTextarea.addEventListener('blur', function() {
            const jsonText = this.value.trim();
            if (jsonText) {
                try {
                    JSON.parse(jsonText);
                    this.style.borderColor = '#28a745';
                } catch (e) {
                    this.style.borderColor = '#dc3545';
                }
            }
        });
    }
    
    function showMessage(text, type) {
        const message = document.createElement('div');
        message.textContent = text;
        message.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 15px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            z-index: 9999;
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#ffc107'};
        `;
        
        document.body.appendChild(message);
        
        setTimeout(() => {
            document.body.removeChild(message);
        }, 3000);
    }
});