from pywinauto import Application


def todo():
    app = Application(backend='uia')
    app.connect(title_re=".*Chrome.*")
    dlg = app.top_window()
    url = dlg.child_window(title="Address and search bar", control_type="Edit").get_value()
    site = url.split('/')[0]
    print(site)

s = """urlhard
appeasy
.urls
https://www.google.com/
https://www.google.com/
.apps
[DIFFERENT APPS]
"""
def parse_rules(s):
    li = s.split('\n.')
    return li

print(parse_rules(s))