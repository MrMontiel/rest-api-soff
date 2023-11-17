from app.users.adapters.sqlalchemy.user import User

def userSchema(user: User)-> dict:
    return{
        "id":user.id,
        "name":user.name,
        "document_type":user.document_type,
        "document":user.document,
        "phone":user.phone,
        "email":user.email,
        "password":user.password,
        "status":user.status,
        "role":user.role.name
    }
    
def usersSchema(users: list[User])->list:
    return[userSchema(user) for user in users]
