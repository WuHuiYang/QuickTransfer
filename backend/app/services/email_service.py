import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from ..core.config import settings


class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_from = settings.SMTP_FROM

    def send_verification_code(self, email: str, code: str) -> bool:
        """发送验证码邮件"""
        if not self.smtp_user or not self.smtp_password:
            # 开发环境：如果没有配置邮件，直接打印到控制台
            print(f"[邮件验证码] 收件人: {email}, 验证码: {code}")
            return True

        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_from
            msg['To'] = email
            msg['Subject'] = "快传 - 登录验证码"

            body = f"""
            <html>
                <body>
                    <h2>快传 - 登录验证码</h2>
                    <p>您好，</p>
                    <p>您的登录验证码是：<strong style="font-size: 24px; color: #4CAF50;">{code}</strong></p>
                    <p>验证码有效期为 10 分钟，请尽快完成验证。</p>
                    <p>如果这不是您的操作，请忽略此邮件。</p>
                    <hr>
                    <p style="color: #999;">快传 - 简单快速的文件传输工具</p>
                </body>
            </html>
            """

            msg.attach(MIMEText(body, 'html'))

            # 根据端口选择连接方式
            # 465 端口使用 SSL，587 端口使用 STARTTLS
            if self.smtp_port == 465:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()

            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()

            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False


class VerificationCodeService:
    """验证码服务（内存存储）"""
    def __init__(self):
        self.codes = {}  # {email: {"code": "123456", "expires": timestamp}}

    def generate_code(self, email: str) -> str:
        """生成6位验证码"""
        code = str(random.randint(100000, 999999))
        import time
        self.codes[email] = {
            "code": code,
            "expires": int(time.time()) + 600  # 10分钟有效期
        }
        return code

    def verify_code(self, email: str, code: str) -> bool:
        """验证验证码"""
        import time
        if email not in self.codes:
            return False

        stored_data = self.codes[email]
        if int(time.time()) > stored_data["expires"]:
            # 验证码过期
            del self.codes[email]
            return False

        if stored_data["code"] == code:
            # 验证成功，删除验证码
            del self.codes[email]
            return True

        return False


email_service = EmailService()
verification_code_service = VerificationCodeService()
