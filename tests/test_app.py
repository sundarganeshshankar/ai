import unittest

from app import custom_6n_method, fermat_factorization, pollard_rho, trial_division


class FactorMethodTests(unittest.TestCase):
    def test_6n_plus_1_case(self):
        # 91 = 7 * 13 and 91 % 6 == 1
        self.assertEqual(custom_6n_method(91), (7, 13))

    def test_6n_minus_1_case(self):
        # 35 = 5 * 7 and 35 % 6 == 5
        self.assertEqual(custom_6n_method(35), (5, 7))

    def test_all_methods_factor_known_semiprime(self):
        n = 1009 * 1013
        expected = (1009, 1013)
        self.assertEqual(trial_division(n), expected)
        self.assertEqual(fermat_factorization(n), expected)
        self.assertEqual(pollard_rho(n), expected)
        self.assertEqual(custom_6n_method(n), expected)


if __name__ == "__main__":
    unittest.main()
