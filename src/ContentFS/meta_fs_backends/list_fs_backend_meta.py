
# TODO: create an fs that will load from json/list that produces that json.
def load_from_path_dicts(self, paths_dict_list):
    if self.__loaded:
        raise Exception("Can load only once")

    for path_dict in paths_dict_list:
        child_dict = path_dict
        path = child_dict['path']
        names = self.path_to_names(path)

        # print(f"Path       : {path}")
        parent_cdir = self.get_or_create_descendant_cdir(names[:-1])
        # print(f"Parent Path: {parent_cdir.path}")
        type = child_dict['type']
        if type == 'FILE':
            mtime = child_dict['mtime']
            size = child_dict['size']
            child_cpath = CFile(names, mtime, size)
        else:
            child_cpath = CDirTree(names)
        parent_cdir.add_child(child_cpath)
    self.__loaded = True

