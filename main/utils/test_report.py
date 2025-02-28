class TestReport:
    def __init__(self):
        self.total_cases = 0
        self.passed_cases = 0
        self.failed_cases = 0

    def update_report(self, result):
        self.total_cases += 1
        if result == "passed":
            self.passed_cases += 1
        elif result == "failed":
            self.failed_cases += 1

    def generate_report(self):
        return {
            "total_cases": self.total_cases,
            "passed_cases": self.passed_cases,
            "failed_cases": self.failed_cases,
            "pass_percentage": (self.passed_cases / self.total_cases) * 100 if self.total_cases > 0 else 0
        }

    def print_report(self):
        report = self.generate_report()
        print("\nTest Report Summary:")
        print(f"Total Cases: {report['total_cases']}")
        print(f"Passed Cases: {report['passed_cases']}")
        print(f"Failed Cases: {report['failed_cases']}")
        print(f"Pass Percentage: {report['pass_percentage']:.2f}%")
