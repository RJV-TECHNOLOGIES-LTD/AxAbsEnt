#!/usr/bin/env python3
import argparse
from AxAbsEnt.ai_system.core_agent import SuperSQLAI

def main():
    parser = argparse.ArgumentParser(description="AxAbsEnt CLI")
    parser.add_argument('--list', action='store_true', help="List discovered domains")
    parser.add_argument('--invoke', nargs=2, metavar=('DOMAIN', 'METHOD'), help="Invoke a method")
    args = parser.parse_args()

    ai = SuperSQLAI()

    if args.list:
        domains = ai.perceive(base_path="AxAbsEnt/architecture")
        print("Available Domains:", domains)

    elif args.invoke:
        result = ai.invoke(domain=args.invoke[0], method=args.invoke[1])
        print("Invocation Result:", result)

if __name__ == "__main__":
    main()
