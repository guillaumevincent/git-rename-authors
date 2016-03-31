import json
import os
import subprocess
import sys
import tkinter
import tkinter.messagebox
import tkinter.ttk

from authors import get_list_authors, merge_authors, parse_authors
from script import get_script


def git_push():
    if git_filter_ok:
        gp = subprocess.run("git push --force --tags origin 'refs/heads/*'", stdout=subprocess.PIPE, shell=True)
        if gp.returncode == 1:
            tkinter.messagebox.showerror(title='Error', message="failed to push some refs")
        else:
            tkinter.messagebox.showinfo(title='Success',
                                        message="Thank you for using clean-git-authors. Created by @guillaume20100.")
        sys.exit(-1)
    else:
        tkinter.messagebox.showerror(title='Error', message='Git filter first')


def git_filter(merged_authors):
    try:
        script = get_script(merged_authors)
        script_name = 'git-authors-rewrite.sh'
        with open(script_name, 'w') as script_sh:
            script_sh.write(script)
        subprocess.run('chmod +x ./{}'.format(script_name), stdout=subprocess.PIPE, shell=True)
        subprocess.run('./{}'.format(script_name), stdout=subprocess.PIPE, shell=True)
        tkinter.messagebox.showinfo(title='Success',
                                    message="Review the new Git history for errors and git push")
        global git_filter_ok
        git_filter_ok = True
        os.remove('./{}'.format(script_name))
    except Exception as e:
        with open('error.log', 'w') as f:
            f.write(str(e))
        tkinter.messagebox.showerror(title='Error', message='cannot git filter, see error.log')


def start():
    process = subprocess.run("git log --pretty=\"%an;%ae%n%cn;%ce\" | sort | uniq", stdout=subprocess.PIPE, shell=True)

    stdout = process.stdout.decode('utf-8')
    if len(stdout) == 0:
        tkinter.messagebox.showerror(title='Error',
                                     message='Not a git repository (or any of the parent directories): .git')
        sys.exit(-1)

    root = tkinter.Tk()
    root.title('Clean git authors')
    root.columnconfigure(0, weight=1)

    authors = parse_authors(stdout)
    merged_authors = {}
    git_filter_ok = False

    def update_merge_author():
        ids_to_merge = authors_list_widget.curselection()
        merge_to_id = destination_email_widget.current()
        merged_authors.update(merge_authors(authors, ids_to_merge, merge_to_id))
        logs_widget['text'] = json.dumps(merged_authors, indent=2)

    def git_filter_cmd():
        if not merged_authors:
            tkinter.messagebox.showerror(title='Error', message='merged authors cannot be empty')
            return

        result = tkinter.messagebox.askquestion("Git filter",
                                                "Warning: This action is destructive to your repository's history. If you're collaborating on a repository with others, it's considered bad practice to rewrite published history. You should only do this in an emergency. Are you sure you want to rewrite your history ?",
                                                icon='warning')
        if result != 'yes':
            return

        git_filter(merged_authors)

    width = 50
    # widgets
    explanation1 = tkinter.ttk.Label(text='Select every emails you want to merge')
    authors_display = tkinter.StringVar(value=get_list_authors(authors))
    authors_list_widget = tkinter.Listbox(width=width, selectmode='extended', listvariable=authors_display,
                                          exportselection=0)
    explanation2 = tkinter.Label(text='Select email, you want to merge in')
    destination_email_text = tkinter.StringVar(value=get_list_authors(authors)[0])
    destination_email_widget = tkinter.ttk.Combobox(textvariable=destination_email_text)
    merge_btn = tkinter.Button(text='1 - merge', command=update_merge_author, bg="green")
    explanation3 = tkinter.ttk.Label(text='Emails to be merged:')
    logs_widget = tkinter.ttk.Label()
    git_filter_btn = tkinter.Button(text="2 - Git filter", command=git_filter_cmd, bg="orange")
    git_push_btn = tkinter.Button(text="3 - Git push force", command=git_push, bg="red")

    # rendering
    explanation1.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    authors_list_widget.grid(row=2, column=0, sticky="nsew", padx=10)
    for i in range(0, len(authors), 2):
        authors_list_widget.itemconfigure(i, background='#f0f0ff')
    explanation2.grid(row=4, column=0, sticky="w", padx=10, pady=10)
    destination_email_widget.grid(row=6, column=0, sticky="nsew", padx=10)
    destination_email_widget['values'] = get_list_authors(authors)
    merge_btn.grid(row=8, column=0, sticky="nsew", padx=10, pady=10)
    explanation3.grid(row=10, column=0, sticky="w", padx=10)
    logs_widget.grid(row=12, column=0, sticky="w", padx=10, pady=10)
    git_filter_btn.grid(row=14, column=0, sticky="nsew", padx=10, pady=10)
    git_push_btn.grid(row=16, column=0, sticky="nsew", padx=10, pady=10)
    root.mainloop()


if __name__ == '__main__':
    start()
