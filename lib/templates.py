from fasthtml.common import *
from collections import defaultdict

# -----------------------------------Form Templates-----------------------------------

# Page form
def page_form(frm, links):
    return (
        header(links=links),
        Div(
            frm,
            cls="flex  justify-center"
        ),
        footer(),
    )

# Login form
def mk_login_form(errors: dict|None = None):
    # If no errors, we default to {}
    # Loop through the errors, turning strings into Small(str)
    d = {k:P(v, cls='text-sm text-red-500 mt-1')
         for k,v in (errors or {}).items()}
    # Set the default value of errors to empty NotStr() objs
    errors = defaultdict(lambda: NotStr(''), d)
    # Return the form
    return Form(
        H2('Login', cls='mb-0 text-lg'),
        Input(id='email', type="email", placeholder='Email', cls="rounded-sm"),
        Div(
            Input(id='pwd', type='password', placeholder='Password', cls="rounded-sm"),
            P(A('Forgot password?', href='/reset', cls='underline'), cls='text-right text-sm mt-1.5'),
            Div(errors['misc'], cls='text-right'),
        ),
        Button(
            'Sign In',
            cls='inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 self-end cursor-pointer -mt-1'
        ),
        Div(
            P('Don\'t have an account? ', A('Sign Up', href='/register', cls='underline'), cls="text-sm"),
            P(A('Sign-in with magic link!', href='/magic-link', cls='underline'), cls='text-sm'),
            cls='flex flex-col items-center gap-y-2 mt-4'
        ),
        id='login-form',
        cls='w-fit mt-4 mb-10 flex flex-col gap-y-6 items-center justify-center',
        hx_post='/login',
        hx_swap="outerHTML",
        hx_target="body"
    )

# Register form
def mk_register_form(errors: dict|None = None):
    # If no errors, we default to {}
    # Loop through the errors, turning strings into Small(str)
    d = {k:P(v, cls='text-sm text-red-500 mt-1.5')
         for k,v in (errors or {}).items()}
    # Set the default value of errors to empty NotStr() objs
    errors = defaultdict(lambda: NotStr(''), d)    
    # Return the form
    return Form(
        H2('Register', cls='mb-0 text-lg'),
        Input(id='name', type="text", placeholder='Name (optional)', cls="rounded-sm"),
        Input(id='email', type="email", placeholder='Email', cls="rounded-sm"),
        Div(
            Input(id='pwd', type='password', placeholder='Password', cls="rounded-sm"),
            Div(errors['misc'], cls='text-right')
        ),
        Button(
            'Sign Up',
            cls='inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 self-end cursor-pointer -mt-1'
        ),
        P('Already have an account? ', A('Sign In', href='/login', cls='underline'), cls='text-sm'),
        cls='w-fit mt-4 mb-10 flex flex-col gap-y-6 items-center justify-center',
        hx_post='/register',
        hx_swap="outerHTML",
        hx_target="body"
    )

# -----------------------------------Misc Templates-----------------------------------

# Custom 404 response
def _404(req, exc): return Title('404 - Page not found!'), Main(
    Div(
        P('404', cls='text-lg font-semibold text-indigo-600'),
        H1('Page not found', cls='mt-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-5xl'),
        P('Sorry, we couldn’t find the page you’re looking for.', cls='mt-6 text-base leading-7 text-gray-600'),
        Div(
            Button(A(home_svg(), 'Home', href='/', cls='inline-flex items-center gap-x-2 px-3.5 py-2.5'), cls='btn p-0'),
            cls='mt-10 flex items-center justify-center gap-x-6'
        ),
        cls='text-center'
    ),
    cls='grid min-h-full place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8'
)

def clr_details(): return Div(hx_swap_oob='innerHTML', id='current-todo')

def header(logo='assets/logo.png', logo_alt='Todo manager', links={}): return Div(
    Nav(
        Ul(
            Li(
                A(
                    Img(src=logo, alt=logo_alt, cls='w-[110px] h-[50px]'),
                    href='/'
                ),
				cls="mr-auto"
            ),
            *[Li(A(link, href=href)) for link, href in links.items()],
            cls="m-0 p-0 list-none flex flex-row flex-wrap gap-x-8 gap-y-4 justify-between items-end font-medium"
        ),
        cls="mb-8"
    ),
)

def footer(logo='assets/fh-logo.svg', logo_alt='Made with FastHTML'):
    return Div(
        Nav(
            Ul(
                Li(
                    A(
                        'Follow me on',
                        Img(src='assets/twitter.png', alt=logo_alt, cls='w-[12px] h-[13px] inline ml-[5px]'),
                        href='https://x.com/dgwyer',
                        target="_blank",
                        cls="flex items-center"
                    ),
                ),
                Li(
                    Span('Built with'),
                    A(
                        Img(src=logo, alt=logo_alt, cls='w-[125px] h-[24px] inline'),
                        target="_blank",
                        href='https://www.fastht.ml/'
                    ),
                    cls="ml-auto flex items-center"
                ),
                cls="m-0 p-0 list-none flex flex-row flex-wrap gap-x-8 gap-y-4 justify-between items-end font-medium"
            ),
            cls="mt-8"
        ),
    )

def home_svg(): return NotStr('<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="-ml-0.5 h-5 w-5"><path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" /></svg>')

def plus_svg(): return NotStr('<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="-ml-0.5 h-5 w-5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>')
