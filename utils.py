
def is_author_list_tag(tag):
    return (tag.name == 'a' and
            tag.parent.name == 'dd')
