from app.models.group import Group, insert_group, get_all_groups


def test_get_all_groups(app):
    g1 = Group(name="G1")
    g2 = Group(name="G2")

    insert_group(g1)
    insert_group(g2)

    groups = get_all_groups()

    assert len(groups) == 2
    assert groups[0].name == g1.name
    assert groups[1].name == g2.name
