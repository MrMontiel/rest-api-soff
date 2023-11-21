from sqlalchemy import select
from fastapi import HTTPException, Depends, Request
from app.infrastructure.database import ConectDatabase
from app.users.adapters.sqlalchemy.user import User
from app.auth.adapters.exceptions.exceptions import InvalidCredentials, UnauthorizedException, InactivateUser, EmailNotFound, CodeNotFound, CodeConfirmed,UserNotFound, ApikeyNotFound
from app.roles.adapters.services.services import get_id_role
from app.permissions.adapters.serializer.roles_schema import permissionSchema, PermissionsSchema
from app.permissions.adapters.services.services import get_id_permission
from app.auth.domain.pydantic.userauth import UserAuthenticated, TokenResponse, User as UserInDB
from app.auth.adapters.services.hashed import verify_password, get_password_hash
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import dotenv_values
from app.roles.adapters.sqlalchemy.role import Role
import uuid
import os
import resend
import random
import string
from app.auth.adapters.sqlalchemy.models import RecoverPassword
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mailersend import emails
import secrets
from typing import Optional



session = ConectDatabase.getInstance()
variables = dotenv_values('.env')

SECRET_KEY = "b902c221b0d6057df167a5fa560178327ebfd974bddde9d18c07be772e4522d7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = "15"
RESEND_API_KEY = "re_j7pkDx9G_CteY4E6qKzRnW22Wyua9ZTs9"
SECRET_KEY_REFRESH = "ae95e7583fdedc822aba608edbb6cb7f046eb4b698ee118bca3107243a71f9c1"

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_permissions(id_role: str):
    role = session.get(Role, id_role)
    permissions = []
    for per in role.Permissions:
        permission = get_id_permission(per.id_permission)
        schema_permission = permissionSchema(permission)
        permissions.append(schema_permission["name"])
    return permissions

def getUser(email: str):
    user:User = session.scalars(select(User).where(User.email == email)).first()
    if not user:
        InvalidCredentials()
    permissions = get_permissions(user.id_role)
    
    return UserAuthenticated(
        name=user.name,
        email=user.email,
        status=user.status,
        permissions=permissions,
        hashed_password=user.password
    )
    
def authenticateUser(email: str, password: str):
    user = getUser(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return UserInDB(
        name=user.name,
        email=user.email,
        status=user.status,
        permissions=user.permissions
    )
    
# def createAccessToken(data: dict, expire_delta: timedelta | None = None):
def createAccessToken(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(days=3)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def createRefreshToken(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=60*24*30)})
    refresh_token = jwt.encode(to_encode, SECRET_KEY_REFRESH, algorithm=ALGORITHM)
    return refresh_token

def get_token_from_header(authorization: str = Depends(oauth_2_scheme)):
    if authorization is None or not authorization.startswith("Bearer "):
        UnauthorizedException()
    token = authorization.replace("Bearer ", "")
    print(token)
    return token

def generateAccessTokenForRefreshToken(refresh_token: str ):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY_REFRESH, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            UnauthorizedException()
    except JWTError:
        UnauthorizedException() 
    
    user = getUser(email)
    if user is None:
        UnauthorizedException()
    
    access = createAccessToken({"sub": user.email})
    return  {
        "access_token": access  
    }

async def getCurrentUser(token: str = Depends(oauth_2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            UnauthorizedException()
        
    except JWTError:
        UnauthorizedException() 

    user = getUser(email)
    if user is None:
        UnauthorizedException()
        
    return UserInDB(
        name = user.name,
        email = user.email,
        status = user.status,
        permissions = user.permissions
    )

async def getCurrentActivateUser(current_user: UserInDB = Depends(getCurrentUser)):
    if current_user.status  == False:
        InactivateUser()
    return current_user

def verifyToken(token: str = Depends(oauth_2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        return False
 
def verifyEmail(email: str):
    user: User = session.scalars(select(User).where(User.email == email)).first()
    if not user:
        EmailNotFound()
    return user

def generateCode():
    caracteres = string.ascii_letters + string.digits  # Incluye letras y números
    codigo = ''.join(random.choice(caracteres) for _ in range(6))
    return codigo.upper()

def generateApiKey():
    api = secrets.token_urlsafe(32)
    return api

def sendEmail(email: str, code: str, cuerpo: str):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Puerto TLS de Gmail
    smtp_user = 'mandisa.soff@gmail.com'  # Tu dirección de correo electrónico de Gmail
    smtp_password = 'wkxa zibm ogth nkef'  # Tu contraseña de Gmail

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Inicia una conexión segura
    
    # Inicia sesión en tu cuenta de Gmail
    server.login(smtp_user, smtp_password)

    # Crea y envía un correo electrónico
    mensaje = MIMEMultipart()
    mensaje['From'] = smtp_user
    mensaje['To'] = email
    mensaje['Subject'] = f'Recuperar contraseña: {code}'
    
    mensaje.attach(MIMEText(cuerpo, 'html'))
    
    # Envía el correo electrónico
    server.sendmail(smtp_user, email, mensaje.as_string())

    # Cierra la conexión al servidor SMTP
    server.quit()

def recoveryPassword(email: str):
    user = verifyEmail(email)
    code = generateCode()
    apikey = generateApiKey()
    newRecoverPassword = RecoverPassword(user_id=user.id, code=code, apikey=apikey)
    session.add(newRecoverPassword)
    session.commit()
    session.refresh(newRecoverPassword)
    
    cuerpo = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap" rel="stylesheet"> 
        </head>
        <body style="font-family: 'Lato', sans-serif; color: #404040 ">
            <div style="display: flex; align-items: center; justify-content: center">
                <div style="width: 100%; background: #f5f5f5; padding: 10px; max-width: 450px">
                    <div style="display: flex; flex-direction: column; gap: 30px">
                        <img style="width: fit-content;" src="https://ndfpwovnqeovyfqhphrh.supabase.co/storage/v1/object/public/soff-user/profile/soff.3c813527.svg" alt="">
                        <h1 style="font-size: 30px; font-weight: 700">Restablecer contraseña</h1>
                    </div>
                    <div>
                        <p style="margin-bottom: 10px;">Estimado {user.name}</p>
                        <p style="margin-bottom: 10px;">Recibiste este correo electrónico para proceder con la solicitud de cambio de contraseña en tu cuenta. Para completar el proceso de verificación, utiliza el siguiente código de seguridad:</p>
                        <div style="margin-bottom: 10px;">
                            <p style="font-size: 30px; font-weight: 700; letter-spacing: 10px">{code}</p>
                        </div>
                        <p style="margin-bottom: 10px;">Por favor, asegúrate de que solo tú tengas acceso a este código. Si no has solicitado un cambio de contraseña, te recomendamos cambiar tu contraseña actual de inmediato y ponerse en contacto con nuestro soporte si consideras que esto es un error.</p>
                        <p style="margin-bottom: 10px;">Gracias por utilizar nuestros servicios.</p>
                        <p>Atentamente, <span style="font-weight: 700;">MANDISA.</span></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
    """
    sendEmail(email, code, cuerpo)
    return {
        'id': newRecoverPassword.id,
        'message': 'nueva recuperación generada'
    }

def verifyCode(code: str, user_id: str):
    recovery: RecoverPassword = session.scalars(select(RecoverPassword).filter(RecoverPassword.user_id == user_id, RecoverPassword.code == code)).first()
    if not recovery:
        CodeNotFound()
    if recovery.verify == True:
        CodeConfirmed()
    return recovery


def createAccessTokenForRecoverPassword(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=12)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def confirmCode(code: str, email: str):
    user = verifyEmail(email)
    recovery = verifyCode(code, user.id)
    recovery.verify = True
    
    session.add(recovery)
    session.commit()
    session.refresh(recovery)
    return {
        "id": recovery.id,
        "apikey": recovery.apikey
    }
    
    
def verifyApikey(apikey: str):
    pass
    
def changePassword(new_password: str, apikey: str):
    recovery: RecoverPassword = session.scalars(select(RecoverPassword).where(RecoverPassword.apikey == apikey)).first()
    if not recovery:
        ApikeyNotFound()
        
    user: User = session.get(User, recovery.user_id) 
    
    if not user:
        UserNotFound()
        
    new_password_hashed = get_password_hash(new_password)
    user.password = new_password_hashed
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
