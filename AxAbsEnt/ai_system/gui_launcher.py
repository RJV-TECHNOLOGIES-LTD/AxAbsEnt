import sys
import yaml
from ai_system.core_agent import SuperSQLAI

def main():
    ai = SuperSQLAI()
    print("""\n🚀 Super_SQL AI System Launcher
---------------------------
[1] Perceive Registered Domains
[2] Invoke Domain Method
[3] Show AI Cognitive State
[0] Exit
""")

    while True:
        choice = input("Select an option: ").strip()
        if choice == '1':
            domains = ai.perceive(base_path="architecture")
            print("\nDiscovered Domains:", domains)
        elif choice == '2':
            domain = input("Enter domain name: ")
            method = input("Enter method name: ")
            result = ai.invoke(domain=domain, method=method)
            print("Invocation Result:", result)
        elif choice == '3':
            with open("ai_system/simulation_mind.yaml") as f:
                state = yaml.safe_load(f)
                print("\nCurrent Cognitive State:\n", yaml.dump(state, sort_keys=False))
        elif choice == '0':
            print("Exiting Super_SQL AI System.")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()
