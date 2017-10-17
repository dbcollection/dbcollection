"""
LSPe Keypoints process functions.
"""


from __future__ import print_function, division
import os

from dbcollection.datasets.leeds_sports_pose.leeds_sports_pose.keypoints import Keypoints as LspKps
from dbcollection.utils.file_load import load_matlab


class Keypoints(LspKps):
    """LSPe Keypoints preprocessing functions."""

    # metadata filename
    filename_h5 = 'detection'

    def load_annotations(self):
        """
        Load annotations from file and split them to train and test sets.
        """
        annot_filepath_lsp = os.path.join(self.data_path, 'lsp_dataset', 'joints.mat')
        annot_filepath_lspe = os.path.join(self.data_path, 'joints.mat')

        # load annotations file
        annotations_lsp = load_matlab(annot_filepath_lsp)
        annotations_lspe = load_matlab(annot_filepath_lspe)

        data = {
            "train": [],
            "test": []
        }

        # ---------------------------
        #  add lsp train + test data
        # ---------------------------

        image_filenames_lsp = os.listdir(os.path.join(self.data_path, 'lsp_dataset', 'images'))
        image_filenames_lsp.sort()

        for i in range(0, 2000):
            if i >= 1000:
                set_name = 'test'
            else:
                set_name = 'train'

            filename = os.path.join(self.data_path, 'lsp_dataset',
                                    'images', image_filenames_lsp[i])

            joints = []
            for j in range(0, 14):
                # is_visible => (0 - visible, 1 - hidden)
                joints.append([annotations_lsp['joints'][0][j][i],   # x
                               annotations_lsp['joints'][1][j][i],   # y
                               annotations_lsp['joints'][2][j][i]])  # is_visible

            data[set_name].append({"filename": filename, "joints": joints})

        # -----------------------
        #  add lspe train data
        # -----------------------

        image_filenames_lspe = os.listdir(os.path.join(self.data_path, 'images'))
        image_filenames_lspe.sort()

        set_name = 'train'
        for i in range(0, 10000):
            filename = os.path.join(self.data_path, 'images', image_filenames_lspe[i])

            joints = []
            for j in range(0, 14):
                # is_visible => (0 - visible, 1 - hidden)
                joints.append([annotations_lspe['joints'][j][0][i],   # x
                               annotations_lspe['joints'][j][1][i],   # y
                               annotations_lspe['joints'][j][2][i]])  # is_visible

            data[set_name].append({"filename": filename, "joints": joints})

        return data
