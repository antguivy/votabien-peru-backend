import logging

import resend
from fastapi import BackgroundTasks

from app.config.settings import get_settings
from app.models.auth import User

logger = logging.getLogger(__name__)
settings = get_settings()

resend.api_key = settings.RESEND_API_KEY


async def send_account_verification_email(
    user: User, token: str, background_tasks: BackgroundTasks
):
    activate_url = f"{settings.FRONTEND_HOST}/auth/new-verification?token={token}&email={user.email}"

    async def _send():
        try:
            response = resend.Emails.send(
                {
                    "from": f"{settings.APP_NAME} <{settings.EMAIL_FROM}>",
                    "to": [str(user.email)],
                    "subject": f"Verifica tu cuenta - {settings.APP_NAME}",
                    "html": get_verification_email_template(
                        app_name=settings.APP_NAME,
                        name=str(user.name),
                        activate_url=activate_url,
                    ),
                }
            )
            logger.info("Email de verificación enviado a %s: %s", user.email, response)
            return response
        except Exception as e:
            logger.error(
                "Error enviando email de verificación a %s: %s", user.email, str(e)
            )
            raise

    background_tasks.add_task(_send)


async def send_account_activation_confirmation_email(
    user: User, background_tasks: BackgroundTasks
):
    login_url = f"{settings.FRONTEND_HOST}/"

    async def _send():
        try:
            response = resend.Emails.send(
                {
                    "from": f"{settings.APP_NAME} <{settings.EMAIL_FROM}>",
                    "to": [str(user.email)],
                    "subject": f"¡Bienvenido a {settings.APP_NAME}! 🎉",
                    "html": get_welcome_email_template(
                        app_name=settings.APP_NAME,
                        name=str(user.name),
                        login_url=login_url,
                    ),
                }
            )
            logger.info("Email de bienvenida enviado a %s: %s", user.email, response)
            return response
        except Exception as e:
            logger.error(
                "Error enviando email de bienvenida a %s: %s", user.email, str(e)
            )
            raise

    background_tasks.add_task(_send)


def get_verification_email_template(app_name: str, name: str, activate_url: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verificación de cuenta - {app_name}</title>
    </head>
    <body style="
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8fafc;
    ">
        <div style="
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        ">
            <!-- Header -->
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 30px;
                text-align: center;
            ">
                <h1 style="
                    color: #ffffff;
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                ">{app_name}</h1>
                <p style="
                    color: #e2e8f0;
                    margin: 8px 0 0 0;
                    font-size: 16px;
                ">Verificación de cuenta</p>
            </div>
            
            <!-- Body -->
            <div style="padding: 40px 30px;">
                <h2 style="
                    color: #1a202c;
                    margin: 0 0 20px 0;
                    font-size: 24px;
                    font-weight: 600;
                ">¡Hola {name}! 👋</h2>
                
                <p style="
                    color: #4a5568;
                    margin: 0 0 24px 0;
                    font-size: 16px;
                    line-height: 1.6;
                ">
                    Gracias por registrarte en <strong>{app_name}</strong>. 
                    Para completar tu registro y activar tu cuenta, necesitas verificar tu dirección de correo electrónico.
                </p>
                
                <div style="text-align: center; margin: 32px 0;">
                    <a href="{activate_url}" style="
                        display: inline-block;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: #ffffff;
                        text-decoration: none;
                        padding: 16px 32px;
                        border-radius: 8px;
                        font-weight: 600;
                        font-size: 16px;
                        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.25);
                        transition: transform 0.2s ease;
                    ">
                        ✨ Verificar mi cuenta
                    </a>
                </div>
                
                <div style="
                    background-color: #f7fafc;
                    border-left: 4px solid #667eea;
                    padding: 16px 20px;
                    margin: 24px 0;
                    border-radius: 0 8px 8px 0;
                ">
                    <p style="
                        color: #4a5568;
                        margin: 0;
                        font-size: 14px;
                        line-height: 1.5;
                    ">
                        <strong>¿No puedes hacer clic en el botón?</strong><br>
                        Copia y pega este enlace en tu navegador:<br>
                        <span style="
                            word-break: break-all;
                            color: #667eea;
                            font-family: 'Courier New', monospace;
                            font-size: 12px;
                        ">{activate_url}</span>
                    </p>
                </div>
                
                <p style="
                    color: #718096;
                    margin: 24px 0 0 0;
                    font-size: 14px;
                    line-height: 1.5;
                ">
                    Este enlace expirará en 24 horas por motivos de seguridad.<br>
                    Si no solicitaste esta cuenta, puedes ignorar este correo.
                </p>
            </div>
            
            <!-- Footer -->
            <div style="
                background-color: #f7fafc;
                padding: 20px 30px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            ">
                <p style="
                    color: #a0aec0;
                    margin: 0;
                    font-size: 12px;
                ">
                    © 2024 {app_name}. Todos los derechos reservados.
                </p>
            </div>
        </div>
    </body>
    </html>
    """


def get_welcome_email_template(app_name: str, name: str, login_url: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>¡Bienvenido a {app_name}!</title>
    </head>
    <body style="
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8fafc;
    ">
        <div style="
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        ">
            <!-- Header -->
            <div style="
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                padding: 40px 30px;
                text-align: center;
            ">
                <h1 style="
                    color: #ffffff;
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                ">{app_name}</h1>
                <div style="font-size: 48px; margin: 16px 0;">🎉</div>
            </div>
            
            <!-- Body -->
            <div style="padding: 40px 30px;">
                <h2 style="
                    color: #1a202c;
                    margin: 0 0 20px 0;
                    font-size: 24px;
                    font-weight: 600;
                    text-align: center;
                ">¡Bienvenido, {name}!</h2>
                
                <p style="
                    color: #4a5568;
                    margin: 0 0 24px 0;
                    font-size: 16px;
                    line-height: 1.6;
                    text-align: center;
                ">
                    Tu cuenta ha sido verificada exitosamente. 
                    ¡Ya puedes comenzar a usar <strong>{app_name}</strong>!
                </p>
                
                <div style="text-align: center; margin: 32px 0;">
                    <a href="{login_url}" style="
                        display: inline-block;
                        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                        color: #ffffff;
                        text-decoration: none;
                        padding: 16px 32px;
                        border-radius: 8px;
                        font-weight: 600;
                        font-size: 16px;
                        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.25);
                    ">
                        🚀 Comenzar ahora
                    </a>
                </div>
                
                <p style="
                    color: #718096;
                    margin: 24px 0 0 0;
                    font-size: 14px;
                    line-height: 1.5;
                    text-align: center;
                ">
                    Si tienes alguna pregunta, no dudes en contactarnos.
                </p>
            </div>
            
            <!-- Footer -->
            <div style="
                background-color: #f7fafc;
                padding: 20px 30px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            ">
                <p style="
                    color: #a0aec0;
                    margin: 0;
                    font-size: 12px;
                ">
                    © 2024 {app_name}. Todos los derechos reservados.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
