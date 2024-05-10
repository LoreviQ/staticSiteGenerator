import os
import shutil

import markdown


def copy_directory(src, dst):
    if os.path.exists(dst):
        recursive_delete(dst)
    recursive_copy(src, dst, "")


def recursive_copy(src, dst, sub_path):
    s_path = os.path.join(src, sub_path)
    d_path = os.path.join(dst, sub_path)
    if not os.path.exists(s_path):
        raise ValueError("Invalid Path")
    if os.path.isdir(s_path):
        os.mkdir(d_path)
        dir_entries = os.listdir(s_path)
        for entry in dir_entries:
            recursive_copy(src, dst, os.path.join(sub_path, entry))
    if os.path.isfile(s_path):
        shutil.copy(s_path, d_path)


def recursive_delete(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        dir_entries = os.listdir(path)
        for entry in dir_entries:
            recursive_delete(os.path.join(path, entry))
        os.rmdir(path)


def generate_page(src, dst, template):
    print(f"Generating page from {src} to {dst} using {template}")
    with open(f"{src}", "r", encoding="UTF-8") as md_file:
        md_text = md_file.read()
    with open(f"{template}", "r", encoding="UTF-8") as html_file:
        html_text = html_file.read()
    content = markdown.markdown_to_html_node(md_text).to_html()
    title = markdown.extract_title(md_text)
    html_text = html_text.replace("{{ Title }}", f'"{title}"')
    html_text = html_text.replace("{{ Content }}", f'"{content}"')
    if os.path.exists(dst):
        os.remove(dst)
    with open(dst, "w", encoding="UTF-8") as out:
        out.write(html_text)


def recursive_generate_page(src, dst, template, sub_path=""):
    s_path = os.path.join(src, sub_path)
    d_path = os.path.join(dst, sub_path)
    if not os.path.exists(s_path):
        raise ValueError("Invalid Path")
    if os.path.isdir(s_path):
        if not os.path.exists(d_path):
            os.mkdir(d_path)
        dir_entries = os.listdir(s_path)
        for entry in dir_entries:
            recursive_generate_page(
                src,
                dst,
                template,
                os.path.join(sub_path, entry),
            )
    if os.path.isfile(s_path):
        generate_page(s_path, d_path[:-2] + "html", template)


if __name__ == "__main__":
    recursive_generate_page("./markdown/", "./static/", "./template.html")
    copy_directory("./static", "./public")
