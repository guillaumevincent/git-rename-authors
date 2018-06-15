import json
import os
import subprocess
import sys
import tkinter
import tkinter.messagebox
import tkinter.ttk

from git_rename_authors.authors import get_list_authors, parse_authors
from git_rename_authors.script import generate_script


def git_filter(source_authors, destination_author):
    try:
        script = generate_script(source_authors, destination_author)
        script_name = 'git-authors-rewrite.sh'
        with open(script_name, 'w') as script_sh:
            script_sh.write(script)
        subprocess.run('chmod +x ./{}'.format(script_name),
                       stdout=subprocess.PIPE, shell=True)
        subprocess.run('./{}'.format(script_name),
                       stdout=subprocess.PIPE, shell=True)
        tkinter.messagebox.showinfo(
            title='Success', message="Review the new Git history for errors.")
        os.remove('./{}'.format(script_name))
        print("Review the new Git history for errors.\nIf you want to delete the refs created, just run:\ngit for-each-ref --format=\"%(refname)\" refs/original/ | xargs -n 1 git update-ref -d")
    except Exception as e:
        with open('error.log', 'w') as f:
            f.write(str(e))
        tkinter.messagebox.showerror(
            title='Error', message='En error occured, see error.log')


def show_preview(source_authors, destination_author):
    if not len(source_authors):
        return 'you should select an email to be replaced by "%s"' % destination_author
    s = ''
    for author in source_authors:
        source_author = '%s <%s>' % (author['name'], author['email'])
        if (source_author == destination_author.strip()):
            s += '"%s" will be ignored (same as "%s")\n' % (
                destination_author, source_author)
        else:
            s += '"%s" will be replaced by "%s"\n' % (
                source_author, destination_author)

    return s


def start():
    process = subprocess.run(
        "git log --pretty=\"%an;%ae%n%cn;%ce\" | sort | uniq", stdout=subprocess.PIPE, shell=True)

    stdout = process.stdout.decode('utf-8')
    if len(stdout) == 0:
        tkinter.messagebox.showerror(title='Error',
                                     message='Not a git repository (or any of the parent directories): .git')
        sys.exit(-1)

    root = tkinter.Tk()
    root.title('Clean git authors')
    root.columnconfigure(0, weight=1)

    authors = parse_authors(stdout)

    def preview():
        source_authors = [authors[i]
                          for i in authors_list_widget.curselection()]
        destination_author = destination_author_field.get()
        logs_widget['text'] = show_preview(source_authors, destination_author)

    def replace_emails():
        result = tkinter.messagebox.askquestion("Git filter",
                                                "Warning: This action is destructive to your repository's history. If you're collaborating on a repository with others, it's considered bad practice to rewrite published history. You should only do this in an emergency. Are you sure you want to rewrite your history ?",
                                                icon='warning')
        if result != 'yes':
            return
        source_authors = [authors[i]
                          for i in authors_list_widget.curselection()]
        destination_author = destination_author_field.get()
        git_filter(source_authors, destination_author)

    width = 100
    # widgets
    explanation1 = tkinter.ttk.Label(
        text='1 - Select one or more emails you want to replace')
    authors_display = tkinter.StringVar(value=get_list_authors(authors))
    authors_list_widget = tkinter.Listbox(
        width=width,
        selectmode='extended',
        listvariable=authors_display,
        exportselection=0
    )
    explanation2 = tkinter.Label(
        text='2 - Enter the name and the destination email')
    destination_author_field = tkinter.Entry()
    destination_author_field.insert(
        tkinter.INSERT, get_list_authors(authors)[0])
    merge_btn = tkinter.Button(
        text='3 - Click me to preview changes', command=preview, bg="green")
    logs_widget = tkinter.ttk.Label()
    git_filter_btn = tkinter.Button(
        text="4 - Click me to replace the emails", command=replace_emails, bg="orange")

    # rendering
    explanation1.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    authors_list_widget.grid(row=2, column=0, sticky="nsew", padx=10)
    for i in range(0, len(authors), 2):
        authors_list_widget.itemconfigure(i, background='#f0f0ff')
    explanation2.grid(row=4, column=0, sticky="w", padx=10, pady=10)
    destination_author_field.grid(row=6, column=0, sticky="nsew", padx=10)
    merge_btn.grid(row=8, column=0, sticky="nsew", padx=10, pady=10)
    logs_widget.grid(row=12, column=0, sticky="w", padx=10, pady=10)
    git_filter_btn.grid(row=14, column=0, sticky="nsew", padx=10, pady=10)
    root.mainloop()


if __name__ == '__main__':
    start()
