import cdist.integration as cdist_integration


class CdistUtilts():
    @staticmethod
    def get_cdist_index():
        """
        Returns the next available instance index.
        This is useful while making simultaneous configurations of
        the same host.
        :return: the next available index
        """
        cdist_instance_index = cdist_integration.instance_index
        cdist_index = next(cdist_instance_index)
        return cdist_index

    @staticmethod
    def free_cdist_index(cdist_index):
        """
        Frees up the index that was used during configuring a host
        using cdist.
        :param cdist_index: The index to be freed
        :return:
        """
        cdist_instance_index = cdist_integration.instance_index
        cdist_instance_index.free(cdist_index)
