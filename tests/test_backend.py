
import node

import unittest


class TestBackend(unittest.TestCase):
    def setUp(self):
        self.config = node.Config(node_id="test_node", node_type="test_type")
        self.backend = node.Backend(self.config)

    def test_get_status(self) -> None:
        expected_status = {
            "node_id": "test_node",
            "node_type": "test_type",
            "current_status": "active",
            "current_version": 1
        }
        reply, httpStatus = self.backend.get_status()
        self.assertEqual(httpStatus, node.HttpStatus.ok)
        self.assertEqual(reply, expected_status)

    def test_get_status_after_change(self) -> None:
        expected_status = {
            "node_id": "test_node",
            "node_type": "test_type",
            "current_status": "unactive",
            "current_version": 1
        }
        self.backend.config.current_status = node.Status.unactive

        reply, httpStatus = self.backend.get_status()
        self.assertEqual(httpStatus, node.HttpStatus.ok)
        self.assertEqual(reply, expected_status)

    def test_change_status_by_command(self) -> None:
        expected_status = {
            "node_id": "test_node",
            "node_type": "test_type",
            "current_status": "unactive",
            "current_version": 1
        }
        _, httpStatus = self.backend.command(node.Commands.stop, "helloworld")
        self.assertEqual(httpStatus, node.HttpStatus.ok)

        reply, httpStatus = self.backend.get_status()
        self.assertEqual(httpStatus, node.HttpStatus.ok)
        self.assertEqual(reply, expected_status)

    def test_change_status_by_command_wrong_pwd(self) -> None:
        expected_status = {
            "node_id": "test_node",
            "node_type": "test_type",
            "current_status": "active",
            "current_version": 1
        }
        _, httpStatus = self.backend.command(node.Commands.stop, "fake")
        self.assertEqual(httpStatus, node.HttpStatus.forbidden)

        reply, httpStatus = self.backend.get_status()
        self.assertEqual(httpStatus, node.HttpStatus.ok)
        self.assertEqual(reply, expected_status)