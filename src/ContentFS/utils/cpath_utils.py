from ContentFS.cpaths.cpath import CPath
from ContentFS.exceptions import CFSException


class CPathUtils:
    @staticmethod
    def is_ancestor(candidate_ancestor: CPath, candidate_descendant: CPath) -> bool:
        if not candidate_ancestor.is_dir():
            raise CFSException(f"Candidate ancestor/parent must pass is_dir: {candidate_ancestor}")  # TODO: create more specific exception
        if candidate_ancestor.names_count >= candidate_descendant.names_count:
            return False

        ancestor_names = candidate_ancestor.names
        descendant_names = candidate_descendant.names
        for idx, ancestor_name in enumerate(ancestor_names):
            descendant_name = descendant_names[idx]
            if ancestor_name != descendant_name:
                return False
        return True

    @staticmethod
    def is_parent(candidate_parent: CPath, candidate_child: CPath) -> bool:
        if CPathUtils.is_ancestor(candidate_parent, candidate_child) \
                and candidate_parent.names_count == candidate_child.names_count - 1:
            return True
        return False
