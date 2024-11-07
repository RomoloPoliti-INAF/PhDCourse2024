from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

# from flaskr.auth import login_required
from simpleSite.db import get_db

bp = Blueprint('example', __name__)


def get_scheda(id):
    scheda = get_db().execute(
        'SELECT e.name, e.surname, e.email,e.text,e.lavoro_id, l.lavoro'
        ' FROM example e Join lavoro l on e.lavoro_id = l.id'
        ' WHERE e.id = ?', 
        (id,)
    ).fetchone()

    if scheda is None:
        abort(404, f"The people with id {id} doesn't exist.")

    return scheda

@bp.route('/')
def index():
    posts = {}
    return render_template('example/index.html', posts=posts)

@bp.route('/list', methods=('GET', 'POST'))
def plist():
    db = get_db()
    posts = db.execute(
        'SELECT example.name, example.surname, example.id, example.email, lavoro.lavoro'
        ' FROM example JOIN lavoro'
        ' ON example.lavoro_id=lavoro.id'
        ' ORDER  BY example.surname ASC'
    ).fetchall()
    return render_template('example/list.html', data=posts)

@bp.route('/list/<int:id>/')
def scheda2(id):
    db = get_db()
    scheda=get_scheda(id)
    return render_template('example/scheda.html', data=scheda)
    pass


@bp.route('/list/add/', methods=('GET', 'POST'))
def add():
    db = get_db()
    lavori = db.execute(
        'SELECT * FROM lavoro ORDER  BY lavoro.lavoro ASC'
    ).fetchall()
    error = {}
    if request.method == 'POST':
        
        name=request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        text=request.form['text']
        lavoro = request.form['lavoro']
        if not name:
            error['name'] = 'Name is required.'
        if not surname:
            error['surname'] = 'Family Name is required.'
        if not email:
            error['email'] = 'Email is required.'
        if not lavoro.isdigit():
            error['lavoro'] = 'Emplyment is required.'
        if len(error)==0:
            db = get_db()
            db.execute(
                'INSERT INTO example (name, surname, email, text, lavoro_id)'
                f' VALUES (?,?,?,?,?)',#("{name}", "{surname}", "{email}", "{text}", "{lavoro}")'
                (name, surname, email, text,lavoro)
            )
            db.commit()
            return redirect(url_for('example.plist'))

    context = {
        'title': 'Add data',
        'main': 'New Entry',
        'label': 'Add',
        'action': '/list/add/',
        'error': error,
        'lavori': lavori,
        'original': {}
    }
    return render_template('example/form.html', cont=context)




@bp.route('/list/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    print(id)
    db = get_db()
    lavori = db.execute(
        'SELECT * FROM lavoro ORDER  BY lavoro.lavoro ASC'
    ).fetchall()
    scheda=get_scheda(id)
    error={}
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        text = request.form['text']
        lavoro = request.form['lavoro']
        if not name:
            error['name'] = 'Name is required.'
        if not surname:
            error['surname'] = 'Family Name is required.'
        if not email:
            error['email'] = 'Email is required.'
        if not lavoro.isdigit():
            error['lavoro'] = 'Emplyment is required.'
        print(f"ERROR: {error}")
        if len(error) == 0:
            db = get_db()
            db.execute(
                'Update example set name=?, surname=?, email=?, text=?, lavoro_id=? where id=?',
                # ("{name}", "{surname}", "{email}", "{text}", "{lavoro}")'
                #
                (name, surname, email, text, lavoro,id)
            )
            db.commit()
            print(url_for('example.plist'))
            
            return redirect(url_for('example.plist'))
        else:
            print(error)

    context = {
        'title': 'Modigy data',
        'main': 'Modify Entry',
        'label': 'Update',
        'action': url_for('example.edit', id=id),
        'error': error,
        'lavori': lavori,
        'original': scheda,
    }
    print(url_for('example.plist'))
    return render_template('example/form.html', cont=context)


@bp.route('/list/<int:id>/del/')
def delete(id):
    db = get_db()
    db.execute(
        'DELETE FROM example WHERE id=?',(id,)
    )
    db.commit()
    return redirect(url_for('example.plist'))

@bp.route('/lavori', methods=('GET', 'POST'))
def lavori():
    db = get_db()
    error=''
    if request.method == 'POST':
        lavoro = request.form['nLavoro']
        if not lavoro:
            error = 'Emplyment is required.'
        else:
            db.execute(
                    'INSERT INTO lavoro (lavoro) VALUES (?)',
                    (lavoro,)
                    )
            db.commit()
    
    lavori = db.execute(
        'SELECT * FROM lavoro ORDER  BY lavoro.lavoro ASC'
    ).fetchall()
    context={
        'data':lavori,
        'error': error
        }    
    return render_template('example/lavori.html', context=context)
    pass
