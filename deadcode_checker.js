const DeadCodeChecker = require('dead-code-checker');

const usecase_dirs = [
  "docs",
  "Docs",
  "example",
  "Example",
  "experimental_result",
  "Experimental_result",
  "notebook",
  "Notebook",
  "project",
  "Project",
  "result",
  "Result",
  "saved_result",
  "Saved_result",
  "test",
  "Test",
  "testing",
  "Testing",
  "tests",
  "Tests",
  "tests_end_to_end",
  "Tests_end_to_end",
  "tests_load",
  "Tests_load",
  "tracing_test",
  "Tracing_test",
  "tutorial",
  "Tutorial",
]
const deprecated_dirs = [
  "legacy",
  "Legacy",
  "old",
  "Old",
  "retired_benchmark",
  "Retired_benchmark",
]

const checker = new DeadCodeChecker('data/repos/dezoito__ollama-grid-search', {
  ignoreFolders: [...deprecated_dirs, ...usecase_dirs],
});

checker.run();

const report = checker.getReport();

console.log(report);