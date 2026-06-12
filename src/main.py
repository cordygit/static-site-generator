import os
import shutil
import sys

from md_parse import extract_title, markdown_to_html_node

static_src_dir = "./static"
static_dst_dir = "./docs"


def main():
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    if os.path.exists(static_dst_dir):
        shutil.rmtree(static_dst_dir)
    os.mkdir(static_dst_dir)
    rcopy(static_src_dir, static_dst_dir)
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


def rcopy(src: str, dst: str):
    entries = os.listdir(src)
    for entry in entries:
        entry_path = os.path.join(src, entry)
        if os.path.isfile(entry_path):
            shutil.copy(entry_path, dst)
        else:
            new_dst_path = os.path.join(dst, entry)
            os.mkdir(new_dst_path)
            rcopy(entry_path, new_dst_path)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
):
    entries = os.listdir(dir_path_content)
    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_path):
            dest_path = os.path.join(dest_dir_path, entry[:-2] + "html")
            generate_page(entry_path, template_path, dest_path, basepath)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, entry)
            if os.path.exists(new_dest_dir_path):
                shutil.rmtree(new_dest_dir_path)
            os.mkdir(new_dest_dir_path)
            generate_pages_recursive(
                entry_path, template_path, new_dest_dir_path, basepath
            )

    pass


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f1:
        markdown = f1.read()
    with open(template_path) as f2:
        template = f2.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    full = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    with open(dest_path, "w") as f3:
        f3.write(full)
    f1.close()
    f2.close()
    f3.close()


main()
