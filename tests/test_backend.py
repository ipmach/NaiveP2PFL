
import config
import node

import unittest


class TestBackend(unittest.TestCase):
    def setUp(self):
        self.config = config.Config(node_id="test_node", node_type="test_type")
        self.backend = node.Backend(self.config)

    def test_get_status(self) -> None:
        expected_status = {
            "node_id": "test_node",
            "node_type": "test_type",
            "current_status": "active",
            "current_version": 1
        }
        reply, httpStatus = self.backend.get_status()
        self.assertEqual(httpStatus, config.HttpStatus.ok)
        self.assertEqual(reply, expected_status)

    def test_get_status_after_change(self) -> None:
        expected_status = {
            "node_id": "test_node",
            "node_type": "test_type",
            "current_status": "unactive",
            "current_version": 1
        }
        self.backend.config.current_status = config.Status.unactive

        reply, httpStatus = self.backend.get_status()
        self.assertEqual(httpStatus, config.HttpStatus.ok)
        self.assertEqual(reply, expected_status)

    def test_change_status_by_command(self) -> None:
        expected_status = {
            "node_id": "test_node",
            "node_type": "test_type",
            "current_status": "unactive",
            "current_version": 1
        }
        _, httpStatus = self.backend.command(config.Commands.stop, "helloworld")
        self.assertEqual(httpStatus, config.HttpStatus.ok)

        reply, httpStatus = self.backend.get_status()
        self.assertEqual(httpStatus, config.HttpStatus.ok)
        self.assertEqual(reply, expected_status)

    def test_change_status_by_command_wrong_pwd(self) -> None:
        expected_status = {
            "node_id": "test_node",
            "node_type": "test_type",
            "current_status": "active",
            "current_version": 1
        }
        _, httpStatus = self.backend.command(config.Commands.stop, "fake")
        self.assertEqual(httpStatus, config.HttpStatus.forbidden)

        reply, httpStatus = self.backend.get_status()
        self.assertEqual(httpStatus, config.HttpStatus.ok)
        self.assertEqual(reply, expected_status)


class LogicTestCase(unittest.TestCase):
    def test_active2active(self) -> None:
        config_ = config.Config(node_id="test_node", node_type="test_type")
        reply, httpStatus = node._status_logic(config_, config.Commands.start)

        self.assertEqual(httpStatus, config.HttpStatus.ok)
        self.assertEqual(reply, "Already in status: active")
        self.assertEqual(config_.current_status, config.Status.active)

    def test_active2unactive(self) -> None:
        config_ = config.Config(node_id="test_node", node_type="test_type")
        reply, httpStatus = node._status_logic(config_, config.Commands.stop)

        self.assertEqual(httpStatus, config.HttpStatus.ok)
        self.assertEqual(reply, "Done")
        self.assertEqual(config_.current_status, config.Status.unactive)

    def test_active2start_training(self) -> None:
        config_ = config.Config(node_id="test_node", node_type="test_type")
        reply, httpStatus = node._status_logic(config_, config.Commands.train)

        self.assertEqual(httpStatus, config.HttpStatus.ok)
        self.assertEqual(reply, "Done")
        self.assertEqual(config_.current_status, config.Status.start_training)

    def test_unactive2active(self) -> None:
        config_ = config.Config(node_id="test_node", node_type="test_type")
        config_.current_status = config.Status.unactive
        reply, httpStatus = node._status_logic(config_, config.Commands.start)

        self.assertEqual(httpStatus, config.HttpStatus.ok)
        self.assertEqual(reply, "Done")
        self.assertEqual(config_.current_status, config.Status.active)

    def test_unactive2others(self) -> None:
        config_ = config.Config(node_id="test_node", node_type="test_type")
        config_.current_status = config.Status.unactive
        reply, httpStatus = node._status_logic(config_, config.Commands.train)

        self.assertEqual(httpStatus, config.HttpStatus.forbidden)
        self.assertEqual(reply, "Cannot change status from unactive")
        self.assertEqual(config_.current_status, config.Status.unactive)

    def test_doingtraining2others(self) -> None:
        config_ = config.Config(node_id="test_node", node_type="test_type")
        config_.current_status = config.Status.doing_training
        reply, httpStatus = node._status_logic(config_, config.Commands.stop)

        self.assertEqual(httpStatus, config.HttpStatus.forbidden)
        self.assertEqual(reply, "Cannot change status while training")
        self.assertEqual(config_.current_status, config.Status.doing_training)