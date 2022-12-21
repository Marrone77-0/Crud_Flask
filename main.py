from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


#Configurações iniciais e essenciais do "flask" e "sqlalchemy"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
db = SQLAlchemy(app)

#Criando a classe "usuarios" que ira se torna uma tabela.
class usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)
    idade = db.Column(db.Integer)
    def __init__(self,nome,idade):
        self.nome = nome
        self.idade = idade


#Criando o caminho inicial da pagina.
#Crio a variavel usuario, e armazeno um comando sqlalchemy.
#Este comando é um "select" SQL: (Select * from usuarios)
@app.route('/')
def homepage():
    usuario = usuarios.query.all()
    return render_template('homepage.html', usuario = usuario)


#Direciona o usuario a uma pagina html.
#Envia pelo método 'POST' as informações do <form>
#Pego essas informações por um request e as armazeno na variavel usuario.
@app.route('/add_user', methods=['POST','GET'])
def add_usuario():
    if request.method == 'POST':
        usuario = usuarios(request.form['nome'],request.form['idade'])
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template('usuarios.html')

#Função que deleta um usuario do Banco de dados
#Pego o (id) primary key do usuario.
#Armazeno este id em usuario.
#Deleto ele do banco de dados, e salvo dando um (commit)
@app.route('/delete/<int:id>')
def delete(id):
    usuario = usuarios.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('homepage'))

#Função que edita um usuario
#Pegando novamente o (id)
#Com o (id) já armazenado em "usuario", ele referencia o (nome) e (idade)
#E altero eles, salvo novamente com um (commit)
@app.route('/editar/<int:id>', methods=['POST','GET'])
def editar(id):
    usuario = usuarios.query.get(id)
    if request.method == 'POST':
       
        usuario.nome = request.form['nome']
        usuario.idade = request.form['idade']
        db.session.commit()
        return redirect(url_for('homepage'))
    else:
        return render_template('edit.html', usuario = usuario)
    

#O if padrão para conferir se o arquivo esta sendo executado como arquivo principal.
#Caso seja, cria todas as tabelas e inica o app-Flask
if __name__ == ('__main__'):
    with app.app_context():
        db.create_all()
    app.run(host='localhost',port=8080,debug=True)

