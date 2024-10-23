# test_main.py
import unittest
from unittest.mock import patch
import main
class TestMain(unittest.TestCase):
    @patch('main.TeamLeaderAI')
    def test_main_flow_create_project(self, MockTeamLeaderAI):
        mock_team_leader = MockTeamLeaderAI.return_value
        mock_team_leader.create_project.return_value = "Project created successfully"
        with patch('builtins.input', side_effect=["1", "web app"]):
            result = main.run_program()
            self.assertEqual(result, "Project created successfully")
            mock_team_leader.create_project.assert_called_once()
    @patch('main.TeamLeaderAI')
    def test_main_flow_debug_project(self, MockTeamLeaderAI):
        mock_team_leader = MockTeamLeaderAI.return_value
        mock_team_leader.debug_project.return_value = "Debugging completed"
        with patch('builtins.input', side_effect=["3"]):
            result = main.run_program()
            self.assertEqual(result, "Debugging completed")
            mock_team_leader.debug_project.assert_called_once()
    # Add additional tests for other options (Enhance, Add Features, Test)
if __name__ == '__main__':
    unittest.main()
