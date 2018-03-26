# Nano tests
GUI tests with selenium

## default.py

Subclass `DefaultCase` and create your own tests.

Preferrably, create a bootstrap `goToUrl`-method in `bootstrap.py`,
which wraps `DefaultCase`, and use that class to inherit from instead.

This could be effective if there is a lenghty login behavior that is similar
across alot of tests.
