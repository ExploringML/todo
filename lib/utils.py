from fasthtml.common import *

# Status code 303 is a redirect that can change POST to GET, so it's appropriate for a login page.
login_redir = RedirectResponse('/login', status_code=303)
register_redir = RedirectResponse('/register', status_code=303)
home_redir = RedirectResponse('/', status_code=303)

@dataclass
class Login: email:str; pwd:str

@dataclass
class Register: name:str; email:str; pwd:str

def n_words(text, n):
    if not text: return ''
    words = text.split()
    if len(words) <= n:
        return text
    trimmed_text = ' '.join(words[:n])
    return NotStr(trimmed_text + '&hellip;')

def loginout_link(sess):
    # Get the authenticated user from the session and create a login or logout link
    auth = sess.get('auth')
    if auth:
        user_name = sess.get('user_name')
        return (f"Logout{' ' + user_name if user_name else ''}", '/logout')
    else:
        return ('Login', '/login')

def get_user(sess):
    # Get the authenticated user from the session
    auth = sess.get('auth')
    return sess.get('user_name') if auth else 'Guest'
