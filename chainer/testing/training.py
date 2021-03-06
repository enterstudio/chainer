from __future__ import division

import mock

from chainer import training


def get_trainer_with_mock_updater(
        stop_trigger=(10, 'iteration'), iter_per_epoch=10):
    """Returns a :class:`~chainer.training.Trainer` object with mock updater.

    The returned trainer can be used for testing the trainer itself and the
    extensions. A mock object is used as its updater. The update function set
    to the mock correctly increments the iteration counts (
    ``updater.iteration``), and thus you can write a test relying on it.

    Args:
        stop_trigger: Stop trigger of the trainer.
        iter_per_epoch: The number of iterations per epoch.

    Returns:
        Trainer object with a mock updater.

    """
    updater = mock.Mock()
    updater.get_all_optimizers.return_value = {}
    updater.iteration = 0
    updater.epoch = 0
    updater.epoch_detail = 0
    updater.is_new_epoch = True
    updater.previous_epoch_detail = None

    def update():
        updater.update_core()
        updater.iteration += 1
        updater.epoch = updater.iteration // iter_per_epoch
        updater.epoch_detail = updater.iteration / iter_per_epoch
        updater.is_new_epoch = (updater.iteration - 1) // \
            iter_per_epoch != updater.epoch
        updater.previous_epoch_detail = (updater.iteration - 1) \
            / iter_per_epoch

    updater.update = update
    trainer = training.Trainer(updater, stop_trigger)
    return trainer
