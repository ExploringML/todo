from fasthtml.common import *
from fasthtml.svg import *
from fastcore.meta import use_kwargs, delegates

@delegates(ft_hx, keep=True)
def Footer_FS(*children, default=True, cls="", **kwargs):
    "A simple responsive footer"
    core_cls = "mt-auto"
    if default:
        core_cls = f"{core_cls} {cls}"
    else:
        core_cls = cls
    #return Div(*children, cls=core_cls, **kwargs)
    return Footer(
        Div(
            Div(
                A(
                    Span('X', cls='sr-only'),
                    Svg(
                        Path(d='M13.6823 10.6218L20.2391 3H18.6854L12.9921 9.61788L8.44486 3H3.2002L10.0765 13.0074L3.2002 21H4.75404L10.7663 14.0113L15.5685 21H20.8131L13.6819 10.6218H13.6823ZM11.5541 13.0956L10.8574 12.0991L5.31391 4.16971H7.70053L12.1742 10.5689L12.8709 11.5655L18.6861 19.8835H16.2995L11.5541 13.096V13.0956Z'),
                        fill='currentColor',
                        viewbox='0 0 24 24',
                        aria_hidden='true',
                        cls='size-6'
                    ),
                    href='https://x.com/dgwyer',
                    target="_blank",
                    cls='text-gray-600 hover:text-gray-800'
                ),
                cls='flex justify-center gap-x-6 md:order-2'
            ),
            P('© 2025 ACME Inc.', cls='mt-8 text-center text-sm/6 text-gray-600 md:order-1 md:mt-0'),
            cls='mx-auto max-w-7xl pt-12 pb-2 md:flex md:items-center md:justify-between'
        ),
        cls=core_cls
    )

@delegates(ft_hx, keep=True)
def Grid_FS(*children, default=True, cls="", **kwargs):
    "A responsive grid layout"
    core_cls = "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
    if default:
        core_cls = f"{core_cls} {cls}"
    else:
        core_cls = cls
    return Div(*children, cls=core_cls, **kwargs)

@delegates(ft_hx, keep=True)
def Card_FS(*children, default=True, cls="", **kwargs):
    "A basic card"
    core_cls = "p-4 rounded bg-gray-100 text-gray-800"
    if default:
        core_cls = f"{core_cls} {cls}"
    else:
        core_cls = cls

    return Div(*children, cls=core_cls, **kwargs)

@delegates(ft_hx, keep=True)
def Nav_FS(*children, default=True, cls="", **kwargs):
    "A basic navigation layout"
    core_cls = "text-gray-600"
    if default:
        core_cls = f"{core_cls} {cls}"
    else:
        core_cls = cls

    return Div(
        Nav(
            Ul(
                *children,
                cls="m-0 p-0 list-none flex flex-row flex-wrap gap-x-8 gap-y-4 justify-between items-center font-medium"
            ),
            cls="mb-8"
        ),
        cls=core_cls,
        **kwargs
    )

@delegates(ft_hx, keep=True)
def Container_FS(*children, default=True, cls="", **kwargs):
    print(f"cls: {cls}")
    "A responsive website container"
    core_cls = "bg-slate-50 min-h-screen"
    if default:
        core_cls = f"{core_cls} {cls}"
    else:
        core_cls = cls

    #return Div(*children, cls=core_cls, **kwargs)
    return Div(
        Div(
            *children,
            cls="flex flex-col p-8 mx-auto max-w-5xl min-h-screen bg-white bg-slate-200"
        ),
        cls=core_cls,
        **kwargs
    )
