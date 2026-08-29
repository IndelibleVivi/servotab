import unittest

from batch_runner import publish_committed


class ExternalActions:
    def __init__(self) -> None:
        self.deliveries: list[str] = []
        self.sent_keys: set[str] = set()

    def send(self, payload: str) -> None:
        self.deliveries.append(payload)

    def send_once(self, action_key: str, payload: str) -> bool:
        if action_key in self.sent_keys:
            return False
        self.sent_keys.add(action_key)
        self.deliveries.append(payload)
        return True


class PublishCommittedTests(unittest.TestCase):
    def test_first_publish_sends_once_and_advances_state(self) -> None:
        state = {
            "results": [
                {
                    "status": "committed",
                    "external_action_key": "run-1",
                    "answer": "answer-1",
                }
            ]
        }
        actions = ExternalActions()

        publish_committed(state, actions)

        self.assertEqual(actions.deliveries, ["answer-1"])
        self.assertEqual(state["results"][0]["status"], "published")

    def test_restart_after_external_success_does_not_duplicate_action(self) -> None:
        state = {
            "results": [
                {
                    "status": "committed",
                    "external_action_key": "run-7",
                    "answer": "answer-7",
                }
            ]
        }
        actions = ExternalActions()
        actions.send_once("run-7", "answer-7")

        publish_committed(state, actions)

        self.assertEqual(actions.deliveries, ["answer-7"])
        self.assertEqual(state["results"][0]["status"], "published")


if __name__ == "__main__":
    unittest.main()
