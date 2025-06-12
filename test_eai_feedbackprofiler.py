import unittest
from eai_feedbackprofiler import match_rubric, td_flag, rubric_VC, rubric_VM, td_matrix

class TestEaiFeedbackProfiler(unittest.TestCase):

    def test_match_rubric_vc_within_range(self):
        score = 0.15
        expected = rubric_VC[(0.1, 0.2)]
        self.assertEqual(match_rubric(score, rubric_VC), expected)

    def test_match_rubric_vc_on_boundary_low(self):
        score = 0.1
        expected = rubric_VC[(0.1, 0.2)]
        self.assertEqual(match_rubric(score, rubric_VC), expected)

    def test_match_rubric_vc_on_boundary_high(self):
        score = 0.2
        expected = rubric_VC[(0.1, 0.2)]
        self.assertEqual(match_rubric(score, rubric_VC), expected)

    def test_match_rubric_vc_outside_range(self):
        score = 0.05
        self.assertIsNone(match_rubric(score, rubric_VC))

    def test_match_rubric_vm_within_range(self):
        score = 0.55
        expected = rubric_VM[(0.5, 0.6)]
        self.assertEqual(match_rubric(score, rubric_VM), expected)

    def test_td_flag_above_norm(self):
        # Test case for AI_dominantie
        p = 0.9
        v_type = "V_C"
        td_score = 0.4
        expected_flag = "AI_dominantie"
        # Retrieve the actual norm from td_matrix to ensure the test is valid
        actual_norm = td_matrix[(str(p), v_type)]["norm"]
        self.assertGreater(td_score, actual_norm) # Ensure td_score is indeed > norm
        self.assertEqual(td_flag(p, v_type, td_score), expected_flag)

    def test_td_flag_below_norm(self):
        # Test case for TD_balanced (when score is below norm)
        p = 0.9
        v_type = "V_C"
        td_score = 0.2
        expected_flag = "TD_balanced"
        # Retrieve the actual norm from td_matrix to ensure the test is valid
        actual_norm = td_matrix[(str(p), v_type)]["norm"]
        self.assertLessEqual(td_score, actual_norm) # Ensure td_score is indeed <= norm
        self.assertEqual(td_flag(p, v_type, td_score), expected_flag)

    def test_td_flag_equal_to_norm(self):
        # Test case for TD_balanced (when score is equal to norm)
        p = 0.5
        v_type = "V_M"
        # Retrieve the actual norm from td_matrix
        actual_norm = td_matrix[(str(p), v_type)]["norm"]
        td_score = actual_norm
        expected_flag = "TD_balanced"
        self.assertEqual(td_flag(p, v_type, td_score), expected_flag)

    def test_td_flag_underuse_warning_above_norm(self):
        # Test case for Underuse_warning
        p = 0.5
        v_type = "V_M"
        td_score = 0.6
        expected_flag = "Underuse_warning"
        # Retrieve the actual norm from td_matrix to ensure the test is valid
        actual_norm = td_matrix[(str(p), v_type)]["norm"]
        self.assertGreater(td_score, actual_norm) # Ensure td_score is indeed > norm
        self.assertEqual(td_flag(p, v_type, td_score), expected_flag)

    def test_td_flag_non_existent_combination(self):
        p = 0.7
        v_type = "V_X" # Non-existent v_type
        td_score = 0.5
        expected_flag = "TD_balanced"
        self.assertEqual(td_flag(p, v_type, td_score), expected_flag)

if __name__ == '__main__':
    unittest.main()
