import EmbedWTSS
import sys


if __name__ == "__main__":
    args = sys.argv.copy()
    args.pop(0)
    if not args:
        args.append(input("Please Enter a Path For WTSS File > \t"))
    Instance = EmbedWTSS.EmbedWTSS()
    Instance.run(file=args[0])
    while True:
        input()
