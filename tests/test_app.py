import unittest

from app import custom_6n_method, fermat_factorization, pollard_rho, trial_division


class FactorTests(unittest.TestCase):
    def test_6n_plus_1(self):
        self.assertEqual(custom_6n_method(91), (7, 13))

    def test_6n_minus_1(self):
        self.assertEqual(custom_6n_method(35), (5, 7))

    def test_methods_on_semiprime(self):
        n = 1009 * 1013
        expected = (1009, 1013)
        self.assertEqual(trial_division(n), expected)
        self.assertEqual(fermat_factorization(n), expected)
        self.assertEqual(pollard_rho(n), expected)
        self.assertEqual(custom_6n_method(n), expected)


if __name__ == "__main__":
    unittest.main()
