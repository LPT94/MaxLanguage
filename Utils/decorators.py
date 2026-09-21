from functools import wraps 
from flask import session, redirect, render_template 
from context import ctrl_usuarios 

def admin_required(func): 
    @wraps(func) 
    def wrapper(*args, **kwargs): 
        if "usuario_id" not in session: 
            return render_template( "erro.html", titulo="Área restrita", mensagem="Área restrita, você precisa fazer login!", voltar="/" ) 
        usuario = ctrl_usuarios.get_registro( session["usuario_id"] )

        if usuario is None: 
            session.pop("usuario_id", None) 
            return render_template( "erro.html", titulo="Sessão inválida", mensagem="Não foi possível encontrar o usuário da sessão.", voltar="/" ) 
            
        if usuario.get_tipo() != "0": 
            return redirect("/") 
                
        return func(*args, **kwargs) 
    
    return wrapper

def user_required(func): 
    @wraps(func) 
    def wrapper(*args, **kwargs): 
        if "usuario_id" not in session: 
            return render_template( "erro.html", titulo="Área restrita", mensagem="Área restrita, você precisa fazer login!", voltar="/" ) 
        usuario = ctrl_usuarios.get_registro( session["usuario_id"] )

        if usuario is None: 
            session.pop("usuario_id", None) 
            return render_template( "erro.html", titulo="Sessão inválida", mensagem="Não foi possível encontrar o usuário da sessão.", voltar="/" ) 
            
        if usuario.get_tipo() != "1": 
            return redirect("/") 
                
        return func(*args, **kwargs) 
    
    return wrapper