from flask import Flask, render_template, session, redirect, url_for, request
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
Bootstrap(app)
Moment(app)

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome', validators=[DataRequired()])
    lastname = StringField('Informe o seu sobrenome', validators=[DataRequired()])
    institution = StringField('Informe a sua Instituição de ensino')
    disciplina = SelectField('Informe a sua disciplina:', choices=[('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'), ('Gestão de Projetos', 'Gestão de Projetos')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['lastname'] = form.lastname.data
        session['institution'] = form.institution.data
        session['disciplina'] = form.disciplina.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), lastname=session.get('lastname'), institution=session.get('institution'), disciplina=session.get('disciplina'), current_time=datetime.utcnow())

@app.route('/user/<name>/<lastname>/<institution>/<disciplina>')
def user(name, lastname, institution, disciplina):
    return render_template('user.html', name=name, lastname=lastname, institution=institution, disciplina=disciplina)

@app.route('/contextorequisicao/<name>')
def contextorequisicao(name):
    user_agent = request.headers.get('User-Agent')
    remote_addr = request.remote_addr
    remote_host = request.host
    return render_template('contexto.html', name=name, user_agent=user_agent, remote_addr=remote_addr, remote_host=remote_host)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
