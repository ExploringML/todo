from fasthtml.common import *
from lib.utils import login_redir, n_words
from datetime import datetime
from fasthtml.svg import *

db = database('data/main.db')

todos,users = db.t.todos,db.t.users

db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT '',
    pwd TEXT,
    email TEXT UNIQUE
);
""")
db.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY,
    title TEXT,
    done INTEGER DEFAULT 0,
    user_id INTEGER,
    details TEXT,
    date TEXT,
    priority INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

#if todos not in db.t:
#    users.create(id=int, name=str, pwd=str, email=str, pk='id', defaults={'email': None})
#    todos.create(id=int, title=str, done=bool, user_id=int, details=str, date=str, priority=int, pk='id', foreign_keys=(('user_id', 'users')), if_not_exists=True)

Todo,User = todos.dataclass(),users.dataclass()

# Beforeware cb function, run before a route handler is called.
def before(req, sess):
    global todos
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth:
        sess['intended_url'] = req.url.path
        return login_redir
    todos.xtra(user_id=auth)

@patch
def __ft__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', 'current-todo')
    edit = AX('Edit',     f'/edit/{self.id}' , 'current-todo', cls='text-indigo-600 hover:text-indigo-900')
    if self.done:
        status = 'Completed'
        dt = 'mt-0.5 rounded-md bg-green-50 px-1.5 py-0.5 text-xs font-medium whitespace-nowrap text-green-700 ring-1 ring-green-600/20 ring-inset'
    else:
        status = 'In progress'
        dt = 'mt-0.5 rounded-md bg-yellow-50 px-1.5 py-0.5 text-xs font-medium whitespace-nowrap text-yellow-800 ring-1 ring-yellow-600/20 ring-inset'
    timestamp = int(self.date)
    formatted_date = datetime.fromtimestamp(timestamp).strftime('%B %d, %Y')

    return Li(
        Div(
            Div(
                Div(
                    Svg(
                        Circle(cx='1', cy='1', r='1'),
                        viewbox='0 0 2 2',
                        cls='size-1.5 fill-current'
                    ),
                    Div(show, cls=f'text-sm/6 font-semibold text-gray-900{" line-through" if self.done else ""}'),
                    cls='flex items-center gap-x-1.5'
                ),
                P(status, cls=dt),
                cls='flex items-start gap-x-3'
            ),
            Div(
                P(
                    NotStr('<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="display:inline-block;" class="size-4"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" /></svg>'),
                    'Due on',
                    Time(formatted_date, datetime='2023-03-17T00:00Z'),
                    cls='flex items-center gap-1 whitespace-nowrap'
                ),
                cls='mt-1 flex items-center gap-x-2 text-xs/5 text-gray-500'
            ),
            cls='min-w-0'
        ),
        Div(
            Div(edit, href='#', cls='rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 ring-1 shadow-xs ring-gray-300 ring-inset hover:bg-gray-50'),
            cls='flex flex-none items-center gap-x-4'
        ),
        id=f'todo-{self.id}',
        cls='flex items-center justify-between gap-x-6 py-5'
    )
