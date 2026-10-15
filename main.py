
from src.train import parse_args, train


def main():
    args = parse_args()
    train(args)


if __name__ == "__main__":
    main()
