import inspect

from google.adk.runners import Runner

print("Signature:\n")
print(inspect.signature(Runner.run_async))

print("\nDocstring:\n")
print(Runner.run_async.__doc__)