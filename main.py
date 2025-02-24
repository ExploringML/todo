from fasthtml.common import *
from fh_dev_utils.serve import *
from fastcore.meta import use_kwargs, delegates
from hmac import compare_digest
from datetime import datetime
from lib.templates import _404, clr_details, plus_svg, mk_login_form, page_form, mk_register_form
from lib.faststart import Container_FS, Nav_FS, Footer_FS
from lib.utils import login_redir, home_redir, register_redir, Login, Register, loginout_link, get_user
from db import before, todos, users, Todo, User, db

# -----------------------------------FastHTML Setup-----------------------------------

DEV_MODE=True
bware = Beforeware(before, skip=[r'/favicon\.ico', r'/assets/.*', r'.*\.css', '/', '/register', '/login'])
app = FastHTMLWithLiveReload(before=bware,
    exception_handlers={404: _404},
    pico=False,
    hdrs=(
        Link(rel="stylesheet", href=f"/public/app.css{cache_buster() if DEV_MODE else ""}", type="text/css"),
    )
)
rt = app.route

# -----------------------------------Homepage Routes-----------------------------------

# Handy custom component to wrap header and footer around content
@delegates(ft_hx, keep=True)
def Wrapper_FS(*children, header=None, footer=None, sess=None, default=True, cls="", **kwargs):
    "A basic card"
    core_cls = ""
    if default:
        core_cls = f"{core_cls} {cls}"
    else:
        core_cls = cls

    return Container_FS(
        site_header(sess),
        *children,
        Footer_FS(),
        cls=core_cls,
        **kwargs
    )

def site_header(sess):
    loginout = loginout_link(sess)
    return Nav_FS(
        Li(
            A(
                Img(src='assets/logo.png', alt='Todo Manager', cls='w-[110px] h-[50px]'),
                href='/'
            ),
            cls="mr-auto"
        ),
        Li(A('My Todos', href='/todos')),
        Li(A('Docs', href='/docs')),
        Li(A(loginout[0], href=loginout[1]))
    )

@rt("/")
def get(sess):
    print(f"sess: {sess}")
    user = get_user(sess)

    return Wrapper_FS(
        Div(
            H2(f"Welcome, {user}!"),
            Div('Todo FastHTML demo appliction.'),
            cls="space-y-6"
        ),
        sess=sess
    )

# -----------------------------------Login Routes-----------------------------------

@rt("/login")
def get(sess):
    frm = mk_login_form()
    return Wrapper_FS(
        Div(
            frm,
            cls="mx-auto"
        ),
        sess=sess
    )

@rt("/login")
def post(login:Login, sess):
    # Early validation of required fields
    if not (login.email and login.pwd):
        return Wrapper_FS(Div(mk_login_form({'misc': 'Email and password required'}), cls="mx-auto"), sess=sess)
    
    try:
        users = db.q("select * from users where email = ?", (login.email,))
        errors = {}

        # If no user is found, or multiple users, show error
        if len(users) != 1:
            errors['misc'] = 'Invalid email or password'
        
        # Check password
        if len(users) == 1:
            user = users[0]
            if not compare_digest(user['pwd'].encode("utf-8"), login.pwd.encode("utf-8")):
                errors['misc'] = 'Invalid email or password'

        if errors:
            return Wrapper_FS(Div(mk_login_form(errors), cls="mx-auto"), sess=sess)

        # Success case - set session and redirect
        sess.update({
            'auth': user['id'],
            'user_name': user['name'], 
            'email': user['email']
        })
        
        return Redirect(sess.pop('intended_url', '/'))

    except NotFoundError:
        return Wrapper_FS(Div(mk_login_form({'misc': 'Invalid email or password'}), cls="mx-auto"), sess=sess)

# -----------------------------------Logout Routes-----------------------------------

@rt("/logout")
def get(sess):
    del sess['auth']
    if 'user_name' in sess:
        del sess['user_name'] 
    if 'email' in sess:
        del sess['email']
    return login_redir

# -----------------------------------Register Routes-----------------------------------

@rt("/register")
def get(sess):
    frm = mk_register_form()
    return Wrapper_FS(
        Div(
            frm,
            cls="mx-auto"
        ),
        sess=sess
    )

@rt("/register")
def post(register:Register, sess):
    # Early validation of required fields
    if not (register.email and register.pwd): # name is optional
        return Wrapper_FS(Div(mk_register_form({'misc': 'Email and password required'}), cls="mx-auto"), sess=sess)
    
    try:
        users = db.q("select * from users where email = ?", (register.email,))
        errors = {}

        if len(users) != 0:
            errors['misc'] = 'User already exists'

        if errors:
            return Wrapper_FS(Div(mk_register_form(errors), cls="mx-auto"), sess=sess)

        # Insert new user using execute with explicit SQL
        db.execute("""
        INSERT INTO users (name, pwd, email) VALUES (?, ?, ?);
        """, (register.name, register.pwd, register.email))

        # Get the new user
        user = db.q("select * from users where email = ?", (register.email,))[0]

        # Set session data
        sess.update({
            'auth': user['id'],
            'user_name': user['name'], 
            'email': user['email']
        })
        
        return RedirectResponse('/', status_code=303)
        
    except NotFoundError:
        return register_redir

# -----------------------------------Todo Routes-----------------------------------

# By including the `auth` parameter, it gets passed the current username, for displaying in the title.
@rt("/todos")
def get(auth, sess):
    user_name = sess.get('user_name', 'User')
    new_inp = Input(id="new-title", name="title", type="text", placeholder="New Todo", cls='rounded-md bg-white font-semibold text-gray-900 ring-1 shadow-xs ring-gray-300 ring-inset hover:bg-gray-50 border-0')
    quick_add = Form(
        Group(
            Div(
                new_inp,
                Button("Quick Add", cls='rounded-md bg-white px-3 py-[10px] text-sm font-semibold text-gray-900 ring-1 shadow-xs ring-gray-300 ring-inset hover:bg-gray-50 cursor-pointer'),
                cls="flex gap-x-2 items-center"
            ),
            Button(
                A(
                    plus_svg(),
                    title="Add a new todo",
                    href='/',
                    cls='inline-flex items-center gap-x-2 px-3.5 py-2.5'
                ),
                cls='rounded-md bg-white text-sm font-semibold text-gray-900 ring-1 shadow-xs ring-gray-300 ring-inset hover:bg-gray-50'
            ),
            cls='flex justify-between'
        ),
        hx_post="/todos",
        target_id='todo-list',
        hx_swap="afterbegin",
        cls="mt-4 mb-8"
    )
    items = Tbody(*todos(order_by='priority'),
               id='todo-list', cls='sortable divide-y divide-gray-200')

    return  Wrapper_FS(
        Div(
            Div(
                quick_add,
                H2(f"{ user_name + '\'s ' if user_name else ''}Todo List", cls='font-semibold text-lg mb-4'),
                Ul(
                    items,
                    id='todo-list',
                    cls='min-w-fit divide-y divide-gray-300'
                ),
                Div(id='current-todo'),
                cls="px-8"
            ),
        ),
        sess=sess
    )

# This route handler uses a path parameter `{id}` which is automatically parsed and passed as an int.
@rt("/todos/{id}")
def delete(id:int):
    print(f"delete id: {id}")
    todos.delete(id)
    return clr_details()

@rt("/edit/{id}")
def get(id:int):
    print(f"edit id: {id}")
    res = Div(
        H2('Edit Todo', cls='mb-2'),
        Form(
            Group(
                Input(id="title", type="text", cls='w-[250px]'),
                Textarea(id="details", name="details", cls='w-[250px] h-[100px]'),
                CheckboxX(id="done", label='Done'),
                Button("Save", cls='cursor-pointer bg-indigo-600 text-white px-3 py-1.5 rounded-md'),
                Button("Cancel", hx_put="/todos/cancel", cls='cursor-pointer bg-white text-gray-600 px-3 py-1.5 rounded-md'),
                Button('Delete', hx_delete=f'/todos/{id}', hx_target=f'#todo-{id}', hx_swap="outerHTML", cls='cursor-pointer bg-red-600 text-white px-3 py-1.5 rounded-md'),
                cls="flex justify-between gap-x-2"
            ),
            Hidden(id="id"),
            hx_put="/todos",
            hx_swap="outerHTML",
            hx_target=f'#todo-{id}',
            cls="space-y-3",
            id="edit"
        ),
        cls="mt-9"
    )
    # `fill_form` populates the form with existing todo data, and returns the result.
    # Indexing into a table (`todos`) queries by primary key, which is `id` here. It also includes
    # `xtra`, so this will only return the id if it belongs to the current user.
    return fill_form(res, todos[id])

@rt("/todos/{id}")
def get(id:int):
    todo = todos[id]
    return Div(
        H2(todo.title),
        Div(todo.details, cls="py-4"),
        Button('Delete', hx_delete=f'/todos/{todo.id}', target_id=f'todo-{todo.id}', hx_swap="outerHTML", cls='btn'),
        cls="mt-9"
    )

@rt("/todos/cancel")
def put():
    return clr_details()

@rt("/todos")
def put(todo:Todo):
    print(f"todo: {todo}")
    todo_title = todo.title.strip()
    if todo_title == '' or todo_title is None:
        return clr_details()

    return todos.update(todo), clr_details()

@rt("/todos")
def post(todo:Todo, auth, sess):
    print(f"auth: {auth}, sess: {sess}")
    todo_title = todo.title.strip()
    if todo_title == '' or todo_title is None:
        return None

    # `hx_swap_oob='true'` tells HTMX to perform an out-of-band swap, updating this element wherever it appears.
    # This is used to clear the input field after adding the new todo.
    new_inp =  Input(id="new-title", name="title", type="text", placeholder="New Todo", hx_swap_oob='true')
    # `insert` returns the inserted todo, which is appended to the start of the list, because we used
    # `hx_swap='afterbegin'` when creating the todo list form.
    todo.date = str(int(datetime.now().timestamp()))
    todo.user_id = auth
    print(todo)
    return todos.insert(todo), new_inp

# -----------------------------------Process Static Files-----------------------------------

@rt("/{fname:path}.{ext:static}")
def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

# -----------------------------------Start Servers-----------------------------------

if DEV_MODE: serve_dev(db=True, db_path='data/main.db', tw=True, jupyter=True, reload_includes=["*.css"])
else: serve()