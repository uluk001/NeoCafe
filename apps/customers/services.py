from apps.branches.models import Branch


def get_branch_name_and_id_list():
    """
    Get list of branches with their id and name.
    """
    branches = Branch.objects.all().only("id", "name_of_shop")
    return branches
